BIAS_BY_ORIGIN = {
    "legislator":           "very_low",    # TD-006 fix: war fälschlich "regulator"
    "supervisory_authority": "very_low",
    "industry_association": "low",
    "research_institution": "low",
    "consulting_firm":      "medium",
    "corporate":            "medium",      # Unternehmen — eigene Interessen
    "software_vendor":      "high",
    "cloud_vendor":         "high",
    "internal":             "medium",
    "unknown":              "elevated"
}


def derive_bias(origin: str) -> str:
    return BIAS_BY_ORIGIN.get(origin, "elevated")