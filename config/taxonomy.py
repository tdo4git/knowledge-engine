DOCUMENT_TYPES = [
    "regulatory_text",        # Gesetz / Verordnung (DORA etc.)
    "supervisory_guidance",   # BaFin, EBA Guidelines
    "industry_position",      # Verbände
    "expert_opinion",         # Fachartikel
    "consulting_framework",   # Beratungsansätze
    "research_report",        # Studien
    "vendor_marketing",       # Anbieter-Marketing
    "blog_article",           # Blog / LinkedIn
    "internal_strategy",      # interne Dokumente
    "unknown"
]

DOMAIN_LAYERS = [
    "regulation",     # regulatorisch / normativ
    "business",       # Fachprozesse Versicherung
    "technology",     # IT / Architektur
    "strategy",       # Transformation / Zielbild
    "market"          # Wettbewerb / Anbieter
]

KNOWLEDGE_DOMAINS = [
    "trusted_advisor",
    "insurance_domain",
    "cloud_technology",
    "portfolio_gtm",
    "ai_genai_agentic",
    "misc"
]

TOPICS = [
    "cloud_governance",
    "cloud_architecture",
    "cloud_security",
    "sovereign_cloud",
    "insurance_business",
    "transformation_strategy",
    "vendor_landscape",
    "advisory_methods",
    "market_analysis"
]

ORIGINS = [
    "supervisory_authority",   # BaFin, EBA
    "legislator",              # EU Gesetzgeber
    "industry_association",    # GDV etc.
    "consulting_firm",
    "research_institution",
    "cloud_vendor",
    "software_vendor",
    "corporate",               # Unternehmen (Versicherer, Banken etc.)
    "internal",
    "unknown"
]

JURISDICTIONS = [
    "EU",
    "Germany",
    "Switzerland",
    "UK",
    "Global",
    "unknown"
]

BIAS_LEVELS = {
    "very_low",
    "low",
    "medium",
    "high",
    "elevated"
}