ANSWER_PROMPT = """
You are answering using ONLY the sources below.
If the sources contain partial information, answer using what is available.
Only say "Not found in the documents." if the sources are truly unrelated.

Sources:
{sources}

Question: {question}

Return:
1) A concise answer.
2) Do NOT mention sources in the answer text.
"""