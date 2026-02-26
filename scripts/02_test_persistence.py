"""
BRONZE: Persistence Test
=========================
Beweist dass die Daten einen Neustart überleben.

WICHTIG: Erstellt einen NEUEN Client. Kein Zugriff auf den alten RAM.
Das ist der einzige korrekte Weg Persistence zu testen.

Ausführen: python scripts/02_test_persistence.py
Ergebnis:  Alle Tests bestanden ODER klare Fehlermeldung
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

# TODO: chromadb importieren


def test_persistence():
    """
    Erstellt einen KOMPLETT NEUEN Client und prüft:

    1. Collection existiert (get_collection, NICHT get_or_create!)
    2. Dokumente sind vorhanden (count > 0)
    3. Eine Test-Query gibt Ergebnisse zurück
    4. Metadaten sind korrekt (kategorie + antwort vorhanden)

    Ausgabe: [PASS] oder [FAIL] pro Test
    """

    # TODO: Implementieren
    pass


if __name__ == "__main__":
    test_persistence()
