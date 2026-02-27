"""
SILVER: Gradio Interface
=========================
Web-UI für die FAQ-Suche.

Starten: python ui/app.py
Lokal:   http://localhost:7860
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# ── Third-party ───────────────────────────────────────────────
import gradio as gr
import chromadb


# ── Internal ──────────────────────────────────────────────────
from config import Config
from rag.pipeline import semantic_search, ask_faq


# ── DB init ─────────────────────────────────────────────
client = chromadb.PersistentClient(Config.DB_PATH)
collection = client.get_collection(Config.COLLECTION_NAME)

# ── Fetch categories dynamically from ChromaDB ────────────────
def get_filter_options() -> dict[str, list[str]]:
    """Reads all unique categories and sources from ChromaDB metadata at startup.
    Returns:
        dict with keys "categories" and "sources", each a sorted list with "all" prepended.
    """
    results = collection.get(include=["metadatas"])

    temp = []
    for meta in results["metadatas"]:
        if "category" in meta:
            temp.append(meta["category"])
    categories = sorted(set(temp))

    temp = []
    for meta in results["metadatas"]:
        if "source" in meta:
            temp.append(meta["source"])
    sources = sorted(set(temp))

    return {
        "categories": ["all"] + categories,  # "all" always first
        "sources": ["all"] + sources,  # "all" always first
    }

# ── Search function ─────────────────────────────────────────────

def search_faq(query: str, top_k: int, category: str, source: str):
    """
    Connects the Gradio interface to ChromaDB via semantic_search.
    Gradio calls this function when the user clicks 'Submit'.
    Input: query (str), top_k (int), category (str)
    Output: Formatted Markdown string
    """

    # Guard: empty query
    if not query or not query.strip():
        return "⚠️ Please enter a search query."

    # Guard: invalid category
    if category != "all" and category not in categories:
        return f"⚠️ Unknown category '{category}'."

    # Guard: invalid source
    if source != "all" and source not in sources:
        return f"⚠️ Unknown category '{category}'."

    # Call shared semantic_search function
    results = semantic_search(  # returns a list of dicts
        query=query,
        collection=collection,
        top_k=top_k,
        category=category if category != "all" else None,  # all = no filter
        source= source if source != "all" else None
    )

    if not results:
        filter_info = f" in category '{category}'" if category and category != "all" else ""
        return f"❌ No results were found {filter_info}."

    # Format results as Markdown string for Gradio output
    output = f"**{len(results)} Results for:** '{query}'\n\n---\n\n"

    for i, r in enumerate(results):  # r is one dict from semantic_search
        similarity = max(0, round((1 - r["distance"]) * 100))
        output += f"### [{i + 1}] Similarity: {similarity}%\n"
        output += f"**Question:** {r['question']}\n\n"
        output += f"**Answer:** {r['answer']}\n\n"
        output += "---\n\n"

    return output

# ── LLM seach function ─────────────────────────────────────────────

def ask_faq_ui(query: str, top_k: int) -> str:
    """
    Wrapper: connects Gradio UI to ask_faq pipeline.
    """

    # Guard: empty query
    if not query or not query.strip():
        return "⚠️ Please enter a question."

    # Call RAG pipeline
    result = ask_faq(
        query=query,
        collection=collection,
        top_k=top_k
    )

    # Check for pipeline error
    if result.get("error"):
        return f"❌ Error: {result['error']}"

    # Format output as Markdown
    output  = f"**Answer:**\n\n{result['answer']}\n\n---\n\n"
    output += f"**Sources used ({len(result['sources'])}):**\n\n"

    for i, s in enumerate(result["sources"], 1):
        similarity = max(0, round((1 - s["distance"]) * 100))  # clamp to 0 minimum
        output += f"**[{i}]** {s['question']} *(Similarity: {similarity}%)*\n\n"

    return output


# ── Gradio Interface ─────────────────────────────────────────────

# Categories for filtering
filter_options = get_filter_options()
categories = filter_options["categories"]
sources = filter_options["sources"]

with gr.Blocks(title="FAQ Assistant") as demo:

    with gr.Tab("🔍 Semantic Search"):       # Tab 1 — deine bisherige Logik
        gr.Markdown("## Semantic FAQ Search")
        gr.Markdown("Finds relevant answers without exact keyword mapping.")

        with gr.Row():
            query1 = gr.Textbox(label="Your question", placeholder="e.g. I forgot my password...", lines=2)
            top_k1 = gr.Slider(minimum=1, maximum=8, value=3, step=1, label="N results")

        with gr.Row():
            category1 = gr.Dropdown(choices=categories, value="all", label="Filter by category")
            source1   = gr.Dropdown(choices=sources, value="all", label="Filter by source")

        search_btn = gr.Button("Search")                 # Explicit button replaces auto-submit
        output1    = gr.Markdown(label="Results")

        search_btn.click(                                # Wire button to function
            fn=search_faq,
            inputs=[query1, top_k1, category1, source1],
            outputs=output1
        )

    with gr.Tab("🤖 AI Answer"):             # Tab 2 — RAG pipeline
        gr.Markdown("## AI-Generated Answer")
        gr.Markdown("GPT-4o-mini answers your question based on relevant FAQ entries.")

        query2  = gr.Textbox(label="Your question", placeholder="e.g. How do I cancel?", lines=2)
        top_k2  = gr.Slider(minimum=1, maximum=5, value=3, step=1, label="FAQ entries to use as context")

        ask_btn = gr.Button("Ask AI")
        output2 = gr.Markdown(label="AI Answer")

        ask_btn.click(
            fn=ask_faq_ui,                   # ← wrapper function (see below)
            inputs=[query2, top_k2],
            outputs=output2
        )

# Öffentliche URL (72h):
demo.launch(share=True)

# TODO: search_faq(query, top_k, kategorie) → str
#
# - Leere Query abfangen
# - where_clause für Kategorie-Filter (wenn nicht "Alle")
# - collection.query(query_texts=[query], n_results=top_k, where=...)
# - Ergebnisse als Markdown formatieren
# - Ähnlichkeit: round((1 - distance) * 100)


# TODO: Gradio Interface
#
# Inputs:
#   - gr.Textbox(label="Eure Frage", lines=2)
#   - gr.Slider(minimum=1, maximum=8, value=3, step=1)
#   - gr.Dropdown(choices=["Alle", "konto", "preis", ...], value="Alle")
#
# Output:
#   - gr.Markdown(label="Ergebnisse")
#
# Mindestens 3 Examples
#
# demo.launch(share=True)


# GOLD: Zweiten Tab "KI-Antwort" hinzufügen (RAG Pipeline)
# DIAMOND (Sebastian): gr.Blocks, Chat-History, HF Spaces
