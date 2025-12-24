from app.generation.answer import generate_answer
from app.ingestion.embedder import embeddings
from app.retrieval.retriever import retrieve
from app.storage.vector_store import get_vector_store


def chat(user_id: str, notebook_id: str, question: str):
    store = get_vector_store(user_id, notebook_id, embeddings)
    chunks = retrieve(question, store)

    result = generate_answer(question, chunks)

    # 🔒 Enforce stable return contract
    if isinstance(result, dict):
        return result

    return {
        "answer": result,
        "citations": []
    }