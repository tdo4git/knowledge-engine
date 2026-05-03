from typing import Dict, Any

from config.taxonomy import (
    DOCUMENT_TYPES,
    DOMAIN_LAYERS,
    KNOWLEDGE_DOMAINS,
    TOPICS,
    ORIGINS,
    JURISDICTIONS
)


# -------------------------------------------------
# Helper
# -------------------------------------------------

def _format_list(name: str, values: list) -> str:
    return f"{name}:\n" + "\n".join(f"- {v}" for v in values)


# -------------------------------------------------
# MAIN BUILDER
# -------------------------------------------------

def build_prompt(query: str, context: str, contract: Dict[str, Any]) -> Dict[str, str]:

    role = contract.get("role", {})
    policies = contract.get("policies", {})
    reasoning_rules = contract.get("reasoning_rules", {})
    output_rules = contract.get("output_rules", {})
    task = contract.get("task", {})

    system_parts = []

    # -------------------------------------------------
    # ROLE
    # -------------------------------------------------

    role_name = role.get("name", "Assistant")
    system_parts.append(f"You act as a {role_name}.")
    system_parts.append("Follow all governance rules strictly.")

    # -------------------------------------------------
    # TASK TYPE
    # -------------------------------------------------

    task_type = task.get("type")

    # =================================================
    # CLASSIFICATION
    # =================================================

    if task_type == "classification":

        system_parts.append("\nTask: Document Classification")

        system_parts.append(
            "Classify the document strictly according to the allowed taxonomy values."
        )

        # =============================================
        # ORIGIN DETECTION GUIDANCE (NEW)
        # =============================================

        system_parts.append("\n--- IMPORTANT: ORIGIN DETECTION ---")
        system_parts.append(
            "Identifying the ORIGIN (who created/published this document) is critical."
        )
        system_parts.append(
            "Look for the following signals (in order of reliability):"
        )
        system_parts.append(
            "1. AUTHOR/PUBLISHER NAME: BaFin, EBA, EU Commission → legislator/supervisory_authority"
        )
        system_parts.append(
            "2. COMPANY/ORG: Deloitte, PWC, Accenture, Exxeta → consulting_firm"
        )
        system_parts.append(
            "3. CLOUD VENDORS: AWS, Azure, Google Cloud → cloud_vendor"
        )
        system_parts.append(
            "4. INSURERS: Allianz, Munich Re, AXA → corporate"
        )
        system_parts.append(
            "5. INDUSTRY GROUPS: GDV, BITKOM → industry_association"
        )
        system_parts.append(
            "6. RESEARCH ORGS: Academic institutions, think tanks → research_institution"
        )
        system_parts.append(
            "7. If none match clearly, mark as 'unknown' and set lower confidence."
        )

        # =============================================
        # TAXONOMY (Single Source of Truth)
        # =============================================

        system_parts.append("\n--- ALLOWED VALUES ---")

        system_parts.append(_format_list("document_type", DOCUMENT_TYPES))
        system_parts.append(_format_list("domain_layer", DOMAIN_LAYERS))
        system_parts.append(_format_list("knowledge_domain", KNOWLEDGE_DOMAINS))
        system_parts.append(_format_list("topic", TOPICS))
        system_parts.append(_format_list("origin", ORIGINS))
        system_parts.append(_format_list("jurisdiction", JURISDICTIONS))

        # =============================================
        # CONFIDENCE GUIDANCE (NEW)
        # =============================================

        system_parts.append("\n--- CONFIDENCE ASSESSMENT ---")
        system_parts.append(
            "confidence: float between 0.0 and 1.0"
        )
        system_parts.append(
            "- 0.95+: Document clearly signals its origin/type (e.g., BaFin letterhead, regulatory text)"
        )
        system_parts.append(
            "- 0.85-0.94: Strong signals but some ambiguity"
        )
        system_parts.append(
            "- 0.75-0.84: Reasonable but not certain (will trigger review)"
        )
        system_parts.append(
            "- <0.75: Unclear or ambiguous (will trigger review)"
        )
        system_parts.append(
            "Be conservative: if unsure, lower the confidence."
        )

        # =============================================
        # RULES
        # =============================================

        rules = contract.get("rules", {})

        system_parts.append("\n--- RULES ---")

        if rules.get("strict_enum_usage", True):
            system_parts.append("- Use only the allowed values above.")

        if rules.get("no_synonyms", True):
            system_parts.append("- Do not use synonyms or variations.")

        if rules.get("no_explanations", True):
            system_parts.append("- Do not provide explanations.")

        if rules.get("output_format") == "json_only":
            system_parts.append("- Return valid JSON only.")

        # =============================================
        # OUTPUT SCHEMA
        # =============================================

        schema = contract.get("output_schema", {})
        required_fields = schema.get("required_fields", [])

        if required_fields:
            system_parts.append(
                f"- Output must contain exactly these fields: {', '.join(required_fields)}"
            )

    # =================================================
    # RETRIEVAL / ADVISORY (bestehendes MVP-Verhalten)
    # =================================================

    else:

        if policies:

            system_parts.append("\nGovernance Policies:")

            source_policy = policies.get("source_policy", {})
            if source_policy.get("use_only_provided_context"):
                system_parts.append("- Use only the provided context as factual basis.")
            if source_policy.get("citation_required"):
                system_parts.append("- Provide inline references to the source.")

            speculation_policy = policies.get("speculation_policy", {})
            if not speculation_policy.get("allow_speculation", True):
                system_parts.append("- Do not speculate.")
            if speculation_policy.get("uncertainty_must_be_explicit"):
                system_parts.append("- Explicitly state uncertainty.")

            compliance_policy = policies.get("compliance_policy", {})
            if compliance_policy.get("no_legal_advice"):
                system_parts.append("- Do not provide legal advice.")
            if compliance_policy.get("no_product_recommendation"):
                system_parts.append("- Do not recommend products or vendors.")

        if reasoning_rules:

            system_parts.append("\nReasoning Requirements:")

            evidence_rules = reasoning_rules.get("evidence_handling", {})
            if evidence_rules.get("derive_requirements_explicitly"):
                system_parts.append("- Derive requirements explicitly from evidence.")
            if evidence_rules.get("identify_legal_references_if_present"):
                system_parts.append("- Identify legal references if present.")
            if evidence_rules.get("do_not_repeat_evidence_text_verbatim"):
                system_parts.append("- Do not repeat evidence verbatim.")

            analytical_rules = reasoning_rules.get("analytical_depth", {})
            if analytical_rules.get("distinguish_between_definition_and_obligation"):
                system_parts.append("- Distinguish between definitions and obligations.")
            if analytical_rules.get("highlight_if_requirement_applies_to_critical_functions_only"):
                system_parts.append("- Highlight if requirements apply only to critical functions.")

        if output_rules:

            system_parts.append("\nOutput Requirements:")

            if output_rules.get("language") == "de":
                system_parts.append("- Respond in German.")

            structure = output_rules.get("structure", {})
            required_sections = structure.get("required_sections", [])
            if required_sections:
                system_parts.append(
                    f"- Structure the answer into: {', '.join(required_sections)}"
                )

            citations = output_rules.get("citations", {})
            if citations.get("inline_references_required"):
                system_parts.append("- Include inline references.")

            tone_rules = output_rules.get("tone", [])
            if tone_rules:
                system_parts.append(
                    f"- Maintain tone: {', '.join(tone_rules)}"
                )

    system_message = "\n".join(system_parts).strip()

    # -------------------------------------------------
    # USER MESSAGE
    # -------------------------------------------------

    if task_type == "classification":

        user_message = f"""
Document:
{context}

Classify this document according to the taxonomy and origin detection guidance above.
Output valid JSON only.
""".strip()

    else:

        user_message = f"""
Frage:
{query}

Evidenzbasis:
{context}

Erstelle eine strukturierte Analyse.
""".strip()

    return {
        "system": system_message,
        "user": user_message
    }