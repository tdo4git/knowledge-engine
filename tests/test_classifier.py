from knowledge_construction.metadata.classifier import classify_document


# ------------------------------------------------
# Dummy LLM
# ------------------------------------------------

class DummyLLM:

    def run(self, prompt, temperature=0.0, max_tokens=400):

        return """
        {
          "document_type": "industry_position",
          "domain_layer": "transformation_strategy",
          "knowledge_domain": "cloud_technology",
          "origin": "consulting_firm",
          "jurisdiction": "Global",
          "confidence": 0.8
        }
        """


# ------------------------------------------------
# Test
# ------------------------------------------------

dummy_llm = DummyLLM()

result = classify_document(
    title="Cloud transformation strategy for insurers",
    preview_text="This report discusses cloud adoption and modernization strategies.",
    llm_client=dummy_llm
)

print(result)