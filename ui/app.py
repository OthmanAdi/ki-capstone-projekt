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

from config import Config
import gradio as gr
import chromadb


# ============================================================================
# 1. DATABASE
# ============================================================================

client = chromadb.PersistentClient(path=Config.DB_PATH)
collection = client.get_or_create_collection(name=Config.COLLECTION_NAME)


# ============================================================================
# 2. SUCHFUNKTION
# ============================================================================

def search_faq(query: str, top_k: int, kategorie: str) -> str:
    """Sucht in ChromaDB und gibt formatiertes Markdown zurück."""

    if not query.strip():
        return "Bitte eine Frage eingeben."

    where_clause = None
    if kategorie and kategorie != "Alle":
        where_clause = {"kategorie": kategorie}

    results = collection.query(
        query_texts=[query],
        n_results=int(top_k),
        where=where_clause,
    )

    if not results["documents"][0]:
        return "Keine Ergebnisse gefunden."

    output = f"**{len(results['documents'][0])} Ergebnisse für:** '{query}'\n\n---\n\n"

    for i in range(len(results["documents"][0])):
        similarity = round((1 - results["distances"][0][i]) * 100)
        output += f"### [{i+1}] Ähnlichkeit: {similarity}%\n"
        output += f"**Frage:** {results['documents'][0][i]}\n\n"
        output += f"**Antwort:** {results['metadatas'][0][i]['antwort']}\n\n"
        output += "---\n\n"

    return output


# ============================================================================
# 3. GRADIO INTERFACE
# ============================================================================

KATEGORIEN = ["Alle", "konto", "preis", "abo", "zahlung", "support"]

demo = gr.Interface(
    fn=search_faq,
    inputs=[
        gr.Textbox(
            label="Eure Frage",
            placeholder="z.B. Passwort vergessen...",
            lines=2,
        ),
        gr.Slider(minimum=1, maximum=8, value=3, step=1, label="Anzahl Ergebnisse"),
        gr.Dropdown(choices=KATEGORIEN, value="Alle", label="Kategorie"),
    ],
    outputs=gr.Markdown(label="Ergebnisse"),
    title="Semantic FAQ Search",
    description=f"Semantische Suche powered by ChromaDB — {collection.count()} Dokumente",
    examples=[
        ["Passwort vergessen", 3, "Alle"],
        ["Was kostet das?", 2, "preis"],
        ["Ich will kündigen", 3, "abo"],
    ],
)

if __name__ == "__main__":
    demo.launch(share=True)
