from config.engine_config import CONTEXT_CONFIG
from knowledge_core.retrieval.retrieval_models import ContextChunk, ContextPackage


class ContextBuilder:

    def __init__(self):
        self.max_chunks = CONTEXT_CONFIG["max_documents"] * CONTEXT_CONFIG["max_chunks_per_document"]

    def build_context(self, query, chunks):

        # --------------------------------------------------
        # Input: bereits selektierte Chunks (vom Orchestrator)
        # --------------------------------------------------

        selected_chunks = chunks[:self.max_chunks]

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