from typing import Dict


# =========================================================
# CROSS-FIELD VALIDATION
# =========================================================

def validate_cross_field(result: Dict):
    """
    Validates semantic consistency between classification fields.

    Rules enforce domain logic beyond simple enum validation.

    Raises:
        ValueError if any rule is violated
    """

    doc_type = result.get("document_type")
    origin = result.get("origin")
    confidence = result.get("confidence")
    domain_layer = result.get("domain_layer")

    # -------------------------------------------------
    # 1. Regulatory texts → legislator
    # -------------------------------------------------

    if doc_type == "regulatory_text":
        if origin != "legislator":
            raise ValueError(
                f"Invalid combination: regulatory_text must originate from legislator (got: {origin})"
            )

    # -------------------------------------------------
    # 2. Supervisory guidance → supervisory authority
    # -------------------------------------------------

    if doc_type == "supervisory_guidance":
        if origin != "supervisory_authority":
            raise ValueError(
                f"Invalid combination: supervisory_guidance must originate from supervisory_authority (got: {origin})"
            )

    # -------------------------------------------------
    # 3. Vendor marketing → vendor only
    # -------------------------------------------------

    if doc_type == "vendor_marketing":
        if origin not in {"cloud_vendor", "software_vendor"}:
            raise ValueError(
                f"Invalid combination: vendor_marketing must originate from vendor (got: {origin})"
            )

    # -------------------------------------------------
    # 4. Vendors cannot produce regulatory content
    # -------------------------------------------------

    if origin in {"cloud_vendor", "software_vendor"}:
        if doc_type in {"regulatory_text", "supervisory_guidance"}:
            raise ValueError(
                f"Invalid combination: vendors cannot produce regulatory/supervisory documents (got: {doc_type})"
            )

    # -------------------------------------------------
    # 5. Supervisory authorities cannot produce marketing
    # -------------------------------------------------

    if origin == "supervisory_authority":
        if doc_type == "vendor_marketing":
            raise ValueError(
                "Invalid combination: supervisory_authority cannot produce marketing content"
            )

    # -------------------------------------------------
    # 6. Regulatory documents must belong to regulation layer
    # -------------------------------------------------

    if doc_type in {"regulatory_text", "supervisory_guidance"}:
        if domain_layer != "regulation":
            raise ValueError(
                f"Invalid domain_layer: {doc_type} must belong to 'regulation' (got: {domain_layer})"
            )