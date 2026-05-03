PREVIEW_MAX_CHARS = 6000

MAX_PDF_PAGES_PREVIEW = 5
DOCX_PARAGRAPH_PREVIEW = 80

CLASSIFIER_TEMPERATURE = 0.0
CLASSIFIER_MAX_TOKENS = 400

GOVERNANCE_REVIEW_TEMPERATURE = 0.0
GOVERNANCE_REVIEW_MAX_TOKENS = 600

CHUNKS_PATH = "knowledge_base/chunks/chunks.json"
CHUNK_SIZE = 600
CHUNK_OVERLAP = 80
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

EMBEDDINGS_PATH = "knowledge_base/vector_index/embeddings.pt"
FAISS_INDEX_PATH = "knowledge_base/vector_index/index.faiss"
CHUNK_IDS_PATH = "knowledge_base/vector_index/chunk_ids.json"

# ----------------------------------
# LLM Configuration
# ----------------------------------

LLM_MODEL = "claude-sonnet-4-6"
LLM_TEMPERATURE = 0.0
LLM_TIMEOUT = 30