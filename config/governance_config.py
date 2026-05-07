# =========================================================
# governance_config.py
# Single Source of Truth für alle Governance-Regeln.
# Änderungen hier wirken sich auf alle Dokumente aus.
#
# Änderungen 2026-05-06 (TD-007 Ursachenbehebung):
#   - FILENAME_KEYWORDS["research_institution"]: generische
#     Formatbegriffe entfernt ("studie", "study", "report",
#     "whitepaper"). Dokumentformat ≠ Author-Origin.
#   - DOCUMENT_TYPE_CORRECTIONS: fehlende Regeln ergänzt für
#     supervisory_authority, consulting_firm, software_vendor,
#     cloud_vendor. Supervisory-Regeln setzen jetzt auch
#     domain_layer="regulation" (Cross-Field-Validation Fix).
#   - LLM_DOMAIN_NORMALIZATION: "transformation_strategy"
#     ergänzt (Classifier-Normalization vor validate_enums).
#
# Änderungen 2026-05-07:
#   - DOCUMENT_TYPE_CORRECTIONS: zwei fehlende Regeln ergänzt:
#     consulting_firm + vendor_marketing → consulting_framework
#     internal + vendor_marketing → internal_strategy
#     Ursache: LLM klassifiziert Whitepapers/Präsentationen
#     gelegentlich als vendor_marketing — Governance korrigiert.
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
    "exxeta":                               "consulting_firm",
    "capgemini":                            "consulting_firm",
    "bearingpoint":                         "consulting_firm",
    "bearing point":                        "consulting_firm",
    "msg":                                  "consulting_firm",
    "msg group":                            "consulting_firm",
    "msg systems":                          "consulting_firm",
    "oliver wyman":                         "consulting_firm",
    "mckinsey":                             "consulting_firm",
    "boston consulting":                    "consulting_firm",
    "bcg":                                  "consulting_firm",
    "roland berger":                        "consulting_firm",
    "ey":                                   "consulting_firm",
    "ernst & young":                        "consulting_firm",
    "ernst and young":                      "consulting_firm",

    # --------------------------------------------------
    # Research Institutions
    # --------------------------------------------------
    "oecd":                                 "research_institution",
    "lünendonk":                            "research_institution",
    "luenendonk":                           "research_institution",
    "trendzowl":                            "research_institution",
    "fraunhofer":                           "research_institution",
    "gartner":                              "research_institution",
    "forrester":                            "research_institution",

    # --------------------------------------------------
    # Cloud Vendors
    # --------------------------------------------------
    "amazon web services":                  "cloud_vendor",
    "aws":                                  "cloud_vendor",
    "microsoft azure":                      "cloud_vendor",
    "google cloud":                         "cloud_vendor",
    "google cloud platform":                "cloud_vendor",

    # --------------------------------------------------
    # Software Vendors
    # --------------------------------------------------
    "sap":                                  "software_vendor",
    "salesforce":                           "software_vendor",
    "servicenow":                           "software_vendor",
    "confluent":                            "software_vendor",
    "databricks":                           "software_vendor",
    "snowflake":                            "software_vendor",
    "heise":                                "software_vendor",

    # --------------------------------------------------
    # Industry Associations
    # --------------------------------------------------
    "gdv":                                  "industry_association",
    "gesamtverband der deutschen versicherungswirtschaft": "industry_association",
    "bitkom":                               "industry_association",
    "beltios":                              "industry_association",

    # --------------------------------------------------
    # Internal (conet)
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
        "msg",
    ],

    # --------------------------------------------------
    # FIX TD-007: Generische Formatbegriffe entfernt.
    # "studie", "study", "report", "whitepaper" beschreiben
    # die Dokumentform, nicht den Author.
    # Beispiel: ein GDV-Whitepaper ist industry_association,
    # kein research_institution — aber "whitepaper" im
    # Dateinamen hat research_institution mit filename_rule-
    # Priorität gesetzt und den korrekten AUTHOR_ORIGIN_MAP-
    # Match für "gdv" / "beltios" überschrieben.
    # --------------------------------------------------
    "research_institution": [
        "luenendonk",
        "lünendonk",
        "trendzowl",
        "oecd",
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
#
# Logik: origin + LLM-document_type → korrekter document_type
#
# Prinzip: Der LLM klassifiziert nach Inhalt und Form.
# Die Governance korrigiert nach Author-Origin, weil Origin
# stärker ist als die inhaltliche Formeinschätzung des LLM.
# Ein BaFin-Dokument ist supervisory_guidance — unabhängig
# davon ob der LLM es als research_report einschätzt.
#
# FIX TD-007: Fehlende Regeln ergänzt.
# Bisher nur *_regulatory_text → * abgedeckt.
# Jetzt vollständige Abdeckung aller relevanten LLM-Typen
# pro Origin-Kategorie.
#
# FIX Cross-Field-Validation:
# Supervisory-Regeln setzen domain_layer="regulation" mit,
# da cross_field_rules.py Rule 6 erfordert dass
# supervisory_guidance immer domain_layer=regulation hat.
# Semantik: wenn wir eine Behörde-Publikation als
# supervisory_guidance einstufen, ist sie per Definition
# normativ → regulation layer.
# =========================================================

DOCUMENT_TYPE_CORRECTIONS = [

    # --------------------------------------------------
    # supervisory_authority
    # BaFin, EBA, EIOPA etc. → immer supervisory_guidance
    # + domain_layer=regulation (Cross-Field-Validation)
    # --------------------------------------------------
    {
        "if": {"origin": "supervisory_authority", "document_type": "regulatory_text"},
        "then": {"document_type": "supervisory_guidance", "domain_layer": "regulation"}
    },
    {
        "if": {"origin": "supervisory_authority", "document_type": "research_report"},
        "then": {"document_type": "supervisory_guidance", "domain_layer": "regulation"}
    },
    {
        "if": {"origin": "supervisory_authority", "document_type": "expert_opinion"},
        "then": {"document_type": "supervisory_guidance", "domain_layer": "regulation"}
    },

    # --------------------------------------------------
    # consulting_firm
    # Beratungsunternehmen → immer consulting_framework
    # --------------------------------------------------
    {
        "if": {"origin": "consulting_firm", "document_type": "regulatory_text"},
        "then": {"document_type": "consulting_framework"}
    },
    {
        "if": {"origin": "consulting_firm", "document_type": "research_report"},
        "then": {"document_type": "consulting_framework"}
    },
    {
        "if": {"origin": "consulting_firm", "document_type": "blog_article"},
        "then": {"document_type": "consulting_framework"}
    },
    # FIX 2026-05-07: LLM klassifiziert Consulting-Whitepapers
    # gelegentlich als vendor_marketing — Governance korrigiert.
    {
        "if": {"origin": "consulting_firm", "document_type": "vendor_marketing"},
        "then": {"document_type": "consulting_framework"}
    },

    # --------------------------------------------------
    # software_vendor
    # Software-Anbieter → immer vendor_marketing
    # --------------------------------------------------
    {
        "if": {"origin": "software_vendor", "document_type": "research_report"},
        "then": {"document_type": "vendor_marketing"}
    },
    {
        "if": {"origin": "software_vendor", "document_type": "blog_article"},
        "then": {"document_type": "vendor_marketing"}
    },

    # --------------------------------------------------
    # cloud_vendor
    # Cloud-Anbieter → immer vendor_marketing
    # --------------------------------------------------
    {
        "if": {"origin": "cloud_vendor", "document_type": "research_report"},
        "then": {"document_type": "vendor_marketing"}
    },
    {
        "if": {"origin": "cloud_vendor", "document_type": "blog_article"},
        "then": {"document_type": "vendor_marketing"}
    },

    # --------------------------------------------------
    # corporate
    # Unternehmen → kein vendor_marketing (das ist für Anbieter)
    # --------------------------------------------------
    {
        "if": {"origin": "corporate", "document_type": "vendor_marketing"},
        "then": {"document_type": "blog_article"}
    },

    # --------------------------------------------------
    # internal
    # Interne Dokumente (conet) → immer internal_strategy
    # FIX 2026-05-07: LLM klassifiziert Unternehmenspräsentationen
    # gelegentlich als vendor_marketing — Governance korrigiert.
    # --------------------------------------------------
    {
        "if": {"origin": "internal", "document_type": "vendor_marketing"},
        "then": {"document_type": "internal_strategy"}
    },
    {
        "if": {"origin": "internal", "document_type": "blog_article"},
        "then": {"document_type": "internal_strategy"}
    },
    {
        "if": {"origin": "internal", "document_type": "research_report"},
        "then": {"document_type": "internal_strategy"}
    },

    # --------------------------------------------------
    # media
    # Presseartikel → immer press_article
    # --------------------------------------------------
    {
        "if": {"origin": "media", "document_type": "blog_article"},
        "then": {"document_type": "press_article"}
    },
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
# 9. LLM DOMAIN NORMALIZATION
#
# Mappt LLM-Ausgaben auf gültige KNOWLEDGE_DOMAINS.
# Wird in classifier.py VOR validate_enums angewendet.
# =========================================================

LLM_DOMAIN_NORMALIZATION = {
    "digital_transformation":       "ai_genai_agentic",
    "transformation_strategy":      "ai_genai_agentic",
    "data_analytics":               "ai_genai_agentic",
    "cybersecurity":                "insurance_domain",
    "risk_management":              "insurance_domain",
    "compliance":                   "insurance_domain",
    "regulatory_compliance":        "insurance_domain",
    "financial_services":           "insurance_domain",
    "portfolio_gtm":                "insurance_domain",
}


# =========================================================
# 10. DOMAIN RULES ENABLED
# =========================================================

ENABLE_DOMAIN_RULES = True