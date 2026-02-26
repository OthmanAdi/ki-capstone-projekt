"""
BRONZE: ChromaDB Setup + Daten-Migration
=========================================
Liest FAQ_DATA, erstellt ChromaDB Collection, speichert alles persistent.

Ausführen: python scripts/01_setup_db.py
Ergebnis:  ./faq_database/ Ordner mit persistenten Daten
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from data.faq_data import FAQ_DATA
import chromadb


def setup_database():
    """
    Erstellt die ChromaDB Collection und migriert alle FAQ-Daten.
    Partial Failure Handling: einzelne Fehler stoppen nicht alles.
    """

    # 1. DB-Pfad erstellen
    db_path = Path(Config.DB_PATH)
    db_path.mkdir(parents=True, exist_ok=True)

    # 2. Client + Collection
    client = chromadb.PersistentClient(path=Config.DB_PATH)
    collection = client.get_or_create_collection(name=Config.COLLECTION_NAME)

    # 3. Migration mit Partial Failure Handling
    migrated = 0
    failed_items = []

    print(f"Migrating {len(FAQ_DATA)} FAQs to ChromaDB...")

    for idx, faq in enumerate(FAQ_DATA):
        try:
            collection.upsert(
                documents=[faq["frage"]],
                metadatas=[{
                    "antwort": faq["antwort"],
                    "kategorie": faq["kategorie"],
                }],
                ids=[f"faq_{idx}"],
            )
            migrated += 1
        except Exception as e:
            failed_items.append((idx, str(e)))

    # 4. Ergebnis
    print(f"\n{migrated}/{len(FAQ_DATA)} FAQs erfolgreich migriert.")

    if failed_items:
        print(f"{len(failed_items)} fehlgeschlagen:")
        for idx, error in failed_items[:3]:
            print(f"  - FAQ {idx}: {error}")

    print(f"\nCollection: {collection.name}")
    print(f"Dokumente:  {collection.count()}")
    print(f"DB-Pfad:    {Config.DB_PATH}")


if __name__ == "__main__":
    setup_database()
