from config.engine_config import CONTEXT_CONFIG
from knowledge_core.retrieval.retrieval_models import ContextChunk, ContextPackage


class ContextBuilder:

    def __init__(self):
        self.max_chunks = CONTEXT_CONFIG["max_documents"] * CONTEXT_CONFIG["max_chunks_per_document"]
        self.min_document_score = CONTEXT_CONFIG.get("min_document_score", 0.0)

    def build_context(self, query, chunks):

        # --------------------------------------------------
        # Input: bereits selektierte Chunks (vom Orchestrator)
        # --------------------------------------------------

        # Filter: Chunks von Dokumenten unterhalb des Score-Threshold
        # ausschließen
        filtered_chunks = [
            chunk for chunk in chunks
            if self._get_chunk_score(chunk) >= self.min_document_score
        ]

        # Limitierung auf max_chunks
        selected_chunks = filtered_chunks[:self.max_chunks]

        context_chunks = []

        for chunk in selected_chunks:

            context_chunks.append(
                ContextChunk(
                    doc_id=chunk.doc_id,
                    chunk_id=chunk.chunk_id,
                    text=chunk.text,
                    chunk_index=chunk.chunk_index,
                    document_metadata=chunk.document_metadata
                )
            )

        sources = list({c.doc_id for c in context_chunks})

        return ContextPackage(
            query=query,
            chunks=context_chunks,
            sources=sources
        )

    def _get_chunk_score(self, chunk):
        """
        Extrahiere den Score aus dem Chunk.

        Score-Propagation (QueryPipeline Schritt 5) schreibt doc.score
        direkt auf chunk.score — daher zuerst direktes Attribut prüfen.
        """

        # Zuerst direktes Attribut (Score-Propagation schreibt auf chunk.score)
        if hasattr(chunk, 'score'):
            return chunk.score

        # Fallback: document_metadata
        if hasattr(chunk, 'document_metadata') and chunk.document_metadata:
            return chunk.document_metadata.get('score', 0.0)

        return 0.0