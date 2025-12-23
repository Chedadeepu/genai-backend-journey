from fastapi import APIRouter
from pydantic import BaseModel
from genai.embeddings import search_similar_chunks
from genai.llm import generate_answer

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(request: QuestionRequest):
    chunks = search_similar_chunks(request.question)

    context = "\n".join(chunks)
    answer = generate_answer(context, request.question)

    return {
        "question": request.question,
        "answer": answer,
        "context_used": chunks
    }
