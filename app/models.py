# app/models.py
from pydantic import BaseModel
from typing import List, Optional

class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3

class Citation(BaseModel):
    source: str   # file name or S3 key
    chunk: str    # first 100 chars of the retrieved chunk

class AnswerResponse(BaseModel):
    answer: str
    citations: List[Citation]
    feedback_id: Optional[str] = None