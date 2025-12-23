from fastapi import FastAPI
from database.db import engine
from database import models
from routes.students import router as student_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Day 5: Database Integrated"}

app.include_router(student_router)

from routes.documents import router as document_router

app.include_router(document_router)
from routes.ask import router as ask_router

app.include_router(ask_router)
from routes.ingest import router as ingest_router

app.include_router(ingest_router)

@app.get("/health")
def health():
    return {"status": "ok"}


