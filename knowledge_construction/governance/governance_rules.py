from pathlib import Path

from config import governance_config


# ------------------------------------------------
# SAFE CONFIG ACCESS
# ------------------------------------------------
FIELD_PRIORITY = getattr(governance_config, "FIELD_PRIORITY", {})
AUTHOR_ORIGIN_MAP = getattr(governance_config, "AUTHOR_ORIGIN_MAP", {})
FILENAME_KEYWORDS = getattr(governance_config, "FILENAME_KEYWORDS", {})
JURISDICTION_KEYWORDS = getattr(governance_config, "JURISDICTION_KEYWORDS", {})
DOCUMENT_TYPE_CORRECTIONS = getattr(governance_config, "DOCUMENT_TYPE_CORRECTIONS", [])

DOMAIN_KEYWORDS = getattr(governance_config, "DOMAIN_KEYWORDS", {})
DOMAIN_PRIORITY = getattr(governance_config, "DOMAIN_PRIORITY", [])
DOMAIN_LAYER_MAPPING = getattr(governance_config, "DOMAIN_LAYER_MAPPING", [])

ENABLE_DOMAIN_RULES = getattr(governance_config, "ENABLE_DOMAIN_RULES", True)
ENABLE_ANTI_MISC = getattr(governance_config, "ENABLE_ANTI_MISC", True)
ANTI_MISC_FALLBACK_DOMAIN = getattr(governance_config, "ANTI_MISC_FALLBACK_DOMAIN", "insurance_domain")

LLM_DOMAIN_NORMALIZATION = getattr(governance_config, "LLM_DOMAIN_NORMALIZATION", {})

# ------------------------------------------------
# ORIGIN PRIORITY — vollständige Liste aller Origins
# Reihenfolge bestimmt welche Origin bevorzugt wird
# wenn mehrere Regeln matchen.
# ------------------------------------------------
ORIGIN_PRIORITY = [
    "legislator",
    "supervisory_authority",
    "consulting_firm",
    "industry_association",
    "research_institution",
    "cloud_vendor",
    "software_vendor",
    "corporate",
    "media",          # niedrigste Prio — journalistisch, nicht autoritativ
]


# ------------------------------------------------
# LLM DOMAIN NORMALIZATION
# ------------------------------------------------
def _normalize_llm_domain(result):
    current = result.get("knowledge_domain")
    if current and current in LLM_DOMAIN_NORMALIZATION:
        normalized = LLM_DOMAIN_NORMALIZATION[current]
        result["knowledge_domain"] = normalized
        result["knowledge_domain_source"] = "normalization"
        print(f"  ↳ Domain normalization: {current} → {normalized}")


# ------------------------------------------------
# PRIORITY HANDLING
# ------------------------------------------------
def _set_with_priority(result, field, value, source):

    current_source = result.get(f"{field}_source")

    if not current_source:
        result[field] = value
        result[f"{field}_source"] = source
        return

    priority = FIELD_PRIORITY.get(field, [])

    if not priority:
        result[field] = value
        result[f"{field}_source"] = source
        return

    if source not in priority:
        result[field] = value
        result[f"{field}_source"] = source
        return

    if current_source not in priority:
        result[field] = value
        result[f"{field}_source"] = source
        return

    if priority.index(source) < priority.index(current_source):
        result[field] = value
        result[f"{field}_source"] = source


# ------------------------------------------------
# ORIGIN DETECTION
#
# FIX: Preview-Text wird NICHT für Origin-Detection
# verwendet. Origin = wer hat das Dokument geschrieben,
# erkennbar an Titel und Dateiname — nicht am Inhalt.
# Ein heise-Whitepaper das BaFin erwähnt, ist trotzdem
# von heise, nicht von BaFin.
# ------------------------------------------------
def _apply_origin(result, title, preview_text, file_path: Path):

    text = title.lower()                    # ← nur Titel, kein Preview-Text
    filename = str(file_path).lower()
    combined = f"{text} {filename}"

    matches = []

    for key, origin in AUTHOR_ORIGIN_MAP.items():
        if key in combined:
            matches.append(origin)

    if not matches:
        _set_with_priority(result, "origin", result.get("origin", "unknown"), "llm")
        return

    for preferred in ORIGIN_PRIORITY:
        if preferred in matches:
            _set_with_priority(result, "origin", preferred, "preview_rule")
            return


# ------------------------------------------------
# FILENAME RULES
# ------------------------------------------------
def _apply_filename_rules(result, file_path: Path):

    filename = str(file_path).lower()

    for origin, keywords in FILENAME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in filename:
                _set_with_priority(result, "origin", origin, "filename_rule")
                return


# ------------------------------------------------
# JURISDICTION
# ------------------------------------------------
def _apply_jurisdiction(result, title, preview_text):

    text = f"{title} {preview_text}".lower()

    for jurisdiction, keywords in JURISDICTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                _set_with_priority(result, "jurisdiction", jurisdiction, "rule_based")
                return


# ------------------------------------------------
# DOMAIN DETECTION
# ------------------------------------------------
def _apply_knowledge_domain(result, title, preview_text):

    if not ENABLE_DOMAIN_RULES:
        return

    text = f"{title} {preview_text}".lower()

    matches = set()

    for domain, keywords in DOMAIN_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                matches.add(domain)

    if not matches:
        return

    for preferred in DOMAIN_PRIORITY:
        if preferred in matches:
            _set_with_priority(result, "knowledge_domain", preferred, "rule_based")
            return


# ------------------------------------------------
# DOMAIN LAYER MAPPING
# ------------------------------------------------
def _apply_domain_layer_mapping(result):

    for rule in DOMAIN_LAYER_MAPPING:
        conditions = rule.get("if", {})

        if all(result.get(k) == v for k, v in conditions.items()):
            _set_with_priority(
                result,
                "knowledge_domain",
                rule["then"],
                "rule_based"
            )


# ------------------------------------------------
# ANTI-MISC CONTROL
# ------------------------------------------------
def _apply_anti_misc(result):

    if not ENABLE_ANTI_MISC:
        return

    if result.get("knowledge_domain") == "misc":
        result["knowledge_domain"] = ANTI_MISC_FALLBACK_DOMAIN


# ------------------------------------------------
# DOCUMENT TYPE CORRECTIONS
# ------------------------------------------------
def _apply_document_type_corrections(result):

    for rule in DOCUMENT_TYPE_CORRECTIONS:
        conditions = rule.get("if", {})
        match = all(result.get(k) == v for k, v in conditions.items())

        if match:
            for field, value in rule.get("then", {}).items():
                _set_with_priority(result, field, value, "rule_based")


# ------------------------------------------------
# MAIN ENTRY
# ------------------------------------------------
def apply_governance(result, title, preview_text, file_path: Path):

    # Schritt 0: LLM-Ausgaben normalisieren
    _normalize_llm_domain(result)

    _apply_filename_rules(result, file_path)
    _apply_origin(result, title, preview_text, file_path)
    _apply_jurisdiction(result, title, preview_text)

    _apply_knowledge_domain(result, title, preview_text)
    _apply_domain_layer_mapping(result)
    _apply_anti_misc(result)

    _apply_document_type_corrections(result)

    return result