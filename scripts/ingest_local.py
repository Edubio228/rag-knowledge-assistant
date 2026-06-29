# scripts/ingest_local.py
import os
from app.ingestion.loader import load_document
from app.ingestion.splitter import split_documents
from app.ingestion.embedder import get_embedding_model
from app.retrieval.vectorstore import get_vector_store

def ingest_local():
    sample_dir = "sample_data"
    if not os.path.exists(sample_dir):
        print(f"❌ Directory '{sample_dir}' not found. Create it and add documents.")
        return

    all_docs = []
    for filename in os.listdir(sample_dir):
        filepath = os.path.join(sample_dir, filename)
        if os.path.isfile(filepath):
            print(f"📄 Processing: {filename}")
            docs = load_document(filepath)
            all_docs.extend(docs)
            print(f"   → Loaded {len(docs)} pages/sections")

    if not all_docs:
        print("❌ No documents found. Add files to sample_data/")
        return

    print(f"📝 Total documents loaded: {len(all_docs)}")
    
    chunks = split_documents(all_docs)
    print(f"✂️  Split into {len(chunks)} chunks")

    embeddings = get_embedding_model()
    vector_store = get_vector_store(embeddings)
    
    # Clear existing data first (optional - prevents duplicates)
    # vector_store._collection.delete(where={})
    
    vector_store.add_documents(chunks)
    print(f"✅ Successfully ingested {len(chunks)} chunks into vector DB.")
    
    # Verify it worked
    count = vector_store._collection.count()
    print(f"📊 Total chunks now in DB: {count}")

if __name__ == "__main__":
    ingest_local()