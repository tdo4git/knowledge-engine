from config.scoring_config import SCORING_CONFIG
from knowledge_core.retrieval.retrieval_models import RankedDocument


class ScoringEngine:

    def __init__(self):

        self.origin_weights = SCORING_CONFIG["origin_weights"]
        self.confidence_weights = SCORING_CONFIG["confidence_weights"]
        self.document_type_weights = SCORING_CONFIG["document_type_weights"]

    def score(self, document_candidates):

        ranked_documents = []

        for doc in document_candidates:

            meta = doc.document_metadata

            # ------------------------------
            # Semantic score
            # ------------------------------
            semantic_score = doc.aggregated_similarity

            # ------------------------------
            # Governance score
            # ------------------------------
            origin_score = self.origin_weights.get(meta.get("origin"), 0)

            confidence_score = self.confidence_weights.get(
                meta.get("confidence_level"),
                0
            )

            doc_type_score = self.document_type_weights.get(
                meta.get("document_type"),
                0
            )

            governance_score = (
                origin_score +
                confidence_score +
                doc_type_score
            )

            # ------------------------------
            # Final score
            # ------------------------------
            final_score = semantic_score + governance_score

            ranked_documents.append(
                RankedDocument(
                    doc_id=doc.doc_id,
                    score=final_score,                 # 🔥 zentral
                    chunks=doc.chunks,
                    document_metadata=meta,
                    semantic_score=semantic_score,
                    governance_score=governance_score
                )
            )

        # ------------------------------
        # Sort
        # ------------------------------
        ranked_documents.sort(
            key=lambda d: d.score,
            reverse=True
        )

        return ranked_documents