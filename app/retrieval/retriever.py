# app/retrieval/retriever.py
from typing import Dict, Any
from app.retrieval.vectorstore import get_vector_store
from app.ingestion.embedder import get_embedding_model
from app.llm.llm_client import get_llm


def retrieve_and_answer(question: str, top_k: int = 3, model: str = "openrouter/free") -> Dict[str, Any]:
    """
    Retrieve relevant document chunks and generate an answer using OpenRouter.
    """
    # 1. Get embeddings and vector store
    embeddings = get_embedding_model()
    vector_store = get_vector_store(embeddings)
    
    # 2. Retrieve chunks using similarity_search
    docs = vector_store.similarity_search(question, k=top_k)
    
    if not docs:
        return {
            "answer": "I don't have any documents that can answer this question.",
            "citations": []
        }
    
    # 3. Build context and citations
    context = "\n\n---\n\n".join([doc.page_content for doc in docs])
    citations = [
        {
            "source": doc.metadata.get("source", "Unknown"),
            "chunk": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
        }
        for doc in docs
    ]
    
    # 4. Create a clear prompt
    prompt = f"""You are a helpful assistant. Answer the question based ONLY on the following context.
If the answer is not in the context, say "I don't have enough information to answer that."

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""
    
    # 5. Call the LLM and extract the text
    llm = get_llm(model=model, temperature=0.2)
    answer = llm.invoke(prompt).content
    
    return {
        "answer": answer,
        "citations": citations
    }