from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )

    chunks = []
    for doc in docs:
        for chunk in splitter.split_text(doc["text"]):
            chunks.append({
                "text": chunk,
                "source": doc["source"],   # filename
                "page": doc.get("page"),
                "doc_id": doc["doc_id"]
            })

    return chunks