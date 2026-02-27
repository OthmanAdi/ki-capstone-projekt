"""
BRONZE: Persistence Test
=========================
Verifies that FAQ data survives an application restart by connecting
with a fresh ChromaDB client and running three checks.

Tests:
    1. Database connection  — collection exists and contains documents
    2. Semantic search      — query returns results
    3. Metadata validation  — results contain all required fields

Run:    python scripts/02_test_persistence.py
Result: [PASS] or [FAIL] per test
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ── Third-party ───────────────────────────────────────────────
import chromadb
from config import Config

def test_persistence(query: str, db_path: str, collection_name: str):
    """
    Runs three persistence checks against an existing ChromaDB collection.
    Uses a fresh client — no shared state with the setup script.

    Args:
        query (str):            Test query for the semantic search check
        db_path (str):          Path to the ChromaDB database directory
        collection_name (str):  Name of the collection to verify

    Prints:
        [PASS] or [FAIL] for each of the three tests
    """

    print("\n" + "=" * 60)
    print("STARTING PERSISTENCE TESTS")
    print("=" * 60)

    # Test 1: Try to connect to collection
    try:
        print("\n" + "=" * 60)
        print("TEST 1: Connecting to database")
        print("=" * 60 + "\n")
        # Convert to path
        db_path = Path(db_path)

        if db_path.exists():
            fresh_client = chromadb.PersistentClient(path=db_path)
            fresh_collection = fresh_client.get_collection(collection_name)
        else:
            print(f"[FAIL] Path to database not found. Provided path: {db_path}")
            return

        print(f"✓ Fresh client connected to existing database")
        print(f"✓ Collection exists: {fresh_collection.name}")

        if fresh_collection.count() > 0:
            print(f"[PASS] Collection '{fresh_collection.name}' found. Number of documents: {fresh_collection.count()}")
        else:
            print(f"[FAIL] Collection '{fresh_collection.name}' exists but no documents were found within.")

    except Exception as error:
        print(f"[FAIL] Connection test failed with Error: {str(error)}")
        return

    # Test 2: Conduct simple semantic search on collection
    try:
        print("\n" + "=" * 60)
        print("TEST 2: Simple semantic search")
        print("=" * 60 + "\n")

        print(f"Performing test with query: '{query}'")

        from rag.pipeline import semantic_search # Import search function

        # Use semantic search function, returning top 3 answers
        results = semantic_search(query, fresh_collection, top_k=3)

        if results:
            for i, r in enumerate(results, 1):
                print(f"  [{i}] {r['question'][:60]}...")  # Shortened preview per result
            print(f"[PASS] Semantic search returned {len(results)} result(s)")
        else:
            print(f"[FAIL] No results returned for query: '{query}'")

    except Exception as error:
        print(f"[FAIL] Semantic search failed with Error: {str(error)}")

    # Test 3: Test if results of semantic search adhere to expected format
    try:
        print("\n" + "=" * 60)
        print("TEST 3: Metadata format validation")
        print("=" * 60 + "\n")

        # Example print
        print(f"    Sample result [0]:")
        for key, value in results[0].items():  # iterate over all key-value pairs
            print(f"    {key}: {value}")  # print each field on its own line
        print()

        required_fields = ["question", "answer", "category", "distance"]  # expected keys per result

        all_valid = True
        for i, r in enumerate(results):
            missing = [field for field in required_fields if field not in r]  # find any missing keys
            if missing:
                print(f"  ⚠ Result {i} missing fields: {missing}")
                all_valid = False

        if all_valid:
            print(f"[PASS] All {len(results)} results contain required fields: {required_fields}")
        else:
            print(f"[FAIL] Some results have missing or malformed metadata.")

    except Exception as error:
        print(f"[FAIL] Metadata format validation failed with Error: {str(error)}")


if __name__ == "__main__":
    print("Performing Tests with config default settings:")
    print(f"    Database Path:      '{Config.DB_PATH}'")
    print(f"    Collection Name:    '{Config.COLLECTION_NAME}'")
    print(f"    Test query:         '{Config.DEFAULT_QUERY}'")

    test_persistence(Config.DEFAULT_QUERY, Config.DB_PATH, Config.COLLECTION_NAME)
