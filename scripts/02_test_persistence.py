"""
BRONZE: Persistence Test
=========================
Beweist dass die Daten einen Neustart überleben.

WICHTIG: Erstellt einen NEUEN Client. Kein Zugriff auf den alten RAM.
Das ist der einzige korrekte Weg Persistence zu testen.

Ausführen: python scripts/02_test_persistence.py
Ergebnis:  Alle Tests bestanden ODER klare Fehlermeldung
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import chromadb

from config import Config


def test_persistence():
    """Erstellt einen KOMPLETT NEUEN Client und prüft Persistence."""

    db_path = Path(Config.DB_PATH)
    passed = 0
    failed = 0

    # Vorab-Check: existiert der DB-Ordner überhaupt?
    if not db_path.exists():
        print(f"[FAIL] Datenbank-Ordner '{db_path}' existiert nicht.")
        print("       Bitte zuerst 'python scripts/01_setup_db.py' ausführen.")
        return

    # NEUER Client (kein Zugriff auf alten RAM)
    client = chromadb.PersistentClient(path=str(db_path))

    # Test 1: Collection existiert (get_collection, NICHT get_or_create!)
    try:
        collection = client.get_collection(name=Config.COLLECTION_NAME)
        print(f"  [PASS] Collection '{Config.COLLECTION_NAME}' existiert")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] Collection '{Config.COLLECTION_NAME}' nicht gefunden: {e}")
        failed += 1
        print(f"\n=== {passed} passed, {failed} failed ===")
        return  # Ohne Collection können weitere Tests nicht laufen

    # Test 2: Dokumente sind vorhanden (count > 0)
    count = collection.count()
    if count > 0:
        print(f"  [PASS] {count} Dokumente vorhanden")
        passed += 1
    else:
        print(f"  [FAIL] Collection ist leer (count = 0)")
        failed += 1

    # Test 3: Test-Query gibt Ergebnisse zurück
    try:
        results = collection.query(query_texts=["Passwort zurücksetzen"], n_results=1)
        if results["documents"] and len(results["documents"][0]) > 0:
            print(f"  [PASS] Query liefert Ergebnisse: '{results['documents'][0][0][:60]}...'")
            passed += 1
        else:
            print("  [FAIL] Query liefert keine Ergebnisse")
            failed += 1
    except Exception as e:
        print(f"  [FAIL] Query fehlgeschlagen: {e}")
        failed += 1

    # Test 4: Metadaten sind korrekt (kategorie + antwort vorhanden)
    try:
        all_data = collection.get(include=["metadatas"])
        required_meta = {"kategorie", "antwort"}
        incomplete = []
        for i, meta in enumerate(all_data["metadatas"]):
            missing = required_meta - set(meta.keys())
            if missing:
                incomplete.append((all_data["ids"][i], missing))

        if not incomplete:
            print(f"  [PASS] Alle {len(all_data['metadatas'])} Dokumente haben vollständige Metadaten")
            passed += 1
        else:
            print(f"  [FAIL] {len(incomplete)} Dokumente mit fehlenden Metadaten:")
            for doc_id, missing in incomplete[:5]:
                print(f"    - {doc_id}: fehlt {missing}")
            failed += 1
    except Exception as e:
        print(f"  [FAIL] Metadaten-Check fehlgeschlagen: {e}")
        failed += 1

    print(f"\n=== {passed} passed, {failed} failed ===")


if __name__ == "__main__":
    test_persistence()
