import re
import uuid
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.ingestion.embedder import embeddings
from app.storage.vector_store import get_vector_store


def ingest_documents(user_id: str, notebook_id: str, documents: list[dict]):
    """
    Ingest already-loaded documents into the vector store
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    texts = []
    metadatas = []

    for doc in documents:
        chunks = splitter.split_text(doc["text"])

        for chunk in chunks:
            texts.append(chunk)
            metadatas.append({
                "source": doc["source"],
                "page": doc.get("page"),
                "doc_id": doc["doc_id"]
            })

    if not texts:
        return

    store = get_vector_store(user_id, notebook_id, embeddings)
    store.add_texts(texts, metadatas)

def load_documents(file_paths: List[str]):
    """
    Load files and normalize them into a common document format
    """
    documents = []

    for path in file_paths:
        doc_id = str(uuid.uuid4())

        if path.endswith(".pdf"):
            loader = PyPDFLoader(path)
            pages = loader.load()

            for page in pages:
                documents.append({
                    "text": normalize_text(page.page_content),
                    "source": path,
                    "page": page.metadata.get("page"),
                    "doc_id": doc_id
                })

        elif path.endswith(".txt"):
            loader = TextLoader(path)
            docs = loader.load()

            for doc in docs:
                documents.append({
                    "text": normalize_text(doc.page_content),
                    "source": path,
                    "page": None,
                    "doc_id": doc_id
                })

        else:
            raise ValueError(f"Unsupported file type: {path}")

    return documents

def normalize_text(text: str) -> str:
    # remove letter-by-letter spacing
    text = re.sub(r'(?<=\w)\s(?=\w)', '', text)
    # collapse whitespace
    text = re.sub(r'\s{2,}', ' ', text)
    # normalize newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()