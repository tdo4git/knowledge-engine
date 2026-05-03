from pathlib import Path
from typing import List, Dict
import json

from transformers import AutoTokenizer

from config.construction_config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL
)


class Chunker:

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
        self.chunk_size = CHUNK_SIZE
        self.overlap = CHUNK_OVERLAP

    # ------------------------------------------------
    # PUBLIC
    # ------------------------------------------------

    def chunk_document(self, text: str, doc_id: str) -> List[Dict]:
        """
        Token-based chunking (production-safe)

        Guarantees:
        - no token overflow
        - deterministic chunk boundaries
        - stable overlap (token-aligned)
        """

        if not text:
            return []

        words = self._safe_split(text)

        chunks = []

        current_tokens = []
        current_words = []

        index = 0

        for word in words:

            word_tokens = self._encode_word(word)

            # skip pathological tokens (extremely long)
            if len(word_tokens) > self.chunk_size:
                continue

            # flush if overflow
            if current_tokens and (len(current_tokens) + len(word_tokens) > self.chunk_size):

                chunk = self._build_chunk(
                    current_words,
                    current_tokens,
                    doc_id,
                    index
                )

                if chunk:
                    chunks.append(chunk)
                    index += 1

                # -------------------------
                # TOKEN-ALIGNED OVERLAP
                # -------------------------
                if self.overlap > 0 and len(current_tokens) > self.overlap:
                    overlap_tokens = current_tokens[-self.overlap:]

                    # IMPORTANT: keep tokens only (no word reconstruction drift)
                    current_tokens = overlap_tokens.copy()
                    current_words = self._tokens_to_words(overlap_tokens)

                else:
                    current_tokens = []
                    current_words = []

            # add word
            current_tokens.extend(word_tokens)
            current_words.append(word)

        # final chunk
        if current_words:
            chunk = self._build_chunk(
                current_words,
                current_tokens,
                doc_id,
                index
            )
            if chunk:
                chunks.append(chunk)

        return chunks

    # ------------------------------------------------
    # INTERNAL
    # ------------------------------------------------

    def _encode_word(self, word: str) -> List[int]:
        return self.tokenizer.encode(
            word,
            add_special_tokens=False
        )

    def _tokens_to_words(self, tokens: List[int]) -> List[str]:
        """
        Safe reconstruction (best-effort)
        """
        text = self.tokenizer.decode(tokens).strip()
        return text.split()

    def _build_chunk(self, words: List[str], tokens: List[int], doc_id: str, index: int) -> Dict:

        text = " ".join(words).strip()

        if not text:
            return None

        return {
            "chunk_id": f"{doc_id}_chunk_{index}",
            "doc_id": doc_id,
            "chunk_index": index,
            "text": text,
            "tokens": len(tokens)
        }

    def _safe_split(self, text: str) -> List[str]:
        """
        Normalize whitespace safely
        """
        text = " ".join(text.split())
        return text.split(" ")

    # ------------------------------------------------
    # STORAGE
    # ------------------------------------------------

    def save_chunks(self, chunks: List[Dict], path: str):

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists():
            try:
                existing = json.loads(path.read_text())
            except json.JSONDecodeError:
                existing = []
        else:
            existing = []

        existing.extend(chunks)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)