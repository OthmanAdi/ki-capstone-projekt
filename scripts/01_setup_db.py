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

# TODO: chromadb importieren


def setup_database():
    """
    Erstellt die ChromaDB Collection und migriert alle FAQ-Daten.

    Schritte:
    1. DB-Pfad erstellen (Path + mkdir)
    2. PersistentClient erstellen
    3. Collection erstellen (get_or_create_collection)
    4. Alle FAQ-Daten mit upsert einfügen (Partial Failure Handling!)
    5. Ergebnis ausgeben

    Hints:
    - Path(Config.DB_PATH).mkdir(parents=True, exist_ok=True)
    - chromadb.PersistentClient(path=Config.DB_PATH)
    - collection.upsert(documents=..., metadatas=..., ids=...)
    - try/except pro Item, failed_items Liste
    """

    # TODO: Implementieren
    pass


if __name__ == "__main__":
    setup_database()
