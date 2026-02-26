"""
GOLD: RAG Pipeline
===================
Retrieval-Augmented Generation: ChromaDB Suche → OpenAI Antwort.

Wird von api/main.py und ui/app.py importiert.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

# TODO: openai, os, dotenv importieren


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
