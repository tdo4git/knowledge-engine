import json
from pathlib import Path
from typing import List, Set

import torch
import faiss

from config.construction_config import (
    CHUNKS_PATH,
    EMBEDDINGS_PATH,
    FAISS_INDEX_PATH,
    CHUNK_IDS_PATH
)


class IndexConsistencyCheck:

    def run(self):

        chunks = self._load_chunks()
        embeddings = self._load_embeddings()
        chunk_ids = self._load_chunk_ids()
        index = self._load_index()

        chunk_id_set = {c["chunk_id"] for c in chunks}

        n_chunks = len(chunks)
        n_embeddings = len(embeddings)
        n_chunk_ids = len(chunk_ids)
        n_index = index.ntotal

        print("\nKnowledge Base Consistency Check")
        print("---------------------------------")

        print(f"Chunks:        {n_chunks}")
        print(f"Embeddings:    {n_embeddings}")
        print(f"Chunk IDs:     {n_chunk_ids}")
        print(f"FAISS entries: {n_index}")

        # ------------------------------------------------
        # 1. Size consistency
        # ------------------------------------------------

        if not (n_embeddings == n_chunk_ids == n_index):
            raise ValueError(
                "\n❌ Size mismatch detected:\n"
                f"embeddings={n_embeddings}, chunk_ids={n_chunk_ids}, index={n_index}"
            )

        # ------------------------------------------------
        # 2. Chunk ID consistency (chunks ↔ ids)
        # ------------------------------------------------

        missing_in_ids = chunk_id_set - set(chunk_ids)
        extra_in_ids = set(chunk_ids) - chunk_id_set

        if missing_in_ids or extra_in_ids:
            raise ValueError(
                "\n❌ Chunk ID mismatch:\n"
                f"Missing in chunk_ids: {list(missing_in_ids)[:5]}\n"
                f"Extra in chunk_ids: {list(extra_in_ids)[:5]}"
            )

        # ------------------------------------------------
        # 3. Duplicate detection
        # ------------------------------------------------

        if len(chunk_ids) != len(set(chunk_ids)):
            raise ValueError("\n❌ Duplicate chunk_ids detected")

        # ------------------------------------------------
        # 4. Order consistency (critical for retrieval!)
        # ------------------------------------------------

        expected_order = sorted(chunk_ids)

        if chunk_ids != expected_order:
            raise ValueError(
                "\n❌ Chunk ID order is not deterministic.\n"
                "Expected sorted order."
            )

        # ------------------------------------------------
        # 5. Embedding dimension consistency
        # ------------------------------------------------

        if len(embeddings.shape) != 2:
            raise ValueError("\n❌ Embeddings must be 2D tensor")

        dimension = embeddings.shape[1]

        if index.d != dimension:
            raise ValueError(
                "\n❌ Embedding dimension mismatch:\n"
                f"embeddings={dimension}, index={index.d}"
            )

        print("\n✔ Knowledge Base fully consistent.")

    # ------------------------------------------------
    # LOADERS
    # ------------------------------------------------

    def _load_chunks(self) -> List[dict]:

        path = Path(CHUNKS_PATH)

        if not path.exists():
            raise ValueError("chunks.json missing")

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_embeddings(self):

        path = Path(EMBEDDINGS_PATH)

        if not path.exists():
            raise ValueError("embeddings.pt missing")

        return torch.load(path)

    def _load_chunk_ids(self) -> List[str]:

        path = Path(CHUNK_IDS_PATH)

        if not path.exists():
            raise ValueError("chunk_ids.json missing")

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_index(self):

        path = Path(FAISS_INDEX_PATH)

        if not path.exists():
            raise ValueError("faiss index missing")

        return faiss.read_index(str(path))