import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

INDEX_PATH = "genai/faiss.index"
CHUNKS_PATH = "genai/chunks.txt"

# Load local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Embedding dimension for this model
dimension = 384

# Initialize defaults
index = faiss.IndexFlatL2(dimension)
text_chunks = []

# Load persisted data if available
if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
    index = faiss.read_index(INDEX_PATH)

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        text_chunks = [line.strip() for line in f.readlines()]

def chunk_text(text: str, chunk_size: int = 500):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

def create_embeddings_from_text(text: str):
    global text_chunks, index

    chunks = list(chunk_text(text))
    text_chunks.extend(chunks)

    vectors = model.encode(chunks)
    vectors = np.array(vectors).astype("float32")
    index.add(vectors)

    # Persist FAISS index
    faiss.write_index(index, INDEX_PATH)

    # Persist chunks
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        for chunk in text_chunks:
            f.write(chunk.replace("\n", " ") + "\n")

    return len(chunks)

def search_similar_chunks(question: str, top_k: int = 3):
    if index.ntotal == 0:
        return ["No documents have been ingested yet."]

    question_vector = model.encode([question])
    question_vector = np.array(question_vector).astype("float32")

    distances, indices = index.search(question_vector, top_k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(text_chunks):
            results.append(text_chunks[idx])

    if not results:
        return ["No relevant content found in documents."]

    return results
