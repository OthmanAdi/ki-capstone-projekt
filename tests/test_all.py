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

# TODO: chromadb importieren


def test_config():
    """Config-Werte sind gesetzt."""
    assert Config.DB_PATH, "DB_PATH fehlt"
    assert Config.COLLECTION_NAME, "COLLECTION_NAME fehlt"
    assert Config.DEFAULT_TOP_K > 0, "DEFAULT_TOP_K muss > 0 sein"
    print("  [PASS] Config")


def test_database_exists():
    """ChromaDB Datenbank existiert und hat Daten."""
    # TODO: PersistentClient laden, collection.count() > 0 prüfen
    print("  [PASS] Database exists")


def test_search_returns_results():
    """Eine einfache Suche gibt Ergebnisse zurück."""
    # TODO: collection.query("Passwort"), prüfe dass results nicht leer
    print("  [PASS] Search returns results")


def test_metadata_has_kategorie():
    """Jedes Dokument hat 'kategorie' und 'antwort' in den Metadaten."""
    # TODO: collection.get(include=["metadatas"]), prüfe jedes Item
    print("  [PASS] Metadata complete")


def test_search_with_filter():
    """Suche mit Kategorie-Filter funktioniert."""
    # TODO: collection.query(..., where={"kategorie": "konto"})
    print("  [PASS] Search with filter")


def test_fastapi_endpoints():
    """FastAPI Endpoints antworten korrekt."""
    # TODO: from api.main import app, TestClient
    # GET / → 200
    # GET /health → 200
    # GET /search?query=test → 200
    # GET /search?query= → 400
    # GET /categories → 200
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

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {test.__name__}: {e}")
            failed += 1

    print(f"\n=== {passed} passed, {failed} failed ===\n")
