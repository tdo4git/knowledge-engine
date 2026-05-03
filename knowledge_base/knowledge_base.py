from pathlib import Path
from typing import List, Dict, Any
import json
import torch
import faiss


class KnowledgeBase:
    """
    Immutable container for all structured knowledge artifacts.

    The KnowledgeBase is created by the Knowledge Construction pipeline
    and used read-only by the Knowledge Engine.
    """

    def __init__(
        self,
        chunks: List[Dict[str, Any]],
        embeddings,
        registry: List[Dict[str, Any]],
        vector_index: faiss.Index
    ):
        self._chunks = chunks
        self._embeddings = embeddings

        # original registry (list, as stored)
        self._registry = registry

        # runtime index for fast lookup
        self._registry_index = {doc["doc_id"]: doc for doc in registry}

        self._vector_index = vector_index

    # ------------------------------------------------
    # Read-only accessors
    # ------------------------------------------------

    @property
    def chunks(self) -> List[Dict[str, Any]]:
        return self._chunks

    @property
    def embeddings(self):
        return self._embeddings

    @property
    def registry(self) -> List[Dict[str, Any]]:
        return self._registry

    @property
    def vector_index(self) -> faiss.Index:
        return self._vector_index

    # ------------------------------------------------
    # Metadata helper
    # ------------------------------------------------

    def get_document_metadata(self, doc_id: str) -> Dict[str, Any]:
        """
        Retrieve metadata for a specific document from the registry.
        """
        return self._registry_index.get(doc_id)

    # ------------------------------------------------
    # Factory loader
    # ------------------------------------------------

    @classmethod
    def load_from_disk(cls, base_path: str):
        """
        Load a KnowledgeBase from the knowledge_base directory.
        """

        base = Path(base_path)

        chunks_path = base / "chunks" / "chunks.json"
        embeddings_path = base / "vector_index" / "embeddings.pt"
        registry_path = base / "registry" / "document_registry.json"
        vector_index_path = base / "vector_index" / "index.faiss"

        # Load chunks
        with open(chunks_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        # Load embeddings
        embeddings = torch.load(embeddings_path, map_location="cpu")

        # Load registry (LIST – original format)
        with open(registry_path, "r", encoding="utf-8") as f:
            registry_list = json.load(f)

        # Load FAISS vector index
        vector_index = faiss.read_index(str(vector_index_path))

        return cls(
            chunks=chunks,
            embeddings=embeddings,
            registry=registry_list,
            vector_index=vector_index
        )

    # ------------------------------------------------
    # Utility
    # ------------------------------------------------

    def __repr__(self):
        return (
            f"KnowledgeBase("
            f"documents={len(self._registry)}, "
            f"chunks={len(self._chunks)}, "
            f"embeddings={len(self._embeddings)})"
        )