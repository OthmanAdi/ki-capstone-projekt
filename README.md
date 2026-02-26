# German AI FAQ Assistant — RAG System

**KI & Python Modul — Capstone Projekt, Woche 4**

Ein vollständiges Retrieval-Augmented Generation (RAG) System: Semantische Suche in einer FAQ-Datenbank mit automatischer Antwortgenerierung.

---

## Was dieses System macht

```
User stellt Frage
        ↓
ChromaDB: Semantische Suche (Embeddings)
        ↓
Top-K relevante FAQs gefunden
        ↓
OpenAI GPT-4o-mini: Generiert Antwort basierend auf FAQs
        ↓
User bekommt eine konkrete, hilfreiche Antwort
```

---

## Tech Stack

| Technologie | Zweck | Warum |
|-------------|-------|-------|
| **ChromaDB** | Vector Database | Lokale Persistenz, automatische Embeddings |
| **FastAPI** | REST API | Automatische Docs, Type Safety, async |
| **Gradio** | Web UI | Python-Funktion → Web-App in einer Zeile |
| **OpenAI** | LLM (GPT-4o-mini) | Antwortgenerierung im RAG-Pipeline |
| **wandb** | Experiment Tracking | Suchqualität messen und vergleichen |

---

## Setup

### 1. Repository klonen + Branch erstellen

```bash
git clone https://github.com/OthmanAdi/ki-capstone-projekt.git
cd ki-capstone-projekt
git checkout -b EUER_NAME/capstone
```

### 2. Virtual Environment

```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate
```

**Python 3.10-3.13 erforderlich.** Python 3.14 funktioniert NICHT mit ChromaDB.

### 3. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 4. API Keys

Kopiert `.env.example` zu `.env` und tragt eure Keys ein:

```bash
cp .env.example .env
```

```
OPENAI_API_KEY=sk-...
WANDB_API_KEY=...
```

**`.env` ist in `.gitignore` — wird NIE committed.**

---

## Ausführen

### Schritt 1: Datenbank aufsetzen

```bash
python scripts/01_setup_db.py
```

### Schritt 2: Persistence testen

```bash
python scripts/02_test_persistence.py
```

### Schritt 3: FastAPI starten (Terminal 1)

```bash
uvicorn api.main:app --reload --port 8000
```

Swagger UI: `http://localhost:8000/docs`

### Schritt 4: Gradio starten (Terminal 2)

```bash
python ui/app.py
```

UI: `http://localhost:7860`

### Schritt 5: Evaluation (optional)

```bash
python scripts/03_evaluate.py
```

Dashboard: `wandb.ai` → Projekt `ki-capstone`

---

## Projektstruktur

```
ki-capstone-projekt/
├── config.py               ← Zentrale Konfiguration
├── data/
│   └── faq_data.py          ← FAQ-Datensatz
├── scripts/
│   ├── 01_setup_db.py       ← ChromaDB Setup
│   ├── 02_test_persistence.py ← Persistence Test
│   └── 03_evaluate.py       ← wandb Evaluation
├── api/
│   └── main.py              ← FastAPI Server
├── ui/
│   └── app.py               ← Gradio Interface
├── rag/
│   └── pipeline.py          ← RAG Pipeline
└── tests/
    └── test_all.py           ← Smoke Tests
```

---

*KI & Python Modul — Morphos GmbH*
