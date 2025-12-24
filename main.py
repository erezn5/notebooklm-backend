import tempfile
from pathlib import Path

from app.config import settings
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from app.auth.deps import get_current_user
from app.auth.jwt import create_access_token
from app.api.chat import chat

from app.ingestion.loader import load_documents, ingest_documents
from app.ingestion.web_loader import load_web_page

app = FastAPI(title="NotebookLM-style RAG")


# ---------- MODELS ----------

class ChatRequest(BaseModel):
    notebook_id: str
    question: str


class LoginRequest(BaseModel):
    email: str


# ---------- AUTH ----------

@app.post("/login")
def login(req: LoginRequest):
    token = create_access_token({"sub": req.email})
    return {"access_token": token}


# ---------- INGEST FILES ----------

@app.post("/ingest")
def ingest(
    notebook_id: str,
    files: List[UploadFile] = File(...),
    user=Depends(get_current_user),
):
    """
    Ingest uploaded PDF/TXT files into a notebook.
    Frontend must send multipart/form-data.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    tmp_paths: List[str] = []

    # Save to temporary files that exist on the BACKEND machine
    for f in files:
        suffix = Path(f.filename or "").suffix.lower()

        if suffix not in {".pdf", ".txt"}:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {f.filename}")

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(f.file.read())
            tmp_paths.append(tmp.name)

    docs = load_documents(tmp_paths)
    ingest_documents(user["user_id"], notebook_id, docs)

    return {
        "status": "ok",
        "docs_added": len(docs),
        "uploaded_files": [f.filename for f in files],
        "user": user["user_id"],
    }


# ---------- INGEST WEB ----------

@app.post("/ingest_web")
def ingest_web(
    notebook_id: str,
    urls: List[str],
    user=Depends(get_current_user),
):
    """
    Scrape and ingest web pages
    """
    all_docs = []

    for url in urls:
        try:
            text = load_web_page(url)
            all_docs.append({
                "text": text,
                "source": url,
                "page": None,
                "doc_id": url,
            })
        except Exception as e:
            print(f"Failed to ingest {url}: {e}")

    ingest_documents(user["user_id"], notebook_id, all_docs)

    return {
        "status": "ok",
        "pages_added": len(all_docs),
        "user": user["user_id"],
    }


# ---------- CHAT ----------

@app.post("/chat")
def chat_endpoint(
    req: ChatRequest,
    user=Depends(get_current_user),
):
    """
    Ask a question against a notebook
    """
    return chat(user["user_id"], req.notebook_id, req.question)

@app.get("/healthz")
def health():
    return {"status": "ok"}