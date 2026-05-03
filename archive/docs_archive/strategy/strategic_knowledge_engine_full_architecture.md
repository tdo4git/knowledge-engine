# Strategic Knowledge Engine -- Full Architecture Diagram

This diagram illustrates the complete architecture of the Strategic
Knowledge Engine, including both the Knowledge Construction layer and
the Retrieval Engine layer.

------------------------------------------------------------------------

## High-Level System Architecture

``` mermaid
flowchart LR

subgraph Sources["Knowledge Sources"]
A[PDF / DOCX / TXT Documents]
end

subgraph Construction["Knowledge Construction Pipeline"]
B[Preview Extractor]
C[LLM Document Classifier]
D[Governance Rules]
E[Validation Layer]
F[Registry Builder]
G[Document Text Extractor]
H[Token-based Chunker]
I[Embedding Generator]
J[FAISS Index Builder]
K[Consistency Check]
end

subgraph KnowledgeBase["Knowledge Base"]
L[Document Registry]
M[Chunks]
N[Embeddings]
O[FAISS Vector Index]
P[Audit Log]
end

subgraph Retrieval["Retrieval Engine"]
Q[User Query]
R[Intent Engine]
S[Role Engine]
T[Query Embedding]
U[Vector Search]
V[Scoring Layer]
W[Document Grouping]
X[Context Builder]
end

subgraph Output["Response Layer"]
Y[LLM Reasoning / Answer Generation]
end

A --> B
B --> C
C --> D
D --> E
E --> F
F --> G
G --> H
H --> I
I --> J
J --> K

F --> L
H --> M
I --> N
J --> O
E --> P

Q --> R
R --> S
S --> T
T --> U
U --> V
V --> W
W --> X
X --> Y

O --> U
M --> W
L --> V
```

------------------------------------------------------------------------

## Architectural Layers

### Knowledge Construction Layer

Responsible for transforming documents into structured, vectorized
knowledge.

Key capabilities:

-   document onboarding
-   metadata classification
-   governance validation
-   chunking
-   embedding generation
-   vector index creation

Artifacts produced:

-   document_registry.json
-   chunks.json
-   embeddings.pt
-   index.faiss

------------------------------------------------------------------------

### Knowledge Base

Persistent storage layer containing:

-   document metadata
-   document chunks
-   vector embeddings
-   FAISS vector index
-   audit logs

------------------------------------------------------------------------

### Retrieval Engine

Processes user queries and retrieves the most relevant knowledge.

Pipeline:

query\
→ intent detection\
→ role detection\
→ query embedding\
→ vector search\
→ scoring\
→ document grouping\
→ context generation

------------------------------------------------------------------------

### Response Layer

The retrieved context is passed to an LLM for reasoning and answer
generation.

The LLM receives:

-   top-ranked chunks
-   document metadata
-   contextual grouping

------------------------------------------------------------------------

## Design Principles

-   Separation of Construction and Retrieval layers
-   Explainable knowledge sources
-   Incremental updates to the vector index
-   Metadata-aware retrieval scoring
-   Deterministic governance where possible

------------------------------------------------------------------------

## Result

The Strategic Knowledge Engine enables:

-   structured enterprise knowledge bases
-   explainable AI retrieval
-   advisory-grade reasoning contexts
