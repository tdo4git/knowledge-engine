from pathlib import Path

from knowledge_construction.onboarding_pipeline import OnboardingPipeline, REVIEW_REPORT_PATH
from knowledge_construction.llm.llm_client import LLMClient


def run_onboarding():

    intake_dir = Path("knowledge_sources/intake")

    pipeline = OnboardingPipeline(
        registry_path="knowledge_base/registry/document_registry.json",
        llm_client=LLMClient()
    )

    files = [f for f in intake_dir.glob("*") if f.is_file()]

    if not files:
        print("No files in intake.")
        return

    print(f"Found {len(files)} files in intake.\n")

    processed = 0
    errors = 0

    for file_path in files:

        print(f"Processing: {file_path.name}")

        try:
            pipeline.process_document(str(file_path))
            processed += 1

        except Exception as e:
            print(f"ERROR processing {file_path.name}: {e}\n")
            print(f"⚠ Document remains in intake: {file_path.name}\n")
            errors += 1

    # -------------------------------------------------
    # Review Report schreiben + anzeigen
    # -------------------------------------------------

    pipeline.write_review_report()

    print("\n===================================")
    print(f"Processed: {processed}")
    print(f"Errors:    {errors}")
    print("===================================\n")

    if REVIEW_REPORT_PATH.exists():
        print("--- REVIEW REPORT ---")
        print(REVIEW_REPORT_PATH.read_text(encoding="utf-8"))
        print(f"(Saved: {REVIEW_REPORT_PATH})")


if __name__ == "__main__":
    run_onboarding()