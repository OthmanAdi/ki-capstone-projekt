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
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb


# ============================================================================
# 1. APP + DATABASE
# ============================================================================

app = FastAPI(title=Config.API_TITLE, version=Config.API_VERSION)

client = chromadb.PersistentClient(path=Config.DB_PATH)
collection = client.get_or_create_collection(name=Config.COLLECTION_NAME)

if collection.count() == 0:
    print("WARNUNG: Collection ist leer! Zuerst: python scripts/01_setup_db.py")


# ============================================================================
# 2. RESPONSE MODELS
# ============================================================================

class SearchResult(BaseModel):
    frage: str
    antwort: str
    distance: float


class SearchResponse(BaseModel):
    query: str
    count: int
    results: list[SearchResult]


# ============================================================================
# 3. ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    return {
        "message": Config.API_TITLE,
        "version": Config.API_VERSION,
        "endpoints": ["/search", "/health", "/categories", "/docs"],
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "collection": Config.COLLECTION_NAME,
        "documents": collection.count(),
    }


@app.get("/search", response_model=SearchResponse)
def search(query: str, top_k: int = Config.DEFAULT_TOP_K, kategorie: str = None):
    """Semantische Suche in der FAQ-Datenbank."""

    if not query.strip():
        raise HTTPException(status_code=400, detail="Query darf nicht leer sein.")

    if top_k < 1 or top_k > Config.MAX_TOP_K:
        raise HTTPException(
            status_code=400,
            detail=f"top_k muss zwischen 1 und {Config.MAX_TOP_K} sein.",
        )

    where_clause = {"kategorie": kategorie} if kategorie else None

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_clause,
    )

    formatted = [
        SearchResult(
            frage=results["documents"][0][i],
            antwort=results["metadatas"][0][i]["antwort"],
            distance=round(results["distances"][0][i], 3),
        )
        for i in range(len(results["documents"][0]))
    ]

    return SearchResponse(query=query, count=len(formatted), results=formatted)


@app.get("/categories")
def get_categories():
    """Alle verfügbaren Kategorien."""

    all_data = collection.get(include=["metadatas"])
    kategorien = set()
    for meta in all_data["metadatas"]:
        if meta and "kategorie" in meta:
            kategorien.add(meta["kategorie"])

    return {"categories": sorted(list(kategorien)), "total": len(kategorien)}
