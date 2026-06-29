# app/main.py
from fastapi import FastAPI, HTTPException
from app.models import QuestionRequest, AnswerResponse, Citation
from app.retrieval.retriever import retrieve_and_answer
from app.feedback.feedback_store import store_feedback
import uuid

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

    # Run the RAG pipeline (caching is disabled)
    result = retrieve_and_answer(question, top_k)

    # Generate a feedback_id for this response
    feedback_id = str(uuid.uuid4())

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