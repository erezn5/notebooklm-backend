def retrieve(query, vector_store, k=5):
    results = vector_store.similarity_search_with_score(query, k=k)

    return [
        {
            "text": doc.page_content,
            "source": doc.metadata["source"],
            "page": doc.metadata.get("page"),
            "score": score
        }
        for doc, score in results
    ]

def dedupe_citations(chunks, max_items=4):
    seen = set()
    deduped = []

    for c in chunks:
        key = (c["source"], c.get("page"))
        if key not in seen:
            seen.add(key)
            deduped.append(c)
        if len(deduped) >= max_items:
            break

    return deduped