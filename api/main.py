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
from rag.pipeline import semantic_search, ask_faq
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

class LLMMetadata(BaseModel):
    question: str
    category: str
    source: str
    distance: float

class LLMAnswer(BaseModel):
    query: str
    answer: str
    sources: list[LLMMetadata]


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

@app.post("/ask", response_model=LLMAnswer)
def ask(query: str = "I forgot my Password", top_k: int = 3, category: str = None, source: str = None, system_role: str = "helpful customer service assistant", max_tokens: int = 300):
    """
    RAG pipeline: semantic search + LLM answer generation.

    Finds the most relevant FAQ entries for the query via ChromaDB,
    then passes them as context to GPT-4o-mini to generate a natural language answer.

    - **query**: Customer question (required)
    - **top_k**: Number of FAQ entries to retrieve as context (default: 3)
    - **category**: Optional filter — restricts search to one category
    - **source**: Optional filter — restricts search to one data source
    - **system_role**: LLM persona (default: helpful customer service assistant)
    - **max_tokens**: Maximum response length in tokens (default: 300)

    Returns the generated answer and the FAQ entries used as sources.
    """

    # Input validation
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    if not (1 <= top_k <= Config.MAX_TOP_K):
        raise HTTPException(status_code=400, detail=f"top_k must be between 1 and {Config.MAX_TOP_K}.")

    result = ask_faq(
        query=query,
        collection=collection,
        top_k=top_k,
        category=category,
        source=source,
        system_role=system_role,
        max_tokens=max_tokens
    )

    # Check result for error
    if result.get("error"):  # Check if pipeline failed
        raise HTTPException(status_code=500, detail=result["error"])

    return LLMAnswer(
        query=result["query"],
        answer=result["answer"],
        sources=result["sources"]
    )