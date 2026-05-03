from pathlib import Path
from knowledge_construction.metadata.preview_extractor import extract_preview

preview = extract_preview(
    Path("knowledge_sources/archive/bafin_cloud_outsourcing_2024.pdf")
)

print(preview[:500])