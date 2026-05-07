"""
Engine Configuration
Strategic Knowledge Engine
"""

# ---------------------------------------------------
# Retrieval Configuration
# ---------------------------------------------------

RETRIEVAL_CONFIG = {

    # Anzahl der Kandidaten aus der Vektor-Suche
    "vector_top_k": 100,

    # Document Aggregation
    "document_aggregation": {

        # wie viele der besten Chunks pro Dokument
        # zur Score-Bildung verwendet werden
        "top_k_chunks": 3

    },

    # Context Construction (später genutzt)
    "context_construction": {

        # maximale Dokumente im Kontext
        "max_documents": 5,

        # maximale Chunks pro Dokument
        "max_chunks_per_document": 2
    }
}
