from fastapi import APIRouter
from genai.pdf_reader import extract_text_from_pdf
from genai.embeddings import create_embeddings_from_text

router = APIRouter()

@router.post("/ingest")
def ingest_documents():
    pdf_path = "uploads/KarmaQuest_IEEE_Paper.pdf"  # change if needed

    text = extract_text_from_pdf(pdf_path)
    chunks = create_embeddings_from_text(text)

    return {
        "message": "Document ingested successfully",
        "chunks_created": chunks
    }
