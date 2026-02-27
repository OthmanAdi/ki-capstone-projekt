"""
SILVER: FastAPI Server
=======================
REST API für die FAQ-Suche.

Starten: uvicorn api.main:app --reload --port 8000
Docs:    http://localhost:8000/docs
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import chromadb
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import Config

logger = logging.getLogger(__name__)

# --- FastAPI App ---
app = FastAPI(title=Config.API_TITLE, version=Config.API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ChromaDB Client + Collection ---
_db_path = Path(Config.DB_PATH)
if not _db_path.exists():
    logger.warning("Datenbank-Ordner '%s' existiert nicht. Bitte 01_setup_db.py ausführen.", _db_path)

_client = chromadb.PersistentClient(path=str(_db_path))

try:
    collection = _client.get_collection(name=Config.COLLECTION_NAME)
except Exception:
    collection = _client.get_or_create_collection(name=Config.COLLECTION_NAME)
    logger.warning("Collection '%s' war nicht vorhanden und wurde neu erstellt.", Config.COLLECTION_NAME)

if collection.count() == 0:
    logger.warning("Collection '%s' ist leer (0 Dokumente).", Config.COLLECTION_NAME)


# --- Pydantic Response Models ---
class SearchResult(BaseModel):
    frage: str
    antwort: str
    kategorie: str
    distance: float
    similarity_pct: float


class SearchResponse(BaseModel):
    query: str
    count: int
    results: list[SearchResult]


class AskRequest(BaseModel):
    query: str
    top_k: int = Config.DEFAULT_TOP_K


class AskResponse(BaseModel):
    query: str
    answer: str
    sources: list[str]


# --- Endpoints ---

@app.get("/")
def root():
    """API Info + Endpoints-Liste."""
    return {
        "title": Config.API_TITLE,
        "version": Config.API_VERSION,
        "documents": collection.count(),
        "endpoints": {
            "GET /": "API Info",
            "GET /health": "Status + Dokumenten-Anzahl",
            "GET /search": "Semantische Suche (query, top_k, kategorie)",
            "GET /categories": "Alle Kategorien",
            "POST /ask": "RAG Pipeline — KI-generierte Antwort",
        },
    }


@app.get("/health")
def health():
    """Status + Dokumenten-Anzahl."""
    doc_count = collection.count()
    return {
        "status": "healthy" if doc_count > 0 else "degraded",
        "documents": doc_count,
        "collection": Config.COLLECTION_NAME,
    }


@app.get("/search", response_model=SearchResponse)
def search(
    query: str = Query(..., min_length=1, description="Suchbegriff"),
    top_k: int = Query(default=Config.DEFAULT_TOP_K, ge=1, le=Config.MAX_TOP_K, description="Anzahl Ergebnisse"),
    kategorie: str | None = Query(default=None, description="Kategorie-Filter"),
):
    """Semantische Suche in der FAQ-Datenbank."""
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query darf nicht leer sein.")

    # where-Clause für Kategorie-Filter
    where_clause = None
    if kategorie and kategorie.strip().lower() != "alle":
        where_clause = {"kategorie": kategorie.strip().lower()}

    try:
        results = collection.query(
            query_texts=[query.strip()],
            n_results=min(top_k, collection.count()) if collection.count() > 0 else top_k,
            where=where_clause,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Suche fehlgeschlagen: {e}")

    search_results = []
    if results["documents"] and results["documents"][0]:
        for i in range(len(results["documents"][0])):
            distance = results["distances"][0][i]
            similarity = round((1 - distance) * 100, 1)
            search_results.append(SearchResult(
                frage=results["documents"][0][i],
                antwort=results["metadatas"][0][i].get("antwort", ""),
                kategorie=results["metadatas"][0][i].get("kategorie", ""),
                distance=round(distance, 4),
                similarity_pct=max(0.0, similarity),
            ))

    return SearchResponse(query=query, count=len(search_results), results=search_results)


@app.get("/categories")
def categories():
    """Alle Kategorien aus den Metadaten."""
    if collection.count() == 0:
        return {"categories": [], "count": 0}

    all_data = collection.get(include=["metadatas"])
    cats = sorted({m.get("kategorie", "unbekannt") for m in all_data["metadatas"]})
    return {"categories": cats, "count": len(cats)}


# --- GOLD: RAG Endpoint ---

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """RAG Pipeline — KI-generierte Antwort basierend auf FAQ-Daten."""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query darf nicht leer sein.")

    try:
        from rag.pipeline import ask_faq
    except ImportError as e:
        raise HTTPException(status_code=501, detail=f"RAG Pipeline nicht verfügbar: {e}")

    result = ask_faq(
        query=request.query.strip(),
        collection=collection,
        top_k=min(request.top_k, Config.MAX_TOP_K),
    )

    if "error" in result:
        raise HTTPException(status_code=503, detail=result["error"])

    return AskResponse(
        query=result.get("query", request.query),
        answer=result.get("answer", ""),
        sources=result.get("sources", []),
    )
