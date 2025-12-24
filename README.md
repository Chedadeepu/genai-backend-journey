# GenAI RAG Backend – Document Question Answering System

This project is a backend system that enables users to ask natural language questions over PDF documents using Retrieval-Augmented Generation (RAG). It combines semantic search using vector embeddings with a lightweight local language model to generate meaningful answers grounded in document content.

The goal of this project is to demonstrate practical GenAI backend engineering concepts such as document ingestion, vector search, model orchestration, and production-aware system design.

---

##  What is RAG?

Retrieval-Augmented Generation (RAG) is an architecture where:
1. Relevant information is retrieved from a knowledge base (documents)
2. That information is passed as context to a language model
3. The model generates answers grounded in retrieved data

This approach avoids hallucinations and scales better than sending entire documents to an LLM.

---

##  Architecture Overview

PDF Document
↓
Text Extraction
↓
Chunking
↓
Local Embeddings (SentenceTransformers)
↓
FAISS Vector Store
↓
Semantic Retrieval
↓
Local LLM Answer Generation


---

##  Tech Stack

- **Backend Framework:** FastAPI
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)
- **Vector Store:** FAISS
- **LLM:** Local transformer-based model
- **Language:** Python
- **API Style:** REST

---

##  Key Features

- PDF ingestion via API
- Semantic search using vector embeddings
- Local, cost-free embeddings (no external APIs)
- Natural language answers generated from retrieved context
- Restart-safe vector persistence
- Production-aware lazy loading of ML models

---

##  Engineering Challenges & Learnings

- Handling in-memory vs persistent vector stores
- Designing ingestion inside the API process
- Lazy-loading ML models to avoid blocking server startup
- Managing deployment constraints on free cloud tiers
- Separating retrieval logic from generation logic

---

## Running Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload

Visit:

/docs for Swagger UI

/ingest to ingest documents

/ask to query documents

 Future Improvements

User-based document isolation

Authentication & authorization

Persistent vector databases (e.g., Pinecone, Weaviate)

Frontend UI

Streaming responses
