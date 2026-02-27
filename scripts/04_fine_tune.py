"""
GOLD/DIAMOND: Kategorie-Classifier Fine-Tuning
================================================
Trainiert ein deutsches BERT-Modell das automatisch erkennt
zu welcher Kategorie eine FAQ-Frage gehört.

OPTIONAL: Das Projekt funktioniert OHNE dieses Script.
          Wenn das trainierte Modell existiert, nutzt die API es automatisch.
          Wenn nicht, funktioniert alles wie vorher.

Ausführen: python scripts/04_fine_tune.py
Ergebnis:  ./models/kategorie_classifier/ mit trainiertem Modell
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from data.faq_data import FAQ_DATA

# TODO: Imports
#   from transformers import AutoTokenizer, AutoModelForSequenceClassification
#   from transformers import TrainingArguments, Trainer
#   from datasets import Dataset
#   import numpy as np
#   from sklearn.metrics import accuracy_score, f1_score, classification_report


def prepare_data():
    """
    Bereitet die FAQ-Daten für Fine-Tuning vor.

    Schritte:
    1. Aus FAQ_DATA die Fragen und Kategorien extrahieren
    2. Kategorien zu numerischen Labels mappen
       - kategorien = sorted(set(item["kategorie"] for item in FAQ_DATA))
       - label_map = {kat: i for i, kat in enumerate(kategorien)}
    3. Dataset erstellen:
       - texts = [item["frage"] for item in FAQ_DATA]
       - labels = [label_map[item["kategorie"]] for item in FAQ_DATA]
    4. Train/Test Split (80/20)
       - dataset = Dataset.from_dict({"text": texts, "label": labels})
       - split = dataset.train_test_split(test_size=0.2, seed=42)
    5. Return: split, label_map, kategorien

    WICHTIG: Ihr braucht mindestens 20 FAQ-Einträge damit das sinnvoll ist.
             Mit 8 Einträgen ist das Dataset zu klein für echtes Training.
             → GOLD Level: 20+ Einträge in data/faq_data.py hinzufügen!
    """

    # TODO: Implementieren
    pass


def tokenize_data(split, tokenizer):
    """
    Tokenisiert das Dataset.

    Hints:
    - def tokenize_fn(examples):
          return tokenizer(examples["text"], truncation=True, max_length=128, padding="max_length")
    - tokenized = split.map(tokenize_fn, batched=True)
    """

    # TODO: Implementieren
    pass


def compute_metrics(eval_pred):
    """
    Berechnet Accuracy und F1 — kennt ihr von Woche 2.

    Hints:
    - logits, labels = eval_pred
    - predictions = np.argmax(logits, axis=-1)
    - return {"accuracy": accuracy_score(labels, predictions),
    -         "f1": f1_score(labels, predictions, average="weighted")}
    """

    # TODO: Implementieren
    pass


def train():
    """
    Fine-Tuned den Kategorie-Classifier.

    Schritte:
    1. prepare_data() aufrufen → split, label_map, kategorien
    2. Tokenizer laden: AutoTokenizer.from_pretrained(Config.CLASSIFIER_BASE_MODEL)
    3. Model laden: AutoModelForSequenceClassification.from_pretrained(
           Config.CLASSIFIER_BASE_MODEL, num_labels=len(kategorien))
    4. tokenize_data() aufrufen
    5. TrainingArguments definieren:
       - output_dir=Config.CLASSIFIER_MODEL_PATH
       - num_train_epochs=Config.CLASSIFIER_EPOCHS
       - per_device_train_batch_size=8
       - per_device_eval_batch_size=16
       - learning_rate=2e-5
       - eval_strategy="epoch"
       - save_strategy="epoch"
       - load_best_model_at_end=True
       - metric_for_best_model="f1"
    6. Trainer erstellen + trainer.train()
    7. Model + Tokenizer speichern nach Config.CLASSIFIER_MODEL_PATH
    8. label_map speichern (JSON) nach Config.CLASSIFIER_MODEL_PATH / "label_map.json"
    9. classification_report ausgeben

    HINWEIS: report_to="wandb" hinzufügen wenn ihr wandb Tracking wollt!
    """

    print("=" * 50)
    print("KATEGORIE-CLASSIFIER FINE-TUNING")
    print("=" * 50)

    print(f"\nFAQ Einträge: {len(FAQ_DATA)}")
    if len(FAQ_DATA) < 15:
        print(f"\n⚠ WARNUNG: Nur {len(FAQ_DATA)} Einträge.")
        print("  Für sinnvolles Training braucht ihr mindestens 20.")
        print("  → Mehr Einträge in data/faq_data.py hinzufügen!")

    kategorien = sorted(set(item["kategorie"] for item in FAQ_DATA))
    print(f"Kategorien: {kategorien}")
    print(f"Base Model: {Config.CLASSIFIER_BASE_MODEL}")
    print(f"Output: {Config.CLASSIFIER_MODEL_PATH}")

    # TODO: Implementieren (Schritte 1-9 oben)
    print("\n❌ Noch nicht implementiert. Füllt die TODOs aus!")


if __name__ == "__main__":
    train()
