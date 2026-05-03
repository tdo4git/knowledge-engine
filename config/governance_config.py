# =========================================================
# GOVERNANCE CONFIG – PRODUCTION VERSION
# =========================================================

# =========================================================
# 1. ORIGIN DETECTION
# =========================================================

AUTHOR_ORIGIN_MAP = {
    # Legislator
    "europäische union": "legislator",
    "european parliament": "legislator",
    "rat der europäischen union": "legislator",
    "european commission": "legislator",

    # Supervisory
    "eba": "supervisory_authority",
    "eiopa": "supervisory_authority",
    "bafin": "supervisory_authority",

    # Consulting
    "deloitte": "consulting_firm",
    "pwc": "consulting_firm",
    "kpmg": "consulting_firm",
    "accenture": "consulting_firm",
    "msg group": "consulting_firm",
    "msg systems": "consulting_firm",
    "ernst & young": "consulting_firm",
    "ernst and young": "consulting_firm",
    "bain": "consulting_firm",
    "bcg": "consulting_firm",
    "mckinsey": "consulting_firm",
    "exxeta": "consulting_firm",

    # Cloud Vendors
    "amazon web services": "cloud_vendor",
    "aws": "cloud_vendor",
    "microsoft azure": "cloud_vendor",
    "google cloud": "cloud_vendor",

    # Corporate (Versicherer, Banken, Unternehmen)
    "allianz": "corporate",
    "munich re": "corporate",
    "hannover re": "corporate",
    "axa": "corporate",
    "zurich": "corporate",
    "generali": "corporate",
    "deutsche bank": "corporate",
    "commerzbank": "corporate",

    # Industry
    "gdv": "industry_association",
    "bitkom": "industry_association",

    # Research
    "whitepaper": "research_institution",
    "study": "research_institution"
}


FILENAME_KEYWORDS = {
    "consulting_firm": ["deloitte", "pwc", "kpmg", "accenture", "exxeta"],
    "cloud_vendor": ["aws", "azure", "gcp"],
    "corporate": ["allianz", "munichre", "axa", "zurich"],
    "research_institution": ["whitepaper", "study", "report"]
}


# =========================================================
# 2. JURISDICTION DETECTION
# =========================================================

JURISDICTION_KEYWORDS = {
    "EU": [
        "eu",
        "european union",
        "verordnung",
        "regulation (eu)"
    ],
    "Germany": [
        "deutschland",
        "bundesrepublik",
        "bafin"
    ],
    "Switzerland": [
        "finma",
        "schweiz"
    ]
}


# =========================================================
# 3. DOCUMENT TYPE CORRECTIONS
# =========================================================

DOCUMENT_TYPE_CORRECTIONS = [
    {
        "if": {
            "origin": "supervisory_authority",
            "document_type": "regulatory_text"
        },
        "then": {
            "document_type": "supervisory_guidance"
        }
    },
    {
        "if": {
            "origin": "consulting_firm",
            "document_type": "regulatory_text"
        },
        "then": {
            "document_type": "consulting_framework"
        }
    },
    {
        "if": {
            "origin": "corporate",
            "document_type": "vendor_marketing"
        },
        "then": {
            "document_type": "blog_article"
        }
    }
]


# =========================================================
# 4. DOMAIN CLASSIFICATION
# =========================================================

DOMAIN_KEYWORDS = {
    "insurance_domain": [
        "versicherung",
        "insurance",
        "financial",
        "finanz",
        "bank",
        "regulation",
        "dora",
        "solvency",
        "risk management"
    ],
    "cloud_technology": [
        "cloud",
        "infrastructure",
        "devops",
        "aws",
        "azure",
        "gcp"
    ],
    "ai_genai_agentic": [
        "ai",
        "artificial intelligence",
        "llm",
        "generative ai",
        "machine learning"
    ]
}


# =========================================================
# 5. DOMAIN PRIORITY
# =========================================================

DOMAIN_PRIORITY = [
    "insurance_domain",
    "cloud_technology",
    "ai_genai_agentic"
]


# =========================================================
# 6. DOMAIN LAYER → DOMAIN MAPPING
# =========================================================

DOMAIN_LAYER_MAPPING = [
    {
        "if": {
            "domain_layer": "regulation"
        },
        "then": "insurance_domain"
    }
]


# =========================================================
# 7. ANTI-MISC CONTROL
# =========================================================

ENABLE_ANTI_MISC = True
ANTI_MISC_FALLBACK_DOMAIN = "insurance_domain"


# =========================================================
# 8. CONFIDENCE RULES
# =========================================================

CONFIDENCE_RULES = [
    {
        "if": {"origin": "legislator"},
        "min_confidence": 0.9
    },
    {
        "if": {"document_type": "regulatory_text"},
        "min_confidence": 0.85
    }
]


# =========================================================
# 9. FIELD PRIORITY (CORE GOVERNANCE MECHANISM)
# =========================================================

FIELD_PRIORITY = {
    "origin": [
        "preview_rule",
        "filename_rule",
        "llm"
    ],
    "jurisdiction": [
        "rule_based",
        "llm"
    ],
    "knowledge_domain": [
        "rule_based",
        "llm"
    ]
}


# =========================================================
# 10. FEATURE SWITCHES
# =========================================================

ENABLE_ORIGIN_RULES = True
ENABLE_JURISDICTION_RULES = True
ENABLE_DOCUMENT_TYPE_RULES = True
ENABLE_DOMAIN_RULES = True
ENABLE_CONFIDENCE_RULES = True
ENABLE_ANTI_MISC = True


# =========================================================
# 11. LLM DOMAIN NORMALIZATION
# Mappt ungültige LLM-Ausgaben auf gültige Taxonomy-Werte.
# Claude verwendet präzise Topic-Begriffe die nicht in
# KNOWLEDGE_DOMAINS stehen — diese werden hier korrigiert.
# =========================================================

LLM_DOMAIN_NORMALIZATION = {
    # Cloud-Topics → cloud_technology
    "cloud_governance":     "cloud_technology",
    "cloud_architecture":   "cloud_technology",
    "cloud_security":       "cloud_technology",
    "sovereign_cloud":      "cloud_technology",
    "cloud_infrastructure": "cloud_technology",

    # Insurance-Topics → insurance_domain
    "insurance_business":   "insurance_domain",
    "insurance_regulation": "insurance_domain",
    "financial_regulation": "insurance_domain",

    # AI-Topics → ai_genai_agentic
    "generative_ai":        "ai_genai_agentic",
    "agentic_ai":           "ai_genai_agentic",

    # Advisory → trusted_advisor
    "advisory_methods":     "trusted_advisor",
}