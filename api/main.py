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

# ── Third-party ───────────────────────────────────────────────
import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ── Internal ──────────────────────────────────────────────────
from rag.pipeline import semantic_search
from config import Config

# ── App & DB init ─────────────────────────────────────────────
app = FastAPI(
    title=Config.API_TITLE,
    description=Config.API_DESCRIPTION,
    version=Config.API_VERSION,
)

client = chromadb.PersistentClient(Config.DB_PATH)
collection = client.get_collection(Config.COLLECTION_NAME)

# ── Pydantic Models ───────────────────────────────────────────
class SearchResult(BaseModel):
    question: str
    answer: str
    category: str
    source: str
    distance: float

class SearchResponse(BaseModel):
    query: str
    count: int
    results: list[SearchResult]

# ── Endpoints ─────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "FAQ Search API Alive"}

@app.get("/health")
def health():
    count = collection.count()

    # does not raise error but gives warning
    if count == 0:
        status = "warning — collection is empty"
    else:
        status = "ok"

    return {
        "status": status,
        "collection": collection.name,
        "dokumente": count
    }

@app.get("/categories")
def categories():
    """
    Automatically fetches all categories available in the FAQ database.
    """

    # Get all metadata from chromaDB
    results = collection.get(include=["metadatas"]) # Only fetch metadata

    # Guard: database is empty
    if not results["metadatas"]:
        raise HTTPException(status_code=404, detail="No documents found in the collection.")

    unique_categories = set(  # set() automatically removes duplicates
        meta["category"]
        for meta in results["metadatas"]
        if "category" in meta  # safety check - skips entries without category
    )

    return {
        "count": len(unique_categories),
        "categories": sorted(unique_categories)
    }

@app.get("/search", response_model=SearchResponse)
def search(query: str = "I forgot my Password", top_k: int = 3, category: str = None):
    """
    Semantic search in the FAQ database.
    - **query**: Search query (required)
    - **top_k**: Number of results (default: 3)
    - **category**: Optional category filter
    """

    # Defensive logic
    # Query cannot be emtpty
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Better feedback for invalid category
    valid_categories = categories()["categories"]
    if (category is not None) and  (category not in valid_categories):
        raise HTTPException(status_code=400, detail=f"Invalid category. Please select from the following categories: {valid_categories}")

    # Top K must be > 0
    if not (1 <= top_k <= Config.MAX_TOP_K):
        raise HTTPException(status_code=400, detail=f"top_k must be between 1 and {Config.MAX_TOP_K}.")

    # Call existing search_faq from core/search.py
    results = semantic_search(
        query=query,
        collection=collection,
        top_k=top_k,
        category=category
    )

    # Convert the list of of dicts into SearchResult
    formatted = []
    for result in results:
        result = SearchResult(
            question = result["question"],
            answer = result["answer"],
            category = result["category"],
            source = result["source"],
            distance = round(result["distance"], 3)
        )
        formatted.append(result)

    return SearchResponse(
        query=query,
        count=len(formatted),
        results=formatted
    )




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