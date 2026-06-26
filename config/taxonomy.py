DOCUMENT_TYPES = [
    "regulatory_text",        # Gesetz / Verordnung (DORA etc.)
    "supervisory_guidance",   # BaFin, EBA Guidelines
    "industry_position",      # Verbände
    "expert_opinion",         # Fachartikel
    "consulting_framework",   # Beratungsansätze
    "research_report",        # Studien
    "vendor_marketing",       # Anbieter-Marketing
    "blog_article",           # Blog / LinkedIn
    "press_article",          # Zeitungsartikel / journalistischer Onlineartikel
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
    "software_architecture",    # neu 2026-05-24
    "leadership_management",    # neu 2026-05-24
    "politics_society",         # neu 2026-05-24
    "misc"
]

TOPICS = [
    # Cloud
    "cloud_governance",
    "cloud_architecture",
    "cloud_security",
    "sovereign_cloud",
    # Insurance
    "insurance_business",
    # Strategy / Advisory
    "transformation_strategy",
    "advisory_methods",
    # Market
    "vendor_landscape",
    "market_analysis",
    # Software Architecture (neu 2026-05-24)
    "software_design",
    "system_architecture",
    "engineering_practices",
    # Leadership & Management (neu 2026-05-24)
    "leadership",
    "team_management",
    "organizational_development",
    # Politics & Society (neu 2026-05-24)
    "politics",
    "public_policy",
    "society_technology",
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
    "media",                   # Presse, Zeitungen, Onlinemedien
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