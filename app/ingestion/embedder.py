from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

def embed(texts):
    return embeddings.embed_documents(texts)