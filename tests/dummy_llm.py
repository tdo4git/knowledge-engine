class DummyLLM:

    def generate(self, prompt: str) -> str:
        return self.run(prompt)

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