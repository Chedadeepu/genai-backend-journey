import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# =========================
# Paths
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "faiss.index")
CHUNKS_PATH = os.path.join(BASE_DIR, "chunks.txt")

# =========================
# Globals (LAZY LOADING)
# =========================
model = None
dimension = 384
index = faiss.IndexFlatL2(dimension)
text_chunks = []

# =========================
# Lazy-load embedding model
# =========================
def get_model():
    global model
    if model is None:
        print("🔄 Loading embedding model (first request)...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

# =========================
# Load persisted data safely
# =========================
def load_persisted_data():
    global index, text_chunks
    try:
        if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
            index = faiss.read_index(INDEX_PATH)
            with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
                text_chunks = [line.strip() for line in f.readlines()]
            print(f"✅ Loaded {len(text_chunks)} chunks from disk")
        else:
            print("ℹ️ No persisted embeddings found, starting fresh")
    except Exception as e:
        print("⚠️ Failed to load persisted embeddings:", e)
        index = faiss.IndexFlatL2(dimension)
        text_chunks = []

# Load persisted data at startup (SAFE)
load_persisted_data()

# =========================
# Chunking
# =========================
def chunk_text(text: str, chunk_size: int = 500):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

# =========================
# Ingestion
# =========================
def create_embeddings_from_text(text: str):
    global index, text_chunks

    chunks = list(chunk_text(text))
    if not chunks:
        return 0

    text_chunks.extend(chunks)

    vectors = get_model().encode(chunks)
    vectors = np.array(vectors).astype("float32")
    index.add(vectors)

    # Persist FAISS index
    faiss.write_index(index, INDEX_PATH)

    # Persist chunks
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        for chunk in text_chunks:
            f.write(chunk.replace("\n", " ") + "\n")

    print(f"✅ Embedded and stored {len(chunks)} chunks")
    return len(chunks)

# =========================
# Semantic Search
# =========================
def search_similar_chunks(question: str, top_k: int = 3):
    if index.ntotal == 0 or not text_chunks:
        return ["No documents have been ingested yet."]

    question_vector = get_model().encode([question])
    question_vector = np.array(question_vector).astype("float32")

    distances, indices = index.search(question_vector, top_k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(text_chunks):
            results.append(text_chunks[idx])

    if not results:
        return ["No relevant content found in documents."]

    return results
