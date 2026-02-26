"""
GOLD: Search Evaluation + wandb Tracking
==========================================
Testet die Suchqualität mit definierten Queries und loggt alles zu wandb.

Ausführen: python scripts/03_evaluate.py
Ergebnis:  wandb Dashboard unter dem Projekt aus Config.WANDB_PROJECT
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

# TODO: chromadb, wandb, dotenv importieren


# Test-Queries mit erwarteten Kategorien
TEST_QUERIES = [
    ("Passwort vergessen", "konto"),
    ("Was kostet das?", "preis"),
    ("Ich will kündigen", "abo"),
    ("Kundenservice kontaktieren", "support"),
    ("Kostenlose Testversion", "preis"),
    ("E-Mail ändern", "konto"),
    ("Zahlungsmethoden", "zahlung"),
    ("Abo pausieren", "abo"),
]


def evaluate_search():
    """
    Führt Test-Queries aus und loggt Ergebnisse zu wandb.

    Schritte:
    1. load_dotenv()
    2. ChromaDB Client + Collection laden
    3. wandb.init(project=Config.WANDB_PROJECT)
    4. Für jede Query: distance, similarity, category_match loggen
    5. Zusammenfassung: avg_similarity, category_accuracy
    6. wandb.finish()
    """

    # TODO: Implementieren
    pass


if __name__ == "__main__":
    evaluate_search()
