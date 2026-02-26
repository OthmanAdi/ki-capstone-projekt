"""
GOLD: RAG Pipeline
===================
Retrieval-Augmented Generation: ChromaDB Suche → OpenAI Antwort.

Wird von api/main.py und ui/app.py importiert.
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def ask_faq(query: str, collection, top_k: int = Config.DEFAULT_TOP_K) -> dict:
    """
    Vollständige RAG Pipeline:
    1. Semantic Search → top_k Ergebnisse aus ChromaDB
    2. Kontext bauen → Ergebnisse als String
    3. Prompt bauen → System + User + Kontext
    4. OpenAI API Call → Antwort generieren
    5. Return → dict mit answer, sources, query
    """

    # Schritt 1: Semantic Search
    results = collection.query(query_texts=[query], n_results=top_k)

    if not results["documents"][0]:
        return {
            "answer": "Keine relevanten Informationen gefunden.",
            "sources": [],
            "query": query,
        }

    # Schritt 2: Kontext bauen
    sources = []
    context = ""

    for i in range(len(results["documents"][0])):
        frage = results["documents"][0][i]
        antwort = results["metadatas"][0][i]["antwort"]
        similarity = round((1 - results["distances"][0][i]) * 100)

        context += f"<faq>\n"
        context += f"  <frage>{frage}</frage>\n"
        context += f"  <antwort>{antwort}</antwort>\n"
        context += f"  <relevanz>{similarity}%</relevanz>\n"
        context += f"</faq>\n\n"

        sources.append({"frage": frage, "similarity": similarity})

    # Schritt 3: Prompt
    system_prompt = (
        "Du bist ein hilfreicher FAQ-Assistent. "
        "Beantworte die Frage des Users basierend auf den bereitgestellten FAQ-Einträgen. "
        "Wenn die FAQs die Frage nicht beantworten können, sage das ehrlich. "
        "Antworte auf Deutsch. Sei konkret und hilfreich."
    )

    user_prompt = f"Frage: {query}\n\nRelevante FAQs:\n{context}"

    # Schritt 4: API Call
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "answer": "OPENAI_API_KEY nicht gesetzt. Bitte in .env eintragen.",
            "sources": sources,
            "query": query,
        }

    openai_client = OpenAI()

    response = openai_client.chat.completions.create(
        model=Config.LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=Config.MAX_TOKENS,
    )

    answer = response.choices[0].message.content

    # Schritt 5: Return
    return {
        "answer": answer,
        "sources": sources,
        "query": query,
    }
