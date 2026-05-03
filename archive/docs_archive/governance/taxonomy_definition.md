# Taxonomy Definition – Strategic Knowledge Engine

## Purpose

Defines the canonical classification schema used in the Knowledge Construction Pipeline.

---

## Dimensions

### Document Type

Defines the nature of the document:

- regulatory_text
- supervisory_guidance
- consulting_framework
- vendor_marketing
- ...

---

### Origin

Defines the source category:

- legislator
- supervisory_authority
- consulting_firm
- cloud_vendor
- ...

Important distinction:

legislator → creates laws  
supervisory_authority → issues guidance and supervision

---

### Domain Layer

Defines abstraction level:

- regulation
- business
- technology
- strategy
- market

---

### Knowledge Domain

Defines knowledge context:

- insurance_domain
- cloud_technology
- trusted_advisor
- ...

---

## Design Principles

- no overlapping categories
- stable and explainable values
- aligned with retrieval scoring

## Taxonomy Enforcement

The taxonomy is enforced via:

- Prompt Builder (LLM constraint)
- Validation layer (hard validation)

The LLM must only produce values defined in the taxonomy.

RULE:
Taxonomy is the single source of truth.
No implicit categories allowed.