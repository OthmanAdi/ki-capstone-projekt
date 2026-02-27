# Capstone Projekt: German AI FAQ Assistant
## KI & Python Modul — Woche 4, Donnerstag + Freitag

**Dauer:** 2 Tage
**Ziel:** Ein vollständiges RAG-System. Alles zusammen. Ein Produkt.
**Format:** Funktionierender Code + GitHub + Live Demo

---

# WAS IHR DIESE WOCHE GEMACHT HABT

```
MONTAG:     ChromaDB — Vector Database, Persistence, Metadata Filtering
DIENSTAG:   FastAPI + Gradio + wandb — API, UI, Tracking
MITTWOCH:   Fine-Tuning — Eigenes Modell trainieren und deployen

JETZT:      Alles zusammen. Ein System. Nicht Fragmente.
```

**Der Unterschied:** Ihr habt jedes Tool einzeln gelernt. Jetzt beweist ihr dass ihr sie ZUSAMMEN benutzen könnt. Das ist was ein AI Engineer im Job macht.

---

# PRIORITÄTEN

| Priorität | Level | Wann | Was ihr macht |
|-----------|-------|------|---------------|
| MUSS | **BRONZE** | Donnerstag | ChromaDB Setup + Persistence Test + Search |
| SOLLTE | **SILVER** | Donnerstag | FastAPI + Gradio — euer System hat eine URL |
| KANN | **GOLD** | Freitag | RAG Pipeline + wandb + eigene Daten (20+) |
| BONUS | **DIAMOND** | Freitag | Poliertes Portfolio-Stück + Tests + Deployment |

**BRONZE + SILVER = Pflicht. Donnerstag Abend muss das laufen.**

---

# BEVOR IHR ANFANGT

## 1. Branch erstellen

```bash
git clone https://github.com/OthmanAdi/ki-capstone-projekt.git
cd ki-capstone-projekt
git checkout -b EUER_NAME/capstone
```

Ab jetzt arbeitet ihr NUR auf eurem Branch. Nie auf `main`.

## 2. Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Python 3.10-3.13 erforderlich. Python 3.14 funktioniert NICHT mit ChromaDB.**

Falls ihr Python 3.14 habt:
```bash
py -3.13 -m venv .venv
```

## 3. API Keys

```bash
cp .env.example .env
```

Tragt eure Keys ein. `.env` wird NIE committed — steht in `.gitignore`.

---

# BRONZE — ChromaDB Setup + Search
## Pflicht | Donnerstag | 2-3 Stunden

### Was ihr macht

1. **`data/faq_data.py`** — die 8 Starter-Einträge verstehen, 5 eigene hinzufügen
2. **`scripts/01_setup_db.py`** — ChromaDB PersistentClient, Daten migrieren
3. **`scripts/02_test_persistence.py`** — Persistence mit NEUEM Client beweisen

### Was in `01_setup_db.py` drin sein muss

```
[ ] chromadb importieren
[ ] Path(Config.DB_PATH).mkdir(parents=True, exist_ok=True)
[ ] client = chromadb.PersistentClient(path=Config.DB_PATH)
[ ] collection = client.get_or_create_collection(name=Config.COLLECTION_NAME)
[ ] Schleife über FAQ_DATA mit collection.upsert()
[ ] Partial Failure Handling: try/except pro Item
[ ] failed_items Liste — am Ende berichten
[ ] Print: wie viele erfolgreich / fehlgeschlagen
```

### Was in `02_test_persistence.py` drin sein muss

```
[ ] NEUER PersistentClient (nicht den gleichen wie in setup!)
[ ] Test 1: Collection existiert (get_collection, nicht get_or_create!)
[ ] Test 2: count() > 0
[ ] Test 3: Query gibt Ergebnisse
[ ] Test 4: Metadaten haben "kategorie" und "antwort"
[ ] Klare Ausgabe: [PASS] oder [FAIL] pro Test
```

### BRONZE Checkliste

- [ ] `python scripts/01_setup_db.py` — läuft ohne Fehler
- [ ] `python scripts/02_test_persistence.py` — alle Tests PASS
- [ ] `./faq_database/` Ordner existiert
- [ ] Mindestens 13 Einträge in der Collection (8 Starter + 5 eigene)

---

# SILVER — FastAPI + Gradio
## Sollte | Donnerstag | 2-3 Stunden

### Was ihr macht

1. **`api/main.py`** — REST API mit 4 Endpoints
2. **`ui/app.py`** — Gradio Interface mit Search

### Was in `api/main.py` drin sein muss

```
[ ] FastAPI App mit Config.API_TITLE
[ ] ChromaDB Client + Collection laden
[ ] Warnung wenn collection.count() == 0
[ ] Pydantic Models: SearchResult, SearchResponse
[ ] GET /          → API Info
[ ] GET /health    → Status + Dokumenten-Anzahl
[ ] GET /search    → Semantic Search mit query, top_k, kategorie
[ ] GET /categories → Alle Kategorien aus den Metadaten
[ ] Input-Validierung: leere Query → 400, top_k Range → 400
```

### Was in `ui/app.py` drin sein muss

```
[ ] ChromaDB Client + Collection laden
[ ] search_faq() Funktion: query → formatiertes Markdown
[ ] Ähnlichkeit in Prozent: round((1 - distance) * 100)
[ ] gr.Interface mit Textbox, Slider, Dropdown
[ ] Kategorie-Filter: "Alle" = kein Filter
[ ] Mindestens 3 Examples
[ ] demo.launch(share=True)
```

### Testen

**Terminal 1:**
```bash
uvicorn api.main:app --reload --port 8000
```

**Terminal 2:**
```bash
python ui/app.py
```

- `http://localhost:8000/docs` — Swagger UI, alle Endpoints testen
- `http://localhost:7860` — Gradio UI, Suche testen
- Beide gleichzeitig offen

### SILVER Checkliste

- [ ] FastAPI startet auf Port 8000
- [ ] `/docs` zeigt Swagger UI mit allen 4 Endpoints
- [ ] `/search?query=Passwort` gibt Ergebnisse zurück
- [ ] `/search?query=` gibt HTTP 400 zurück
- [ ] `/categories` zeigt eure echten Kategorien
- [ ] Gradio startet auf Port 7860
- [ ] Search gibt formatierte Ergebnisse mit Ähnlichkeit in %
- [ ] Kategorie-Dropdown filtert korrekt
- [ ] `share=True` — öffentliche URL funktioniert

---

# GOLD — RAG Pipeline + wandb
## Kann | Freitag | 2-3 Stunden

### Was ihr macht

1. **`rag/pipeline.py`** — Vollständige RAG Pipeline
2. **`api/main.py`** — neuer POST `/ask` Endpoint
3. **`ui/app.py`** — "KI-Antwort" Funktion hinzufügen
4. **`scripts/03_evaluate.py`** — wandb Experiment Tracking
5. **`data/faq_data.py`** — auf 20+ Einträge erweitern

### Was in `rag/pipeline.py` drin sein muss

```
[ ] ask_faq(query, collection, top_k) → dict
[ ] Schritt 1: collection.query() → top_k Ergebnisse
[ ] Schritt 2: Kontext als String bauen (Frage + Antwort pro Ergebnis)
[ ] Schritt 3: System-Prompt + User-Prompt + Kontext
[ ] Schritt 4: openai.OpenAI().chat.completions.create()
[ ] Schritt 5: return {"answer": ..., "sources": ..., "query": ...}
[ ] Fail Fast: if not os.getenv("OPENAI_API_KEY") → Fehlermeldung
```

### Was in `03_evaluate.py` drin sein muss

```
[ ] load_dotenv()
[ ] ChromaDB laden
[ ] wandb.init(project=Config.WANDB_PROJECT)
[ ] Mindestens 8 Test-Queries
[ ] Pro Query: distance, similarity, category_match loggen
[ ] Zusammenfassung: avg_similarity, category_accuracy
[ ] wandb.finish()
```

### GOLD Checkliste

- [ ] `python scripts/03_evaluate.py` — läuft, wandb Dashboard sichtbar
- [ ] POST `/ask` Endpoint in FastAPI funktioniert
- [ ] RAG-Antwort in Gradio sichtbar
- [ ] 20+ FAQ-Einträge in der Collection
- [ ] Mindestens 3 verschiedene Kategorien

---

# DIAMOND — Portfolio-Qualität
## Bonus | Freitag | 2+ Stunden

### Beide

- [ ] `python tests/test_all.py` — alle Tests PASS
- [ ] README.md vollständig: Was, Warum, Wie, Tech Stack, Screenshots
- [ ] Code: sauber, kommentiert, keine Copy-Paste-Reste

### Dennis (AI/ML Engineer)

- [ ] Embedding Model Vergleich: `all-MiniLM-L6-v2` vs `paraphrase-multilingual-MiniLM-L12-v2`
- [ ] Vergleich in wandb Table loggen
- [ ] Evaluation mit 10+ Test-Queries, Metriken dokumentiert
- [ ] In README: "Nach X Experimenten hat sich Modell Y als besser erwiesen, weil..."

### Sebastian (Applied AI / Full Stack)

- [ ] `ui/app.py` mit `gr.Blocks` statt `gr.Interface`
- [ ] Zwei Tabs: "Suche" und "KI-Antwort"
- [ ] HuggingFace Spaces Deployment (permanente URL)
- [ ] In README: Live-Demo Link

---

# ABGABE

## Wie ihr abgebt

1. Alle Änderungen committen:
```bash
git add -A
git commit -m "capstone: [EUER LEVEL] fertig"
```

2. Branch pushen:
```bash
git push origin EUER_NAME/capstone
```

3. Ahmad Bescheid sagen: "Branch ist fertig."

## Was abgegeben wird

```
[ ] Code läuft (mindestens BRONZE + SILVER)
[ ] Persistence Test besteht
[ ] FastAPI + Gradio laufen gleichzeitig
[ ] Mindestens 13 FAQ-Einträge
[ ] Keine API Keys im Code (.env in .gitignore)
```

---

# TROUBLESHOOTING

### Python Version — ChromaDB startet nicht

**Problem:** `pydantic.v1.errors.ConfigError` oder `unable to infer type`

**Ursache:** Python 3.14 ist nicht kompatibel mit ChromaDB.

**Lösung:**
```bash
# Prüfe deine Version:
python --version

# Wenn 3.14: benutze 3.13 oder 3.12
py -3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

### collection.count() ist 0

**Ursache:** `faq_database/` Ordner existiert nicht oder falscher Pfad.

**Lösung:**
```bash
# Zuerst Setup ausführen:
python scripts/01_setup_db.py

# Prüfen:
python -c "import chromadb; c = chromadb.PersistentClient(path='./faq_database'); print(c.get_or_create_collection('faq').count())"
```

---

### ModuleNotFoundError: No module named 'config'

**Ursache:** Python findet die Projekt-Module nicht.

**Lösung:** Immer vom Projekt-Root ausführen:
```bash
cd ki-capstone-projekt
python scripts/01_setup_db.py    # Richtig
cd scripts && python 01_setup_db.py  # Falsch!
```

---

### FastAPI: uvicorn findet app nicht

**Problem:** `Error loading ASGI app`

**Lösung:**
```bash
# Vom Projekt-Root:
uvicorn api.main:app --reload --port 8000

# NICHT:
cd api && uvicorn main:app --reload
```

---

### FastAPI + Gradio gleichzeitig

Zwei separate Terminals. Beide gleichzeitig offen lassen:

```
Terminal 1:  uvicorn api.main:app --reload --port 8000
Terminal 2:  python ui/app.py
```

FastAPI: `http://localhost:8000`
Gradio:  `http://localhost:7860`

---

### Gradio Dropdown — keine Ergebnisse

**Ursache:** Kategorie-Namen sind case-sensitive. `"Konto"` ≠ `"konto"`.

**Lösung:** Prüfe die echten Werte:

```python
import chromadb

client = chromadb.PersistentClient(path="../faq_database")
collection = client.get_collection("faq")
data = collection.get(include=["metadatas"])
kategorien = set(m["kategorie"] for m in data["metadatas"])
print(kategorien)  # Diese Werte in den Dropdown!
```

---

### wandb Login

```bash
# Option 1: Terminal
wandb login EUER_API_KEY

# Option 2: .env
WANDB_API_KEY=euer_key

# Wichtig: load_dotenv() VOR wandb.init()!
```

---

### OpenAI API Key fehlt

```bash
# In .env:
OPENAI_API_KEY=sk-...

# Im Code: load_dotenv() ganz oben!
```

---

### Port schon belegt

```bash
# FastAPI auf anderem Port:
uvicorn api.main:app --reload --port 8001

# Gradio auf anderem Port:
# In app.py: demo.launch(server_port=7861, share=True)
```

---

### Git: .env versehentlich committed

```bash
# Aus Git-History entfernen:
git rm --cached .env
git commit -m "remove .env from tracking"

# Prüfen dass .gitignore korrekt ist:
cat .gitignore | grep .env
```

---

# KARRIERE-RELEVANZ

| Was ihr gebaut habt | Job-Bezeichnung | Gehalt (DE) |
|---------------------|-----------------|-------------|
| ChromaDB + Semantic Search | AI Engineer | 65.000 - 95.000 |
| FastAPI REST API | Backend Engineer | 55.000 - 85.000 |
| Gradio ML Demo | ML Engineer | 60.000 - 90.000 |
| RAG Pipeline | AI Engineer | 70.000 - 100.000 |
| wandb Experiment Tracking | ML Engineer | 65.000 - 95.000 |
| **Alles zusammen** | **AI Engineer** | **75.000 - 110.000** |

---

*Ahmad Othman Adi — Morphos GmbH, KI & Python Modul, Woche 4 Capstone*
