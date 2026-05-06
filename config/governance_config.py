# =========================================================
# governance_config.py
# Single Source of Truth für alle Governance-Regeln.
# Änderungen hier wirken sich auf alle Dokumente aus.
# =========================================================


# =========================================================
# FIELD PRIORITY
# Bestimmt welche Quelle bei Konflikten gewinnt.
# Niedrigerer Index = höhere Priorität.
# =========================================================

FIELD_PRIORITY = {
    "origin": [
        "filename_rule",    # Dateiname ist stärkstes Signal
        "preview_rule",     # Titel/Author-Match
        "llm",              # LLM-Klassifikation als Fallback
    ],
    "jurisdiction": [
        "preview_rule",
        "llm",
    ],
    "knowledge_domain": [
        "domain_rule",
        "llm",
    ],
}


# =========================================================
# 1. ORIGIN DETECTION
# =========================================================

AUTHOR_ORIGIN_MAP = {

    # --------------------------------------------------
    # Legislator
    # --------------------------------------------------
    "europäische union":                    "legislator",
    "european parliament":                  "legislator",
    "rat der europäischen union":           "legislator",
    "european commission":                  "legislator",

    # --------------------------------------------------
    # Supervisory Authority
    # --------------------------------------------------
    "eba":                                  "supervisory_authority",
    "eiopa":                                "supervisory_authority",
    "bafin":                                "supervisory_authority",
    "finma":                                "supervisory_authority",
    "fca":                                  "supervisory_authority",

    # --------------------------------------------------
    # Consulting Firms
    # --------------------------------------------------
    "deloitte":                             "consulting_firm",
    "pwc":                                  "consulting_firm",
    "adesso":                               "consulting_firm",
    "kpmg":                                 "consulting_firm",
    "accenture":                            "consulting_firm",
    "msg group":                            "consulting_firm",
    "msg systems":                          "consulting_firm",
    "ernst & young":                        "consulting_firm",
    "ernst and young":                      "consulting_firm",
    "bain":                                 "consulting_firm",
    "bcg":                                  "consulting_firm",
    "mckinsey":                             "consulting_firm",
    "exxeta":                               "consulting_firm",
    "capgemini":                            "consulting_firm",
    "bearingpoint":                         "consulting_firm",
    "bearing point":                        "consulting_firm",
    "oliver wyman":                         "consulting_firm",
    "roland berger":                        "consulting_firm",
    "zeb":                                  "consulting_firm",

    # --------------------------------------------------
    # Research Institutions
    # --------------------------------------------------
    "lünendonk":                            "research_institution",
    "luenendonk":                           "research_institution",
    "trendzowl":                            "research_institution",
    "fraunhofer":                           "research_institution",
    "bitkom research":                      "research_institution",
    "oecd":                                 "research_institution",

    # --------------------------------------------------
    # Cloud Vendors
    # --------------------------------------------------
    "amazon web services":                  "cloud_vendor",
    "aws":                                  "cloud_vendor",
    "microsoft azure":                      "cloud_vendor",
    "google cloud":                         "cloud_vendor",

    # --------------------------------------------------
    # Software Vendors
    # --------------------------------------------------
    "heise":                                "software_vendor",
    "heise academy":                        "software_vendor",
    "amber":                                "software_vendor",

    # --------------------------------------------------
    # Industry Associations
    # --------------------------------------------------
    "gdv":                                  "industry_association",
    "bitkom":                               "industry_association",
    "beltios":                              "industry_association",
    "gesamtverband der deutschen versicherungswirtschaft": "industry_association",

    # --------------------------------------------------
    # Internal (conet-eigene Dokumente)
    # Vor corporate — verhindert dass "allianz" im
    # Titel die interne Origin überschreibt.
    # --------------------------------------------------
    "conet":                                "internal",
    "conet deutschland":                    "internal",
    "conet deutschland gmbh":              "internal",
    "conet group":                          "internal",

    # --------------------------------------------------
    # Corporate (Versicherer, Banken, Unternehmen)
    # --------------------------------------------------
    "allianz":                              "corporate",
    "munich re":                            "corporate",
    "hannover re":                          "corporate",
    "axa":                                  "corporate",
    "zurich":                               "corporate",
    "generali":                             "corporate",
    "deutsche bank":                        "corporate",
    "commerzbank":                          "corporate",
    "ergo":                                 "corporate",
    "talanx":                               "corporate",
    "swiss re":                             "corporate",
    "signal iduna":                         "corporate",
    "huk-coburg":                           "corporate",
    "r+v":                                  "corporate",

    # --------------------------------------------------
    # Media (Presse, Zeitungen, Onlinemedien)
    # --------------------------------------------------
    "süddeutsche zeitung":                  "media",
    "sueddeutsche zeitung":                 "media",
    "süddeutsche":                          "media",
    "frankfurter allgemeine":               "media",
    "handelsblatt":                         "media",
    "der spiegel":                          "media",
    "manager magazin":                      "media",
    "wirtschaftswoche":                     "media",
    "versicherungsjournal":                 "media",
    "pfefferminzia":                        "media",
}


FILENAME_KEYWORDS = {

    "supervisory_authority": [
        "bafin",
        "eiopa",
        "eba",
        "finma",
    ],

    "legislator": [
        "dora verordnung",
        "regulation eu",
    ],

    "consulting_firm": [
        "deloitte",
        "pwc",
        "kpmg",
        "accenture",
        "exxeta",
        "capgemini",
        "bearingpoint",
        "playbook",
    ],

    "research_institution": [
        "luenendonk",
        "lünendonk",
        "trendzowl",
        "oecd",
        "studie",
        "study",
        "report",
        "whitepaper",
    ],

    "cloud_vendor": [
        "aws",
        "azure",
        "gcp",
    ],

    "software_vendor": [
        "heise",
        "amber",
    ],

    "industry_association": [
        "gdv",
        "beltios",
        "bitkom",
    ],

    # --------------------------------------------------
    # Internal VOR corporate — kritisch für korrekte
    # Priorität bei Dateinamen wie:
    #   conet_rfp_allianz_2026.docx
    # "conet" muss vor "allianz" greifen.
    # --------------------------------------------------
    "internal": [
        "conet",
    ],

    "corporate": [
        "allianz",
        "munichre",
        "munich re",
        "axa",
        "zurich",
        "ergo",
        "talanx",
        "rv",
    ],

    "media": [
        "sueddeutsche",
        "handelsblatt",
        "spiegel",
        "wirtschaftswoche",
        "versicherungsjournal",
        "pfefferminzia",
    ],
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
    },
    {
        "if": {
            "origin": "media",
            "document_type": "blog_article"
        },
        "then": {
            "document_type": "press_article"
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
# 9. FEATURE SWITCHES
# =========================================================

ENABLE_ORIGIN_RULES = True
ENABLE_JURISDICTION_RULES = True
ENABLE_DOCUMENT_TYPE_RULES = True
ENABLE_DOMAIN_RULES = True
ENABLE_CONFIDENCE_RULES = True
ENABLE_ANTI_MISC = True


# =========================================================
# 10. LLM DOMAIN NORMALIZATION
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