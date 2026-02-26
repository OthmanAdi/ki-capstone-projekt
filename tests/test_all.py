"""
DIAMOND: Smoke Tests
=====================
Prüft dass alle Komponenten funktionieren.

Ausführen: python tests/test_all.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
import chromadb


def test_config():
    """Config-Werte sind gesetzt."""
    assert Config.DB_PATH, "DB_PATH fehlt"
    assert Config.COLLECTION_NAME, "COLLECTION_NAME fehlt"
    assert Config.DEFAULT_TOP_K > 0, "DEFAULT_TOP_K muss > 0 sein"
    assert Config.LLM_MODEL, "LLM_MODEL fehlt"
    print("  [PASS] Config")


def test_database_exists():
    """ChromaDB Datenbank existiert und hat Daten."""
    client = chromadb.PersistentClient(path=Config.DB_PATH)
    collection = client.get_collection(Config.COLLECTION_NAME)
    assert collection.count() > 0, f"Collection leer (count={collection.count()})"
    print(f"  [PASS] Database exists ({collection.count()} docs)")


def test_search_returns_results():
    """Eine einfache Suche gibt Ergebnisse zurück."""
    client = chromadb.PersistentClient(path=Config.DB_PATH)
    collection = client.get_collection(Config.COLLECTION_NAME)
    results = collection.query(query_texts=["Passwort"], n_results=1)
    assert results["documents"][0], "Keine Ergebnisse für 'Passwort'"
    print("  [PASS] Search returns results")


def test_metadata_has_kategorie():
    """Jedes Dokument hat 'kategorie' in den Metadaten."""
    client = chromadb.PersistentClient(path=Config.DB_PATH)
    collection = client.get_collection(Config.COLLECTION_NAME)
    all_data = collection.get(include=["metadatas"])
    for i, meta in enumerate(all_data["metadatas"]):
        assert "kategorie" in meta, f"FAQ {i} hat keine 'kategorie'"
        assert "antwort" in meta, f"FAQ {i} hat keine 'antwort'"
    print("  [PASS] Metadata complete")


def test_search_with_filter():
    """Suche mit Kategorie-Filter funktioniert."""
    client = chromadb.PersistentClient(path=Config.DB_PATH)
    collection = client.get_collection(Config.COLLECTION_NAME)
    results = collection.query(
        query_texts=["Passwort"],
        n_results=1,
        where={"kategorie": "konto"},
    )
    assert results["documents"][0], "Filter-Suche gibt keine Ergebnisse"
    kat = results["metadatas"][0][0]["kategorie"]
    assert kat == "konto", f"Falscher Filter: erwartet 'konto', bekommen '{kat}'"
    print("  [PASS] Search with filter")


def test_fastapi_endpoints():
    """FastAPI Endpoints antworten korrekt."""
    try:
        from api.main import app
        from fastapi.testclient import TestClient

        c = TestClient(app)
        assert c.get("/").status_code == 200, "GET / failed"
        assert c.get("/health").status_code == 200, "GET /health failed"
        assert c.get("/search?query=test").status_code == 200, "GET /search failed"
        assert c.get("/search?query=").status_code == 400, "Empty query should be 400"
        assert c.get("/categories").status_code == 200, "GET /categories failed"
        print("  [PASS] FastAPI endpoints")
    except ImportError:
        print("  [SKIP] FastAPI (not implemented yet)")


if __name__ == "__main__":
    print("\n=== SMOKE TESTS ===\n")

    tests = [
        test_config,
        test_database_exists,
        test_search_returns_results,
        test_metadata_has_kategorie,
        test_search_with_filter,
        test_fastapi_endpoints,
    ]

    passed = 0
    failed = 0
    skipped = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [FAIL] {test.__name__}: {e}")
            failed += 1

    print(f"\n=== {passed} passed, {failed} failed ===\n")
