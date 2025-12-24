# notebooklm-backend

FastAPI backend for a NotebookLM-style RAG system.

Responsible for:
- Document ingestion (PDF / TXT / Web)
- Chunking & embeddings
- Vector storage (Chroma)
- Retrieval-Augmented Generation (RAG)
- JWT-based authentication
- Chat API for frontend clients (Streamlit / Web)

---

## Requirements

- Python **3.11.x** (required)
- pip
- virtualenv

---

## Project Structure
```
backend/
├── app/
│   ├── api/            # HTTP routes (chat, ingest, auth)
│   ├── auth/           # JWT logic & dependencies
│   ├── ingestion/      # PDF / TXT / Web ingestion
│   ├── vectorstore/    # Chroma vector store
│   ├── config/         # Settings & env loading
│   └── init.py
├── main.py             # FastAPI entry point
├── requirements.txt
└── README.md

---
```

## Environment Variables

Create a `.env` file in the backend root:

```env
OPENAI_API_KEY=sk-xxxx
JWT_SECRET_KEY=super-secret-key
JWT_ALGORITHM=HS256
```
# How to start
### 1) Create venv

python3 -m venv venv --p=3.11

### 2) activate the venv
source venv/bin/activate

### 3) install requirements into the virtual environment
pip install -r requirements.txt

### 4) Run the backend 
uvicorn main:app --reload --host 127.0.0.1 --port 8000