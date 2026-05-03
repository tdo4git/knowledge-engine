from knowledge_construction.llm.llm_client import LLMClient


def test_llm():

    llm = LLMClient()

    prompt = """
Classify the following document:

Title: DORA regulation
Text: The Digital Operational Resilience Act defines requirements for ICT risk management in financial institutions.

Return JSON with:
- document_type
- domain_layer
- knowledge_domain
- origin
- jurisdiction
"""

    result = llm.run(prompt)

    print("\n--- LLM RESULT ---\n")
    print(result)


if __name__ == "__main__":
    test_llm()