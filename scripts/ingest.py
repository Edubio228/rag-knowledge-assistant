import os
from app.ingestion.loader import download_documents_from_s3, load_document
from app.ingestion.splitter import split_documents
from app.ingestion.embedder import get_embedding_model
from app.retrieval.vectorstore import get_vector_store  # we'll implement next

def ingest_all():
    # 1. Download docs from S3
    file_paths = download_documents_from_s3()
    all_docs = []
    for path in file_paths:
        docs = load_document(path)
        all_docs.extend(docs)
    # 2. Split
    chunks = split_documents(all_docs)
    # 3. Embed and store
    embeddings = get_embedding_model()
    vector_store = get_vector_store(embeddings)
    vector_store.add_documents(chunks)
    print(f"Ingested {len(chunks)} chunks.")

if __name__ == "__main__":
    ingest_all()