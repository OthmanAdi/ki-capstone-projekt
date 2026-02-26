# =============================================================================
# SETUP DB — Database for FAQ Assistant
# =============================================================================
# - Creates Chromadb faq database from entries in faq_data

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import chromadb
from config import Config
from data.faq_data import FAQ_DATA

def setup_database(db_path: str, collection_name: str, faq_data: list):
    """
    Initializes ChromaDB and migrates FAQ data to ChromaDB with validation and error handling.

    Args:
        db_path (string): Path to ChromaDB database (absolute or relative)
        collection_name (string): Name for new or existing ChromaDB collection
        faq_data (list): List of FAQ dictionaries with 'question', 'answer', 'category' keys

    Returns:
        int: Number of FAQs successfully migrated

    Raises:
        ValueError: If config or faq values are invalid
        RuntimeError: If database initialization or FAQ migration fails
    """


    # Validate faq_data type
    if not isinstance(faq_data, list):
        raise TypeError(
            f"faq_data must be a list, got {type(faq_data).__name__}"
        )

    # Validate FAQ data exists
    if len(faq_data) == 0:
        raise ValueError("faq_data is empty. Nothing to migrate.")

    print("\n" + "=" * 60)
    print("Initializing ChromaDB...")
    print("=" * 60)

    try:
        # Ensure directory exists
        db_path = Path(db_path)
        db_path.mkdir(parents=True, exist_ok=True)

        # Create persistent client
        client = chromadb.PersistentClient(path=db_path)

        # Get or create collection
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "FAQ knowledge base for customer service"}
        )

        print(f"✓ ChromaDB initialized at: {db_path}")
        print(f"✓ Collection '{collection_name}' ready")
        print(f"✓ Current document count: {collection.count()}")

        #return client, collection

    # Print Error if ChromaDB cannot be initialized
    except Exception as error:
        raise RuntimeError(
            f"Failed to initialize ChromaDB at '{db_path}': {str(error)}"
        ) from error

    print(f"\nMigrating {len(faq_data)} FAQs to ChromaDB......")

    migrated_count = 0
    failed_items = []

    for idx, faq in enumerate(faq_data):
        try:
            collection.upsert(
                documents=[faq["question"]],
                metadatas=[{
                    "answer": faq["answer"],
                    "category": faq["category"],
                    "source": faq["source"],
                    "id_original": idx
                }],
                ids=[f"faq_{idx}"]
            )
            migrated_count += 1

        except Exception as error:
            error_msg = f"Failed to migrate FAQ {idx}: {str(error)}"
            print(f"⚠ {error_msg}")
            failed_items.append((idx, str(error)))

    # Summary
    print(f"\n✓ {migrated_count}/{len(faq_data)} FAQs migrated successfully.")

    if failed_items:
        print(f"⚠ {len(failed_items)} items failed:")
        for idx, error in failed_items[:3]:  # Show first 3 errors
            print(f"  - FAQ {idx}: {error}")

    print(f"✓ Collection now has {collection.count()} entries.")

    return migrated_count


if __name__ == "__main__":
    setup_database(Config.DB_PATH, Config.COLLECTION_NAME, FAQ_DATA)
