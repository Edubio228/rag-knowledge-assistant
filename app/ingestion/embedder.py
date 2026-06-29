# app/ingestion/embedder.py
from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Returns a local, free embedding model from Hugging Face.
    This runs entirely on your computer - no API key required!
    """
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",  # ~130MB, great for RAG
        # Alternative: "sentence-transformers/all-MiniLM-L6-v2" (also excellent)
        model_kwargs={'device': 'cpu'},       # Use 'cuda' if you have a GPU
        encode_kwargs={'normalize_embeddings': True}  # Better for similarity search
    )