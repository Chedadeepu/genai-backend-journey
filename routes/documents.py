from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from database.db import SessionLocal
from database.models import Document

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db = SessionLocal()
    doc = Document(filename=file.filename, filepath=file_path)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    db.close()

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }
