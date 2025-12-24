from langchain_openai import ChatOpenAI
from .prompts import ANSWER_PROMPT
from ..retrieval.retriever import dedupe_citations


def get_llm():
    return ChatOpenAI(model="gpt-4o-mini")

def generate_answer(question, chunks):
    sources_text = "\n\n".join(
        f"[{i+1}] {c['text']}"
        for i, c in enumerate(chunks)
    )

    prompt = ANSWER_PROMPT.format(
        sources=sources_text,
        question=question
    )

    answer = get_llm().invoke(prompt).content

    chunks = dedupe_citations(chunks)

    citations = [
        {
            "source": c["source"],
            "page": c.get("page"),
            "snippet": c["text"][:200]
        }
        for c in chunks
    ]

    return {
        "answer": answer,
        "citations": citations
    }