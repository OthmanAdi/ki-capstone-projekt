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

import chromadb

from config import Config
from data.faq_data import FAQ_DATA


def setup_database():
    """Erstellt die ChromaDB Collection und migriert alle FAQ-Daten."""

    # 1. DB-Pfad erstellen
    db_path = Path(Config.DB_PATH)
    db_path.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Datenbank-Pfad: {db_path.resolve()}")

    # 2. PersistentClient erstellen
    client = chromadb.PersistentClient(path=str(db_path))

    # 3. Collection erstellen (get_or_create für Idempotenz)
    collection = client.get_or_create_collection(name=Config.COLLECTION_NAME)
    print(f"[INFO] Collection '{Config.COLLECTION_NAME}' geladen (aktuell {collection.count()} Dokumente)")

    # 4. Validierung der FAQ-Daten
    if not FAQ_DATA:
        print("[WARN] FAQ_DATA ist leer — keine Daten zum Importieren.")
        return

    required_keys = {"frage", "antwort", "kategorie"}
    failed_items = []
    success_count = 0

    # 5. Daten einzeln mit upsert einfügen (Partial Failure Handling)
    for idx, item in enumerate(FAQ_DATA):
        try:
            # Validierung: alle Pflichtfelder vorhanden?
            missing = required_keys - set(item.keys())
            if missing:
                raise ValueError(f"Fehlende Felder: {missing}")

            # Validierung: keine leeren Werte?
            for key in required_keys:
                if not isinstance(item[key], str) or not item[key].strip():
                    raise ValueError(f"Feld '{key}' ist leer oder kein String")

            doc_id = f"faq_{idx:03d}"
            collection.upsert(
                documents=[item["frage"]],
                metadatas=[{
                    "antwort": item["antwort"],
                    "kategorie": item["kategorie"].strip().lower(),
                }],
                ids=[doc_id],
            )
            success_count += 1

        except Exception as e:
            failed_items.append((idx, str(e)))
            print(f"  [FAIL] Item {idx}: {e}")

    # 6. Ergebnis ausgeben
    print(f"\n{'='*40}")
    print(f"  Erfolgreich: {success_count}/{len(FAQ_DATA)}")
    if failed_items:
        print(f"  Fehlgeschlagen: {len(failed_items)}")
        for idx, err in failed_items:
            print(f"    - Item {idx}: {err}")
    print(f"  Collection total: {collection.count()} Dokumente")
    print(f"{'='*40}")


if __name__ == "__main__":
    setup_database()
