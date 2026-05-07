"""
Governance Scoring Configuration
"""

SCORING_CONFIG = {

    # --------------------------------------------------
    # Kombinations-Gewichte (müssen sich zu 1.0 summieren)
    # Überschreibbar pro Bot
    # --------------------------------------------------
    "semantic_weight":    0.65,
    "governance_weight":  0.35,

    # --------------------------------------------------
    # Origin — normalisiert 0.0–1.0
    # --------------------------------------------------
    "origin_weights": {
        "legislator":            1.0,
        "supervisory_authority": 0.8,
        "industry_association":  0.6,
        "consulting_firm":       0.5,
        "research_institution":  0.5,
        "corporate":             0.3,
        "internal":              0.3,
        "cloud_vendor":          0.2,
        "software_vendor":       0.2,
        "media":                 0.1,
        "unknown":               0.3,
    },

    # --------------------------------------------------
    # Document Type — normalisiert 0.0–1.0
    # --------------------------------------------------
    "document_type_weights": {
        "regulatory_text":      1.0,
        "supervisory_guidance": 0.8,
        "expert_opinion":       0.6,
        "consulting_framework": 0.6,
        "research_report":      0.5,
        "industry_position":    0.4,
        "press_article":        0.2,
        "blog_article":         0.2,
        "vendor_marketing":     0.1,
        "unknown":              0.3,
    },

    # --------------------------------------------------
    # Confidence — normalisiert 0.0–1.0
    # --------------------------------------------------
    "confidence_weights": {
        "high":   1.0,
        "medium": 0.6,
        "low":    0.2,
    },

    # --------------------------------------------------
    # Gewichtung innerhalb des Governance-Scores
    # --------------------------------------------------
    "governance_components": {
        "origin":        0.50,
        "document_type": 0.35,
        "confidence":    0.15,
    }
}