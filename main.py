from fastapi import FastAPI
from routes.ask import router as ask_router
from routes.ingest import router as ingest_router

app = FastAPI(title="GenAI RAG Backend")

# RAG routes
app.include_router(ingest_router)
app.include_router(ask_router)

@app.get("/")
def root():
    return {"message": "GenAI RAG Backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
