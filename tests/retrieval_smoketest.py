from sentence_transformers import SentenceTransformer
import faiss
import json
from pathlib import Path

# ----------------------------------
# Robust Path Handling
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]

index_path = BASE_DIR / "knowledge_base/vector_index/index.faiss"
chunks_path = BASE_DIR / "knowledge_base/chunks/chunks.json"

print("BASE_DIR:", BASE_DIR)
print("Index Path:", index_path)
print("Chunks Path:", chunks_path)

# ----------------------------------
# Load Data
# ----------------------------------
if not index_path.exists():
    raise FileNotFoundError(f"Index not found: {index_path}")

if not chunks_path.exists():
    raise FileNotFoundError(f"Chunks not found: {chunks_path}")

index = faiss.read_index(str(index_path))

with open(chunks_path) as f:
    chunks = json.load(f)

# ----------------------------------
# Model
# ----------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------------
# Query
# ----------------------------------
query = "What is DORA regulation about?"
q_emb = model.encode([query])

# ----------------------------------
# Search
# ----------------------------------
k = min(5, index.ntotal)
D, I = index.search(q_emb, k=k)

# ----------------------------------
# Results
# ----------------------------------
print("\n--- RESULTS ---\n")

print("chunks:", len(chunks))

print("\n--- INDEX INFO ---")
print("ntotal:", index.ntotal)
print("dim:", index.d)

for score, idx in zip(D[0], I[0]):
    chunk = chunks[idx]
    print(f"Score: {score:.4f}")
    print(f"Doc: {chunk['doc_id']}")
    print(f"Text: {chunk['text'][:200]}")
    print("-" * 50)