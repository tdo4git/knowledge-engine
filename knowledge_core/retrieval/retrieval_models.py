from dataclasses import dataclass
from typing import List


@dataclass
class ChunkCandidate:
    chunk_id: str
    doc_id: str
    text: str
    chunk_index: int
    similarity_score: float
    document_metadata: dict


@dataclass
class DocumentCandidate:
    doc_id: str
    chunks: List[ChunkCandidate]
    document_metadata: dict
    aggregated_similarity: float


@dataclass
class RetrievalResult:
    query: str
    chunk_candidates: List[ChunkCandidate]
    document_candidates: List[DocumentCandidate]


@dataclass
class RankedDocument:
    doc_id: str
    score: float                 # 🔥 EINHEITLICHES FELD
    chunks: List[ChunkCandidate]
    document_metadata: dict

    # optional für Explainability
    semantic_score: float
    governance_score: float


@dataclass
class ContextChunk:
    doc_id: str
    chunk_id: str
    text: str
    chunk_index: int
    document_metadata: dict


@dataclass
class ContextPackage:
    query: str
    chunks: List[ContextChunk]
    sources: List[str]