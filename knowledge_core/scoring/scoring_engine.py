from config.scoring_config import SCORING_CONFIG
from knowledge_core.retrieval.retrieval_models import RankedDocument


class ScoringEngine:

    def __init__(self, config_override: dict = None):

        cfg = config_override or SCORING_CONFIG

        self.semantic_weight    = cfg["semantic_weight"]
        self.governance_weight  = cfg["governance_weight"]

        self.origin_weights     = cfg["origin_weights"]
        self.doc_type_weights   = cfg["document_type_weights"]
        self.confidence_weights = cfg["confidence_weights"]
        self.gov_components     = cfg["governance_components"]

    def score(self, document_candidates):

        ranked = []

        for doc in document_candidates:

            meta = doc.document_metadata

            # --------------------------------------------------
            # Semantic score (normalized ~0–1 by FAISS)
            # --------------------------------------------------
            semantic_score = doc.aggregated_similarity

            # --------------------------------------------------
            # Governance score (normalized 0–1)
            # --------------------------------------------------
            origin_score     = self.origin_weights.get(meta.get("origin"), 0.3)
            doc_type_score   = self.doc_type_weights.get(meta.get("document_type"), 0.3)
            confidence_score = self.confidence_weights.get(meta.get("confidence_level"), 0.6)

            governance_score = (
                origin_score     * self.gov_components["origin"] +
                doc_type_score   * self.gov_components["document_type"] +
                confidence_score * self.gov_components["confidence"]
            )

            # --------------------------------------------------
            # Final score
            # --------------------------------------------------
            final_score = (
                self.semantic_weight   * semantic_score +
                self.governance_weight * governance_score
            )

            ranked.append(
                RankedDocument(
                    doc_id=doc.doc_id,
                    score=final_score,
                    chunks=doc.chunks,
                    document_metadata=meta,
                    semantic_score=semantic_score,
                    governance_score=governance_score,
                )
            )

        ranked.sort(key=lambda d: d.score, reverse=True)
        return ranked