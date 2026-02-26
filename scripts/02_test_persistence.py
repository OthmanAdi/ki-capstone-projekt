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

from config import Config
import chromadb


def test_persistence():
    """
    Erstellt einen KOMPLETT NEUEN Client und prüft:
    1. Collection existiert
    2. Dokumente sind vorhanden (count > 0)
    3. Eine Test-Query gibt Ergebnisse zurück
    4. Metadaten sind korrekt (kategorie vorhanden)
    """

    print("=== PERSISTENCE TEST ===\n")
    passed = 0
    failed = 0

    # 1. Neuer Client (simulates restart)
    fresh_client = chromadb.PersistentClient(path=Config.DB_PATH)

    # Test 1: Collection existiert
    try:
        collection = fresh_client.get_collection(Config.COLLECTION_NAME)
        print(f"  [PASS] Collection '{Config.COLLECTION_NAME}' existiert")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] Collection nicht gefunden: {e}")
        failed += 1
        print(f"\n=== {passed} passed, {failed} failed ===")
        return

    # Test 2: Dokumente vorhanden
    count = collection.count()
    if count > 0:
        print(f"  [PASS] {count} Dokumente gefunden")
        passed += 1
    else:
        print(f"  [FAIL] Collection ist leer (count=0)")
        failed += 1

    # Test 3: Query funktioniert
    results = collection.query(query_texts=["Passwort vergessen"], n_results=1)
    if results["documents"][0]:
        print(f"  [PASS] Query gibt Ergebnisse: '{results['documents'][0][0][:50]}...'")
        passed += 1
    else:
        print(f"  [FAIL] Query gibt keine Ergebnisse")
        failed += 1

    # Test 4: Metadaten korrekt
    if results["metadatas"][0] and "kategorie" in results["metadatas"][0][0]:
        kat = results["metadatas"][0][0]["kategorie"]
        print(f"  [PASS] Metadaten vorhanden (kategorie='{kat}')")
        passed += 1
    else:
        print(f"  [FAIL] Metadaten fehlen oder keine 'kategorie'")
        failed += 1

    print(f"\n=== {passed} passed, {failed} failed ===")


if __name__ == "__main__":
    test_persistence()
