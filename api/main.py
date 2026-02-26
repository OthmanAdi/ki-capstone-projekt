"""
SILVER: FastAPI Server
=======================
REST API für die FAQ-Suche.

Starten: uvicorn api.main:app --reload --port 8000
Docs:    http://localhost:8000/docs
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

# TODO: FastAPI, HTTPException, BaseModel, chromadb importieren


# TODO: FastAPI App erstellen
#   app = FastAPI(title=Config.API_TITLE, version=Config.API_VERSION)

# TODO: ChromaDB Client + Collection laden
#   Warnung wenn collection.count() == 0


# TODO: Pydantic Response Models
#
# class SearchResult(BaseModel):
#     frage: str
#     antwort: str
#     distance: float
#
# class SearchResponse(BaseModel):
#     query: str
#     count: int
#     results: list[SearchResult]


# TODO: Endpoints
#
# GET /          → API Info + Endpoints-Liste
# GET /health    → Status + Dokumenten-Anzahl
# GET /search    → Semantic Search (query, top_k, kategorie)
#                  Validierung: leere Query → 400, top_k Range → 400
# GET /categories → Alle Kategorien aus den Metadaten
#
# GOLD:
# POST /ask      → RAG Pipeline (importiert ask_faq aus rag/pipeline.py)
