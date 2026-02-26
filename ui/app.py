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

# TODO: gradio, chromadb importieren

# TODO: ChromaDB Client + Collection laden


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
