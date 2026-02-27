"""
GOLD: Search Evaluation + wandb Tracking
==========================================
Tests search quality across embedding models and logs all results to wandb.

Run: python scripts/03_evaluate.py
Result:  wandb Dashboard at https://wandb.ai under Config.WANDB_PROJECT
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

import chromadb
import wandb
from dotenv import load_dotenv
from chromadb.utils import embedding_functions


# Test-Queries with expected categories
TEST_QUERIES = [
    ("I forgot my password",             "account"),
    ("How much does it cost?",           "price"),
    ("I want to cancel my subscription", "subscription"),
    ("How do I contact customer service?", "support"),
    ("Is there a free trial?",           "price"),
    ("How do I change my email address?", "account"),
    ("Which payment methods are accepted?", "payment"),
    ("Can I pause my subscription?",     "subscription"),
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
