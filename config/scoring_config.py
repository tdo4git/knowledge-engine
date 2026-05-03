"""
Governance Scoring Configuration
"""

SCORING_CONFIG = {

    "origin_weights": {

        "legislator": 0.6,
        "supervisory_authority": 0.2,
        "consulting_firm": 0.1,
        "cloud_vendor": -0.05,
        "unknown": 0.0
    },

    "confidence_weights": {

        "high": 0.10,
        "medium": 0.0,
        "low": -0.10
    },

    "document_type_weights": {

        "regulatory_text": 0.4,
        "supervisory_guidance": 0.2,
        "expert_opinion": 0.05,
        "consulting_framework": 0.05,
        "research_report": 0.05,
        "vendor_marketing": -0.2,
        "blog_article": -0.1,
        "unknown": 0.0
    }

}
