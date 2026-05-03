from sentence_transformers import SentenceTransformer
import faiss
import json
from pathlib import Path
from collections import defaultdict
import numpy as np

# ----------------------------------
# Paths
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]

index_path = BASE_DIR / "knowledge_base/vector_index/index.faiss"
chunks_path = BASE_DIR / "knowledge_base/chunks/chunks.json"

# ----------------------------------
# Load
# ----------------------------------
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
query = "What are cloud requirements in DORA?"
q_emb = model.encode([query])

k = min(20, index.ntotal)
D, I = index.search(q_emb, k=k)

# ----------------------------------
# Aggregation
# ----------------------------------
doc_scores = defaultdict(list)

for score, idx in zip(D[0], I[0]):
    chunk = chunks[idx]
    doc_scores[chunk["doc_id"]].append(score)

# Top-3 mean
doc_ranking = []

for doc_id, scores in doc_scores.items():
    top_scores = sorted(scores, reverse=True)[:3]
    agg_score = np.mean(top_scores)
    doc_ranking.append((doc_id, agg_score))

doc_ranking = sorted(doc_ranking, key=lambda x: x[1])

# ----------------------------------
# Output
# ----------------------------------
print("\n--- DOCUMENT RANKING ---\n")

for doc_id, score in doc_ranking:
    print(f"{doc_id} → {score:.4f}")