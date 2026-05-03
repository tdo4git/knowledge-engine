# Retrieval Architecture Guideline – Strategic Knowledge Engine
Version: 3.3
Layer: Architecture

## Status
This document replaces the previous version of `retrieval_architecture_guideline.md`.

## Purpose
The Retrieval Engine transforms a user query into a structured, explainable knowledge context for the reasoning model. 
It operates exclusively on the curated Knowledge Base and ensures governance‑aware knowledge selection.

---

# Retrieval Pipeline

Query
→ Query Embedding
→ Vector Search
→ Candidate Chunk Retrieval
→ Document Aggregation
→ Governance Scoring
→ Context Construction

This pipeline ensures high recall during retrieval and high precision through governance‑aware ranking.

---

# Step 1 – Query Embedding

The user query is embedded using the same embedding model that was used to generate chunk embeddings.

Example model:
sentence-transformers/all-MiniLM-L6-v2

Consistency between document and query embeddings ensures meaningful semantic similarity.

---

# Step 2 – Vector Search

The query embedding is compared with the FAISS vector index.

Input:
query embedding

Output:
Top‑K similar chunks

The goal of this step is **high recall**, not final ranking.

---

# Step 3 – Candidate Chunk Retrieval

The indices returned by FAISS are mapped to chunks in:

knowledge_base/chunks/chunks.json

Each candidate chunk includes:

- chunk_id
- doc_id
- chunk_index
- text
- similarity_score
- document metadata

---

# Step 4 – Document Aggregation

Chunks are grouped by their source document.

ChunkCandidates
↓
DocumentCandidates

The aggregated similarity score of a document is computed from the top chunks retrieved from that document.

Recommended aggregation:

Top‑3 mean similarity

This avoids unstable rankings caused by single high‑scoring chunks.

---

# Step 5 – Governance Scoring

Document ranking combines semantic relevance with governance signals from the registry.

Final Score =

semantic_similarity  
+ origin_weight  
+ confidence_weight  
+ document_type_weight

Registry metadata used:

origin  
confidence_level  
document_type

This mechanism ensures regulatory and high‑trust sources are prioritized.

Additional signals:

- review_required may be used to:
  - downrank uncertain documents
  - flag results for explanation
  - influence answer transparency

This enables integration of quality signals from the construction pipeline into retrieval.

## Governance Signal Origin (Update)

Governance signals used in retrieval scoring are generated during the
Knowledge Construction pipeline via a centralized governance process.

Source:

Classification (LLM, contract-driven)
→ apply_governance()

This includes:
- origin normalization
- jurisdiction rules
- bias derivation
- confidence calculation

Retrieval does NOT generate governance signals.
It only consumes them from the document registry.


## Scoring Model (Refined)

The scoring engine combines:

1. Semantic Similarity (vector-based)
2. Governance Signals (from registry)

Example scoring logic:

score =
    semantic_similarity
    + origin_weight
    + confidence_weight
    + document_type_weight
    - bias_penalty

This ensures:

regulatory sources > advisory > vendor > marketing

Bias is used as a negative signal to prevent over-weighting of promotional content.

## Bias Handling

Each document includes a bias_level derived during governance.

Usage in retrieval:
- high bias → downranking
- neutral → no impact

Purpose:
- prevent over-representation of vendor or marketing content
- ensure balanced, trustworthy context construction
---

# Step 6 – Context Construction

The Context Builder selects chunks from the highest ranked documents.

Strategy:

Balanced Multi‑Document Context

Example:

Top Documents
↓
Top Chunks per Document
↓
LLM Context

Typical configuration:

max_documents = 5  
max_chunks_per_document = 2

---

# Explainability

Every retrieved chunk is traceable to:

chunk_id → doc_id → document metadata

This enables transparent explanations of why information was retrieved.

---

# Design Principles

Explainable  
Governance‑aware  
Document‑centric  
Deterministic where possible  
Separation of retrieval and ranking