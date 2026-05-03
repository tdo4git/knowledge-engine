from knowledge_core.retrieval.retrieval_models import ChunkCandidate


class CandidateRetriever:

    def __init__(self, knowledge_base, vector_top_k):

        self.kb = knowledge_base
        self.vector_top_k = vector_top_k

    def retrieve(self, query_vector):

        distances, indices = self.kb.vector_index.search(
            query_vector,
            self.vector_top_k
        )

        candidates = []

        for distance, idx in zip(distances[0], indices[0]):

            chunk = self.kb.chunks[idx]

            doc_meta = self.kb.get_document_metadata(chunk["doc_id"])

            similarity = 1 / (1 + distance)

            candidate = ChunkCandidate(
                chunk_id=chunk["chunk_id"],
                doc_id=chunk["doc_id"],
                text=chunk["text"],
                chunk_index=chunk["chunk_index"],
                similarity_score=similarity,
                document_metadata=doc_meta
            )

            candidates.append(candidate)

        return candidates