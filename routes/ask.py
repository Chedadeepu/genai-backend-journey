from fastapi import APIRouter
from pydantic import BaseModel
from genai.embeddings import search_similar_chunks

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(request: QuestionRequest):
    results = search_similar_chunks(request.question)

    return {
        "question": request.question,
        "answers": results
    }
