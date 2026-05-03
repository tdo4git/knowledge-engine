from knowledge_core.retrieval.query_embedder import QueryEmbedder
from knowledge_core.retrieval.candidate_retriever import CandidateRetriever
from knowledge_core.retrieval.document_aggregator import DocumentAggregator
from knowledge_core.retrieval.retrieval_models import RetrievalResult

from config.engine_config import RETRIEVAL_CONFIG

class RetrievalEngine:

    def __init__(

        self,
        knowledge_base,
        embedding_model
    ):

        retrieval_cfg = RETRIEVAL_CONFIG

        self.embedder = QueryEmbedder(embedding_model)

        self.retriever = CandidateRetriever(
            knowledge_base,
            retrieval_cfg["vector_top_k"]
        )

        self.aggregator = DocumentAggregator(
            retrieval_cfg["document_aggregation"]["top_k_chunks"]
        )

    def retrieve(self, query):

        query_vector = self.embedder.embed(query)

        chunk_candidates = self.retriever.retrieve(query_vector)

        document_candidates = self.aggregator.aggregate(chunk_candidates)

        return RetrievalResult(
            query=query,
            chunk_candidates=chunk_candidates,
            document_candidates=document_candidates
        )