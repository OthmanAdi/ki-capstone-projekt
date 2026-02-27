"""
Kategorie-Classifier — Optional laden und nutzen.

OPTIONAL: Wenn das trainierte Modell existiert, kann es benutzt werden.
          Wenn nicht, gibt predict_category() None zurück.
          Der Rest des Systems funktioniert ohne Änderung.

Nutzung in api/main.py oder ui/app.py:
    from fine_tune.classifier import predict_category

    kategorie = predict_category("Ich habe mein Passwort vergessen")
    # → "konto"  (wenn Modell trainiert)
    # → None     (wenn Modell nicht existiert)
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config


def predict_category(text: str) -> str | None:
    """
    Sagt die Kategorie einer FAQ-Frage voraus.

    Returns:
        str:  Kategorie-Name (z.B. "konto", "preis") wenn Modell existiert
        None: Wenn kein trainiertes Modell vorhanden ist

    Das Projekt funktioniert IMMER — mit oder ohne Modell.
    Wer diese Funktion aufruft, prüft einfach:

        kategorie = predict_category(query)
        if kategorie:
            # Modell hat eine Kategorie vorhergesagt → als Filter nutzen
            where_clause = {"kategorie": kategorie}
        else:
            # Kein Modell → kein Auto-Filter, normales Verhalten
            where_clause = None
    """

    model_path = Path(Config.CLASSIFIER_MODEL_PATH)
    label_map_path = model_path / "label_map.json"

    # Kein Modell? → None. System läuft weiter wie vorher.
    if not model_path.exists() or not label_map_path.exists():
        return None

    # TODO: Implementieren
    #
    # Schritte:
    # 1. label_map.json laden → {"konto": 0, "preis": 1, ...}
    # 2. Umkehren: {0: "konto", 1: "preis", ...}
    # 3. AutoTokenizer.from_pretrained(model_path)
    # 4. AutoModelForSequenceClassification.from_pretrained(model_path)
    # 5. inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    # 6. outputs = model(**inputs)
    # 7. predicted_id = outputs.logits.argmax(dim=-1).item()
    # 8. return id_to_label[predicted_id]
    #
    # Hints:
    # - import torch bei Bedarf
    # - model.eval() + torch.no_grad() für Inference
    # - try/except um Fehler abzufangen → return None bei Fehler

    return None
