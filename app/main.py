
# app/main.py
from fastapi import FastAPI, HTTPException
from app.models import QuestionRequest, AnswerResponse, Citation  # <-- ADD Citation here
from app.retrieval.retriever import retrieve_and_answer
from app.cache.redis_cache import get_cache_value, set_cache
from app.feedback.feedback_store import store_feedback
import uuid

app = FastAPI(
    title="AI Knowledge Assistant",
    description="RAG system with OpenRouter and local embeddings",
    version="1.0.0"
)

app = FastAPI(
    title="AI Knowledge Assistant",
    description="RAG system with OpenRouter and local embeddings",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "AI Knowledge Assistant is running!"}

@app.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    """
    Ask a question against your internal documentation.
    Returns an answer with source citations.
    """
    question = request.question
    top_k = request.top_k
    
    # 1. Check Redis cache
    cached = get_cache_value(question)
    if cached:
        # Return cached response with a new feedback_id
        return AnswerResponse(
            answer=cached["answer"],
            citations=[Citation(**c) for c in cached["citations"]],
            feedback_id=str(uuid.uuid4())
        )
    
    # 2. Cache miss – run the RAG pipeline
    result = retrieve_and_answer(question, top_k)
    
    # 3. Store in cache for 1 hour (save as dict for JSON serialization)
    cache_data = {
        "answer": result["answer"],
        "citations": result["citations"]
    }
    set_cache(question, cache_data, ttl=3600)
    
    # 4. Generate feedback_id for this response
    feedback_id = str(uuid.uuid4())
    
    # (Optional) Store the response with feedback_id in a temporary DB
    # For now, we'll just return it and expect feedback with this ID
    
    return AnswerResponse(
        answer=result["answer"],
        citations=result["citations"],
        feedback_id=feedback_id
    )

@app.post("/feedback/{feedback_id}/{rating}")
async def feedback(feedback_id: str, rating: str):
    """
    Submit feedback for a previous answer.
    Rating must be 'up' or 'down'.
    """
    if rating not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="Rating must be 'up' or 'down'")
    
    store_feedback(feedback_id, rating)
    return {"status": "ok", "feedback_id": feedback_id, "rating": rating}

@app.get("/health")
async def health():
    """Simple health check endpoint."""
    return {"status": "healthy"}