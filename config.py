"""
Zentrale Konfiguration — Single Source of Truth.
Alle Pfade, Namen, Parameter an EINER Stelle.
"""


class Config:
    # ChromaDB
    DB_PATH = "./faq_database"
    COLLECTION_NAME = "faq"

    # Search
    DEFAULT_QUERY = "I forgot my password"
    DEFAULT_TOP_K = 3
    MAX_TOP_K = 10

    # OpenAI
    LLM_MODEL = "gpt-4o-mini"
    MAX_TOKENS = 500

    # FastAPI
    API_TITLE = "FAQ Search API"
    API_DESCRIPTION = "Semantic search over FAQ entries using ChromaDB."
    API_VERSION = "1.0.0"
    API_PORT = 8000

    # Gradio
    GRADIO_PORT = 7860

    # wandb
    WANDB_PROJECT = "ki-capstone"
