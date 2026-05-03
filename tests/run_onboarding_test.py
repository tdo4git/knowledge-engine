import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from knowledge_construction.onboarding_pipeline import OnboardingPipeline


class DummyLLM:

    def run(self, prompt, **kwargs):
        return """
{
  "document_type": "regulatory_text",
  "domain_layer": "regulation",
  "knowledge_domain": "trusted_advisor",
  "origin": "legislator",
  "jurisdiction": "EU",
  "confidence": 0.8
}
"""

pipeline = OnboardingPipeline(
    registry_path="knowledge_base/registry/document_registry.json",
    llm_client=DummyLLM()
)

pipeline.process_document(
    "knowledge_sources/intake/test_dora.txt"
)

print("✅ Dokument verarbeitet")