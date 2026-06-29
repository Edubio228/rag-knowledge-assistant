from langchain_chroma import Chroma
from app.config import settings

def get_vector_store(embeddings):
    # Persistent directory so we don't re‑embed every time
    persist_directory = "./chroma_db"
    return Chroma(
        embedding_function=embeddings,
        persist_directory=persist_directory,
        collection_name="docs"
    )