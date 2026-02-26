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
from dotenv import load_dotenv
import chromadb
import wandb

load_dotenv()


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
    """

    # 1. ChromaDB laden
    client = chromadb.PersistentClient(path=Config.DB_PATH)
    collection = client.get_collection(Config.COLLECTION_NAME)

    print(f"Collection: {collection.count()} Dokumente")

    # 2. wandb starten
    wandb.init(
        project=Config.WANDB_PROJECT,
        name="search-evaluation",
        config={
            "collection": Config.COLLECTION_NAME,
            "top_k": Config.DEFAULT_TOP_K,
            "total_queries": len(TEST_QUERIES),
            "total_documents": collection.count(),
        },
    )

    # 3. Queries ausführen
    distances = []
    correct_category = 0

    for i, (query, expected_kat) in enumerate(TEST_QUERIES):
        results = collection.query(
            query_texts=[query],
            n_results=Config.DEFAULT_TOP_K,
        )

        if results["documents"][0]:
            top_distance = results["distances"][0][0]
            top_similarity = round((1 - top_distance) * 100)
            top_kategorie = results["metadatas"][0][0].get("kategorie", "")

            distances.append(top_distance)
            if top_kategorie == expected_kat:
                correct_category += 1

            wandb.log({
                "query_nr": i,
                "top_distance": top_distance,
                "top_similarity": top_similarity,
                "category_match": 1 if top_kategorie == expected_kat else 0,
            })

            status = "MATCH" if top_kategorie == expected_kat else "MISS"
            print(f"  [{status}] '{query}' → {top_similarity}% (kat: {top_kategorie})")

    # 4. Zusammenfassung
    avg_similarity = round((1 - sum(distances) / len(distances)) * 100) if distances else 0

    wandb.log({
        "avg_similarity": avg_similarity,
        "category_accuracy": round(correct_category / len(TEST_QUERIES) * 100),
        "total_queries": len(TEST_QUERIES),
    })

    wandb.finish()

    print(f"\nAvg Similarity:    {avg_similarity}%")
    print(f"Category Accuracy: {correct_category}/{len(TEST_QUERIES)}")
    print(f"\nSchaut auf wandb.ai unter '{Config.WANDB_PROJECT}'")


if __name__ == "__main__":
    evaluate_search()
