"""
GOLD: RAG Pipeline
===================
Retrieval-Augmented Generation: ChromaDB Suche → OpenAI Antwort.

Wird von api/main.py und ui/app.py importiert.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import os
from openai import OpenAI
from dotenv import load_dotenv
from config import Config


# TODO: ask_faq(query, collection, top_k) → dict
#
# Schritt 1: collection.query(query_texts=[query], n_results=top_k)
#
# Schritt 2: Kontext als String bauen
#   for i in range(len(results["documents"][0])):
#       frage = results["documents"][0][i]
#       antwort = results["metadatas"][0][i]["antwort"]
#       context += f"Frage: {frage}\nAntwort: {antwort}\n\n"
#
# Schritt 3: Prompts bauen
#   system_prompt = "Du bist ein hilfreicher FAQ-Assistent..."
#   user_prompt = f"Frage: {query}\n\nRelevante FAQs:\n{context}"
#
# Schritt 4: OpenAI API Call
#   client = openai.OpenAI()
#   response = client.chat.completions.create(
#       model=Config.LLM_MODEL,
#       messages=[
#           {"role": "system", "content": system_prompt},
#           {"role": "user", "content": user_prompt},
#       ],
#       max_tokens=Config.MAX_TOKENS,
#   )
#
# Schritt 5: Return
#   return {"answer": ..., "sources": [...], "query": query}
#
# Fail Fast: if not os.getenv("OPENAI_API_KEY") → Fehlermeldung zurückgeben


# =============================================================================
# SEMANTIC SEARCH — The core search function
# =============================================================================
# Returns top-k results for a single query string as a formatted list.

def semantic_search(
        query: str,
        collection,
        top_k: int,
        category: str = None,
        source: str = None,
    ) -> list:
    """
    Searches for the most similar FAQs to a query using semantic similarity.

    Args:
        query (str): User's search query
        collection: ChromaDB collection instance
        top_k (int): Number of results to return
        category (str, optional): Filter by category metadata
        source (str, optional): Filter by source metadata

    Returns:
        list: List of dictionaries containing question, answer, category, source and distance

    Raises:
        ValueError: If query is empty or top_k is invalid
        TypeError: If collection is None
    """

    # Validate inputs
    if collection is None:
        raise TypeError("Collection cannot be None. Initialize ChromaDB first and pass a valid collection.")

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    if not isinstance(top_k, int) or top_k <= 0:
        raise ValueError(f"top_k must be a positive integer, got: {top_k}")

    # Build filter clause
    where_clause = None
    if category and source:
        where_clause = {
            "$and": [
                {"category": category},
                {"source": source}
            ]
        }
    elif category:
        where_clause = {"category": category}
    elif source:
        where_clause = {"source": source}

    try:
        # Query ChromaDB
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where_clause
        )
    except Exception as error:
        print(f"⚠ ChromaDB query failed: {str(error)}")
        return []

    # Format results
    formatted = []
    if len(results["documents"][0]) > 0: # If results where found
        for idx in range(len(results["documents"][0])):
            try:
                formatted.append({
                    "question": results["documents"][0][idx],
                    "answer": results["metadatas"][0][idx]["answer"],
                    "category": results["metadatas"][0][idx].get("category", "unknown"), # If category is not present, then assign default: "category", "unknown"
                    "source": results["metadatas"][0][idx].get("source", "unknown"), # If source is not present, then assign default: "category", "unknown"
                    "distance": results["distances"][0][idx] # Smaller numbers = more similar
                })
            except (KeyError, IndexError) as error:
                print(f"⚠ Skipping result {idx} due to malformed data: {error}")
                continue
    else:
        if where_clause:
            print(f"ℹ No matches found for query '{query}' with filters: {where_clause}")
        else:
            print(f"ℹ No matches found for query '{query}'")

    return formatted

# =============================================================================
# SEARCH WRAPPER
# =============================================================================
# Wrapper for conducting semantic searches for multiple queries

def wrap_search(
        query,
        collection,
        category: str = None,
        source: str = None,
        top_k: int = 3,
        verbose: bool = True
    ) -> dict:
    """
    Conducts semantic search using embeddings.
    Accepts either a single query (str) or multiple queries (list).
    Returns top k results per query (dict).

    Args:
        query (str or list): Single query string or list of query strings
        collection: ChromaDB collection instance
        category (str, optional): Filter by category (e.g., "payment", "subscription")
        source (str, optional): Filter by data source (e.g., "faq", "docs")
        top_k (int): Number of results per query (default: 3)
        verbose (bool): Print results to console (default: True)

    Returns:
        dict: Dictionary mapping each query to its results
              Format: {query_text: [list of result dicts]}

    Examples:
        # Print results
        wrap_search("costs", collection, category="payment")

        # Get results without printing
        results = wrap_search("costs", collection, verbose=False)

        # Multiple queries
        results = wrap_search(["free trial", "cancel"], collection)
    """

    #  Validate and convert query to list
    if isinstance(query, str):
        queries = [query]
    elif isinstance(query, list):
        if not query:  # Empty list check
            print("⚠ Query list is empty. Returning empty results.")
            return {}
        queries = query
    else:
        print(
            f"✗ Invalid query type: {type(query).__name__}. "
            f"Expected str or list, got: {repr(query)}"
        )
        return

    print("\n" + "=" * 60)
    print("Starting semantic search...")
    print("=" * 60)
    print(f"Searching for {len(queries)} {'query' if len(queries) == 1 else 'queries'} ...")

    # Store all results
    all_results  = {}

    for idx, q in enumerate(queries, 1):
        if verbose:
            print(f"\n{'─' * 60}")
            print(f"QUERY {idx}: \"{q}\"")
            print(f"{'─' * 60}")

        try:
            results = semantic_search(q, collection, top_k, category, source)
        except (ValueError, TypeError) as error:
            print(f"⚠ Skipping query '{q}': {error}")
            all_results[q] = []
            continue

        # Store results for respective query
        all_results[q] = results

        if verbose:
            if not results:
                print("      No results found.")
            else: # Print results
                for i, r in enumerate(results, 1):
                    print(f"\n  [{i}] Distance: {r['distance']:.3f}")
                    print(f"      Query:   {r['question']}")
                    print(f"      Answer: {r['answer'][:60]}...")
                    print(f"      Category: {r['category']}")


    return all_results

# =============================================================================
# CREATE SYSTEM PROMPT
# =============================================================================
# Create a system prompt for LLM calls

def create_system_prompt(query: str, search_results: list, system_role: str = "helpful customer service assistant") -> str:
    """
    Creates a structured prompt for the LLM based on search results.

    Args:
        query: The user's original question
        search_results: List of FAQ matches from semantic search
        system_role: Role description for the LLM

    Returns:
        Formatted prompt string for the LLM

    Raises:
        ValueError: If query is empty or search_results is invalid
    """

    # DEFENSIVE: Validate parameters
    if not query or not isinstance(query, str):
        raise ValueError("query must be a non-empty string")

    if not isinstance(search_results, list):
        raise ValueError("search_results must be a list")

    # Build the FAQ context from search results
    faq_context = ""
    for i, result in enumerate(search_results, 1):
        faq_context += f"\nFAQ {i}:\n"
        faq_context += f"Question: {result['question']}\n"
        faq_context += f"Answer: {result['answer']}\n"

    # Create the complete prompt with instructions
    prompt = f"""<system>
        You are a {system_role}.
        You job is to answer customer queries based on the FAQ-Database.

        Rules:
        1. Answer ONLY based on the provided FAQ entries
        2. If the question cannot be answered through the FAQs, say so honestly
        3. Be friendly and professional
        4. Keep the answer brief and precise (2-3 sentences)
        5. If multiple FAQ entries are relevant, combine the information
        </system>

        <context>
        The following FAQ entries have been identified as relevant to the customer inquiry:
        {faq_context}
        </context>

        <customer_query>
        {query}
        </customer_query>

        <instruction>
        Answer the customer inquiry based on the context.
        If the relevance scores are low (< 0.5), point out that you are not certain.
        </instruction>

        <answer>
        """

    return prompt



