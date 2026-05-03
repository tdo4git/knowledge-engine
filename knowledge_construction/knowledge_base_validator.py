from pathlib import Path
import json
import torch
import faiss


class KnowledgeBaseValidator:

    def __init__(self, base_path: str):

        base = Path(base_path)

        self.registry_path = base / "registry" / "document_registry.json"
        self.chunks_path = base / "chunks" / "chunks.json"
        self.embeddings_path = base / "vector_index" / "embeddings.pt"
        self.index_path = base / "vector_index" / "index.faiss"

    # ------------------------------------------------
    # Public validation entrypoint
    # ------------------------------------------------

    def validate(self):

        print("Running Knowledge Base validation...")

        registry = self._load_registry()
        chunks = self._load_chunks()
        embeddings = self._load_embeddings()
        index = self._load_index()

        self._validate_doc_ids(registry)
        self._validate_chunk_doc_links(registry, chunks)
        self._validate_embedding_alignment(chunks, embeddings)
        self._validate_index_dimension(index, embeddings)

        print("Knowledge Base validation successful.")

    # ------------------------------------------------
    # Loaders
    # ------------------------------------------------

    def _load_registry(self):

        with open(self.registry_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_chunks(self):

        with open(self.chunks_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_embeddings(self):

        return torch.load(self.embeddings_path, map_location="cpu")

    def _load_index(self):

        return faiss.read_index(str(self.index_path))

    # ------------------------------------------------
    # Validation checks
    # ------------------------------------------------

    def _validate_doc_ids(self, registry):

        doc_ids = [doc["doc_id"] for doc in registry]

        if len(doc_ids) != len(set(doc_ids)):
            raise ValueError("Duplicate doc_id detected in registry.")

    def _validate_chunk_doc_links(self, registry, chunks):

        registry_ids = {doc["doc_id"] for doc in registry}

        for chunk in chunks:

            if chunk["doc_id"] not in registry_ids:
                raise ValueError(
                    f"Chunk {chunk['chunk_id']} references unknown doc_id {chunk['doc_id']}"
                )

    def _validate_embedding_alignment(self, chunks, embeddings):

        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Mismatch: {len(chunks)} chunks but {len(embeddings)} embeddings."
            )

    def _validate_index_dimension(self, index, embeddings):

        embedding_dim = embeddings.shape[1]
        index_dim = index.d

        if embedding_dim != index_dim:
            raise ValueError(
                f"Embedding dimension {embedding_dim} does not match index dimension {index_dim}"
            )