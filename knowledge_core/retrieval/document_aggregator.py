from collections import defaultdict
from statistics import mean
from knowledge_core.retrieval.retrieval_models import DocumentCandidate

class DocumentAggregator:

    def __init__(self, top_k_chunks=3):

        self.top_k_chunks = top_k_chunks

    def aggregate(self, chunk_candidates):

        grouped = defaultdict(list)

        for chunk in chunk_candidates:
            grouped[chunk.doc_id].append(chunk)

        document_candidates = []

        for doc_id, chunks in grouped.items():

            # sort chunks by similarity
            sorted_chunks = sorted(
                chunks,
                key=lambda c: c.similarity_score,
                reverse=True
            )

            top_chunks = sorted_chunks[:self.top_k_chunks]

            aggregated_score = mean(
                c.similarity_score for c in top_chunks
            )

            document_candidate = DocumentCandidate(
                doc_id=doc_id,
                chunks=top_chunks,
                document_metadata=top_chunks[0].document_metadata,
                aggregated_similarity=aggregated_score
            )

            document_candidates.append(document_candidate)

        return document_candidates