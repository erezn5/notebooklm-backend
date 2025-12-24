from langchain_chroma import Chroma
from pathlib import Path

def get_vector_store(user_id: str, notebook_id: str, embedding_fn):
    base = Path("data") / user_id / notebook_id
    base.mkdir(parents=True, exist_ok=True)

    return Chroma(
        persist_directory=str(base),
        embedding_function=embedding_fn
    )