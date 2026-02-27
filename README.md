# 🔍 FAQ RAG System — Capstone Project

> **Learning Project**: Building a production-style RAG (Retrieval-Augmented Generation) system from scratch — semantic search with ChromaDB, a REST API, a web UI, and experiment tracking with wandb.

---

## 🎯 What This Is

A complete RAG pipeline:

**User question → ChromaDB finds relevant FAQ entries via semantic search → GPT-4o-mini generates a grounded answer**

Built as the Week 4 Capstone for the KI & Python module at Morphos GmbH.

---

## 🏆 Challenge Status

| Level | What | Status |
|---|---|---|
| 🥉 Bronze | ChromaDB setup + persistence test | ✅ Done |
| 🥈 Silver | FastAPI REST API + Gradio Web UI | ✅ Done |
| 🥇 Gold | RAG pipeline + wandb experiment tracking + embedding model comparison | ⬜ In Progress |
| 💎 Diamond | Tests + polished README + own fine-tuned model | ⬜ Bonus |

---

## 🗂️ Project Structure

```
ki-capstone-projekt/
├── config.py                  ← Central config — single source of truth
├── data/faq_data.py           ← 24 FAQ entries across 6 categories
├── scripts/
│   ├── 01_setup_db.py         ← ChromaDB setup
│   ├── 02_test_persistence.py ← Persistence tests
│   └── 03_evaluate.py         ← wandb evaluation pipeline (Gold)
├── rag/pipeline.py            ← semantic_search, wrap_search, ask_faq (Gold)
├── api/main.py                ← FastAPI server
├── ui/app.py                  ← Gradio web UI
└── tests/test_all.py          ← Smoke tests (Diamond)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- OpenAI API Key
- wandb Account + API Key

### Installation

```bash
git clone https://github.com/yourusername/ki-capstone-projekt.git
cd ki-capstone-projekt

python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### Environment Setup

Copy `.env.example` and fill in your keys:

```bash
cp .env.example .env
```

`.env.example`:
```
OPENAI_API_KEY=sk-...
WANDB_API_KEY=...
```

### Setup the Database

Run once to populate ChromaDB with the 24 FAQ entries:

```bash
python scripts/01_setup_db.py
```

---

## ▶️ Run the App

### FastAPI Server

```bash
uvicorn api.main:app --reload --port 8000
```

Swagger UI: `http://localhost:8000/docs`

Available endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | API health check |
| `/health` | GET | Status + document count |
| `/categories` | GET | All available FAQ categories |
| `/search` | GET | Semantic search (query, top_k, category) |
| `/ask` | POST | RAG pipeline — full AI answer *(Gold)* |

### Gradio Web UI

```bash
python ui/app.py
```

Local: `http://localhost:7860`

---

## 🛠️ Tech Stack

| Technology | Purpose | Why |
|---|---|---|
| **ChromaDB** | Vector Database | Local persistence, automatic embeddings |
| **FastAPI** | REST API | Automatic docs, type safety, async |
| **Gradio** | Web UI | Python function → Web app in one line |
| **OpenAI** | LLM (GPT-4o-mini) | Answer generation in the RAG pipeline |
| **wandb** | Experiment Tracking | Measure and compare search quality |
| **sentence-transformers** | Embedding Models | Model comparison for Gold challenge |

---

## 🔬 Gold — Embedding Model Comparison

A key focus of the Gold challenge is comparing embedding models with wandb:

| Model | Type |
|---|---|
| `all-MiniLM-L6-v2` | Baseline (English) |
| `paraphrase-multilingual-MiniLM-L12-v2` | Multilingual comparison |

The evaluation pipeline is modular — adding a new model = one new entry in a list, no logic changes.

---

## 📦 Dependencies

```
chromadb          # Vector database
fastapi           # REST API
uvicorn[standard] # ASGI server
gradio            # Web UI
wandb             # Experiment tracking
openai            # LLM API
python-dotenv     # Environment variables
sentence-transformers  # Embedding models
```

---

## ✏️ Author

**Dennis Feyerabend**
KI & Python Modul — Morphos GmbH — February 2026

---

## 📝 License

Created as part of an AI & Python training program at Morphos GmbH. Learning project for educational purposes.
