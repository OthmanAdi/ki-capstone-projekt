"""
SILVER + DIAMOND: Gradio Interface (gr.Blocks + Tabs)
======================================================
Web-UI für FAQ-Suche und KI-Antwort.

Starten: python ui/app.py
Lokal:   http://localhost:7860
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import gradio as gr
import chromadb

from config import Config

# --- ChromaDB Client + Collection ---
_db_path = Path(Config.DB_PATH)
if not _db_path.exists():
    raise FileNotFoundError(
        f"Datenbank-Ordner '{_db_path}' nicht gefunden. "
        "Bitte zuerst 'python scripts/01_setup_db.py' ausführen."
    )

_client = chromadb.PersistentClient(path=str(_db_path))

try:
    collection = _client.get_collection(name=Config.COLLECTION_NAME)
except Exception as e:
    raise RuntimeError(
        f"Collection '{Config.COLLECTION_NAME}' nicht gefunden: {e}. "
        "Bitte zuerst 'python scripts/01_setup_db.py' ausführen."
    )

# Kategorien dynamisch aus DB laden
_all_data = collection.get(include=["metadatas"])
_categories = sorted({m.get("kategorie", "") for m in _all_data["metadatas"]} - {""})
_dropdown_choices = ["Alle"] + _categories


def search_faq(query: str, top_k: int, kategorie: str) -> str:
    """Semantische Suche — gibt formatiertes Markdown zurück."""
    if not query or not query.strip():
        return "Bitte geben Sie eine Frage ein."

    query = query.strip()
    n_results = min(int(top_k), collection.count()) if collection.count() > 0 else int(top_k)

    # Kategorie-Filter
    where_clause = None
    if kategorie and kategorie != "Alle":
        where_clause = {"kategorie": kategorie.lower()}

    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_clause,
        )
    except Exception as e:
        return f"**Fehler bei der Suche:** {e}"

    if not results["documents"] or not results["documents"][0]:
        return "Keine Ergebnisse gefunden."

    # Markdown-Formatierung
    output_parts = [f"## Ergebnisse für: *{query}*\n"]
    for i in range(len(results["documents"][0])):
        frage = results["documents"][0][i]
        meta = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        similarity = max(0, round((1 - distance) * 100, 1))

        output_parts.append(
            f"### {i + 1}. {frage}\n"
            f"**Antwort:** {meta.get('antwort', 'k.A.')}\n\n"
            f"**Kategorie:** `{meta.get('kategorie', 'k.A.')}` | "
            f"**Ähnlichkeit:** {similarity}%\n\n---\n"
        )

    return "\n".join(output_parts)


def ask_ai(query: str, top_k: int) -> str:
    """RAG Pipeline — KI-generierte Antwort."""
    if not query or not query.strip():
        return "Bitte geben Sie eine Frage ein."

    try:
        from rag.pipeline import ask_faq
    except ImportError:
        return "**RAG Pipeline nicht verfügbar.** Bitte rag/pipeline.py implementieren."

    result = ask_faq(
        query=query.strip(),
        collection=collection,
        top_k=int(top_k),
    )

    if "error" in result:
        return f"**Fehler:** {result['error']}"

    # Antwort + Quellen als Markdown
    parts = [
        f"## KI-Antwort\n\n{result.get('answer', 'Keine Antwort erhalten.')}\n\n---\n",
        "### Verwendete Quellen\n",
    ]
    for src in result.get("sources", []):
        parts.append(f"- {src}\n")

    return "\n".join(parts)


# --- Gradio UI: gr.Blocks mit Tabs (DIAMOND) ---
with gr.Blocks(title="FAQ Assistent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# FAQ Assistent\nSemantische Suche und KI-generierte Antworten")

    with gr.Tab("Suche"):
        with gr.Row():
            with gr.Column(scale=3):
                search_input = gr.Textbox(
                    label="Eure Frage",
                    placeholder="z.B. Wie kann ich mein Passwort zurücksetzen?",
                    lines=2,
                )
            with gr.Column(scale=1):
                search_top_k = gr.Slider(
                    minimum=1, maximum=8, value=3, step=1, label="Anzahl Ergebnisse"
                )
                search_kategorie = gr.Dropdown(
                    choices=_dropdown_choices, value="Alle", label="Kategorie"
                )
        search_btn = gr.Button("Suchen", variant="primary")
        search_output = gr.Markdown(label="Ergebnisse")

        search_btn.click(
            fn=search_faq,
            inputs=[search_input, search_top_k, search_kategorie],
            outputs=search_output,
        )
        # Enter-Taste löst auch Suche aus
        search_input.submit(
            fn=search_faq,
            inputs=[search_input, search_top_k, search_kategorie],
            outputs=search_output,
        )

        gr.Examples(
            examples=[
                ["Wie kann ich mein Passwort zurücksetzen?", 3, "Alle"],
                ["Was kostet das Premium-Abo?", 3, "preis"],
                ["Wie kontaktiere ich den Support?", 3, "support"],
                ["Welche Browser werden unterstützt?", 3, "technik"],
                ["Werden meine Daten weitergegeben?", 3, "datenschutz"],
            ],
            inputs=[search_input, search_top_k, search_kategorie],
        )

    with gr.Tab("KI-Antwort"):
        with gr.Row():
            with gr.Column(scale=3):
                ask_input = gr.Textbox(
                    label="Eure Frage",
                    placeholder="Stellt eine Frage — die KI antwortet basierend auf den FAQ-Daten",
                    lines=2,
                )
            with gr.Column(scale=1):
                ask_top_k = gr.Slider(
                    minimum=1, maximum=5, value=3, step=1, label="Kontext-Dokumente"
                )
        ask_btn = gr.Button("KI fragen", variant="primary")
        ask_output = gr.Markdown(label="KI-Antwort")

        ask_btn.click(fn=ask_ai, inputs=[ask_input, ask_top_k], outputs=ask_output)
        ask_input.submit(fn=ask_ai, inputs=[ask_input, ask_top_k], outputs=ask_output)

        gr.Examples(
            examples=[
                ["Ich habe mein Passwort vergessen, was soll ich tun?", 3],
                ["Was sind die Unterschiede zwischen den Abo-Modellen?", 3],
                ["Wie sicher sind meine Daten bei euch?", 3],
            ],
            inputs=[ask_input, ask_top_k],
        )

    gr.Markdown(
        f"---\n*{collection.count()} FAQ-Einträge | "
        f"Kategorien: {', '.join(_categories)}*"
    )


if __name__ == "__main__":
    demo.launch(server_port=Config.GRADIO_PORT, share=True)
