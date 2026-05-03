import json
from pathlib import Path
from typing import List, Dict

import torch
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from config.construction_config import (
    EMBEDDING_MODEL,
    CHUNKS_PATH,
    EMBEDDINGS_PATH,
    FAISS_INDEX_PATH,
    CHUNK_IDS_PATH
)


class EmbeddingGenerator:

    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    # ------------------------------------------------

    def run(self):

        chunks = self._load_chunks()

        if not chunks:
            print("No chunks found.")
            return

        existing_chunk_ids = self._load_existing_chunk_ids()

        # 🔒 deterministic ordering
        chunks = sorted(chunks, key=lambda x: x["chunk_id"])

        new_chunks = [
            c for c in chunks
            if c["chunk_id"] not in existing_chunk_ids
        ]

        if not new_chunks:
            print("No new chunks to embed.")
            return

        texts = [c["text"] for c in new_chunks]

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        embeddings = self._validate_embeddings(embeddings)

        # 🔥 atomic update sequence
        self._update_all(new_chunks, embeddings)

        print(f"New embeddings created: {len(new_chunks)}")

    # ------------------------------------------------
    # LOADERS
    # ------------------------------------------------

    def _load_chunks(self) -> List[Dict]:

        path = Path(CHUNKS_PATH)

        if not path.exists():
            return []

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _load_existing_chunk_ids(self):

        path = Path(CHUNK_IDS_PATH)

        if not path.exists():
            return set()

        try:
            with open(path, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            return set()

    # ------------------------------------------------
    # CORE UPDATE (ATOMIC)
    # ------------------------------------------------

    def _update_all(self, new_chunks, new_embeddings):

        # load existing
        existing_embeddings = self._load_existing_embeddings()
        existing_ids = self._load_existing_chunk_ids()

        new_ids = [c["chunk_id"] for c in new_chunks]

        # consistency check
        if any(cid in existing_ids for cid in new_ids):
            raise ValueError("Duplicate chunk_id detected")

        # combine embeddings
        combined_embeddings = (
            np.vstack([existing_embeddings, new_embeddings])
            if existing_embeddings is not None
            else new_embeddings
        )

        # rebuild index (safe, deterministic)
        index = self._build_faiss_index(combined_embeddings)

        # persist ALL artifacts together
        self._save_embeddings(combined_embeddings)
        self._save_index(index)
        self._save_chunk_ids(existing_ids.union(new_ids))

    # ------------------------------------------------
    # EMBEDDINGS
    # ------------------------------------------------

    def _load_existing_embeddings(self):

        path = Path(EMBEDDINGS_PATH)

        if not path.exists():
            return None

        return torch.load(path).numpy()

    def _save_embeddings(self, embeddings):

        path = Path(EMBEDDINGS_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)

        torch.save(torch.tensor(embeddings), path)

    # ------------------------------------------------
    # INDEX
    # ------------------------------------------------

    def _build_faiss_index(self, embeddings):

        embeddings = embeddings.astype("float32")

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        return index

    def _save_index(self, index):

        path = Path(FAISS_INDEX_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)

        faiss.write_index(index, str(path))

    # ------------------------------------------------
    # IDS
    # ------------------------------------------------

    def _save_chunk_ids(self, chunk_ids):

        path = Path(CHUNK_IDS_PATH)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(sorted(list(chunk_ids)), f, indent=2)

    # ------------------------------------------------
    # VALIDATION
    # ------------------------------------------------

    def _validate_embeddings(self, embeddings):

        if embeddings is None or len(embeddings) == 0:
            raise ValueError("Empty embeddings")

        if not isinstance(embeddings, np.ndarray):
            raise ValueError("Embeddings must be numpy array")

        if len(embeddings.shape) != 2:
            raise ValueError("Embeddings must be 2D")

        return embeddings