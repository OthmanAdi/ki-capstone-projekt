"""
FAQ Datensatz — Starter-Daten.

BRONZE: Diese 8 Einträge nutzen.
GOLD:   Mindestens 20 Einträge, mindestens 3 Kategorien.
        Eigene Einträge UNTEN hinzufügen.
"""

FAQ_DATA = [
    {
        "frage": "Wie kann ich mein Passwort zurücksetzen?",
        "antwort": "Klicken Sie auf 'Passwort vergessen' auf der Login-Seite. "
                   "Sie erhalten eine E-Mail mit einem Reset-Link. "
                   "Der Link ist 24 Stunden gültig.",
        "kategorie": "konto",
    },
    {
        "frage": "Was kostet das Premium-Abo?",
        "antwort": "Das Premium-Abo kostet 9,99 Euro pro Monat "
                   "oder 99 Euro pro Jahr (2 Monate gratis).",
        "kategorie": "preis",
    },
    {
        "frage": "Wie kündige ich mein Abonnement?",
        "antwort": "Gehen Sie zu Einstellungen > Abonnement > Kündigen. "
                   "Die Kündigung wird zum Ende der aktuellen Laufzeit wirksam.",
        "kategorie": "abo",
    },
    {
        "frage": "Welche Zahlungsmethoden werden akzeptiert?",
        "antwort": "Kreditkarte (Visa, Mastercard), PayPal und SEPA-Lastschrift.",
        "kategorie": "zahlung",
    },
    {
        "frage": "Wie kontaktiere ich den Kundenservice?",
        "antwort": "E-Mail: support@example.com oder Telefon: 0800-123456 "
                   "(Mo-Fr, 9-18 Uhr).",
        "kategorie": "support",
    },
    {
        "frage": "Kann ich mein Abo pausieren?",
        "antwort": "Ja, bis zu 3 Monate. "
                   "Einstellungen > Abonnement > Pausieren.",
        "kategorie": "abo",
    },
    {
        "frage": "Gibt es eine kostenlose Testversion?",
        "antwort": "Ja, 14-tägige kostenlose Testversion. "
                   "Keine Kreditkarte erforderlich.",
        "kategorie": "preis",
    },
    {
        "frage": "Wie ändere ich meine E-Mail-Adresse?",
        "antwort": "Einstellungen > Profil > E-Mail ändern. "
                   "Bestätigung per Link an die neue Adresse nötig.",
        "kategorie": "konto",
    },

    # ──────────────────────────────────────────────────────
    # Eigene Einträge (20+ total, 6 Kategorien)
    # ──────────────────────────────────────────────────────

    # --- konto ---
    {
        "frage": "Wie lösche ich meinen Account?",
        "antwort": "Einstellungen > Konto > Account löschen. "
                   "Alle Daten werden nach 30 Tagen unwiderruflich gelöscht. "
                   "Vorher können Sie Ihre Daten unter Einstellungen > Datenexport herunterladen.",
        "kategorie": "konto",
    },
    {
        "frage": "Kann ich meinen Benutzernamen ändern?",
        "antwort": "Ja, unter Einstellungen > Profil > Benutzername. "
                   "Der Name kann nur einmal alle 90 Tage geändert werden.",
        "kategorie": "konto",
    },
    {
        "frage": "Wie aktiviere ich die Zwei-Faktor-Authentifizierung?",
        "antwort": "Einstellungen > Sicherheit > 2FA aktivieren. "
                   "Sie benötigen eine Authenticator-App wie Google Authenticator oder Authy.",
        "kategorie": "konto",
    },

    # --- preis ---
    {
        "frage": "Gibt es einen Rabatt für Studenten?",
        "antwort": "Ja, Studenten erhalten 50% Rabatt auf alle Abos. "
                   "Verifizierung über SheerID mit gültiger Uni-E-Mail-Adresse.",
        "kategorie": "preis",
    },
    {
        "frage": "Was passiert nach Ablauf der Testversion?",
        "antwort": "Nach den 14 Tagen wird Ihr Konto automatisch auf den kostenlosen "
                   "Basic-Plan umgestellt. Es werden keine Kosten berechnet.",
        "kategorie": "preis",
    },
    {
        "frage": "Gibt es einen Familientarif?",
        "antwort": "Ja, der Familientarif kostet 14,99 Euro pro Monat für bis zu 5 Mitglieder. "
                   "Jedes Mitglied bekommt ein eigenes Profil.",
        "kategorie": "preis",
    },

    # --- abo ---
    {
        "frage": "Wie wechsle ich von monatlich auf jährlich?",
        "antwort": "Einstellungen > Abonnement > Plan ändern > Jährlich. "
                   "Der Restbetrag des aktuellen Monats wird anteilig verrechnet.",
        "kategorie": "abo",
    },
    {
        "frage": "Wird mein Abo automatisch verlängert?",
        "antwort": "Ja, alle Abos verlängern sich automatisch. "
                   "Sie erhalten 7 Tage vor Verlängerung eine Erinnerungs-E-Mail.",
        "kategorie": "abo",
    },

    # --- zahlung ---
    {
        "frage": "Kann ich eine Rechnung herunterladen?",
        "antwort": "Ja, unter Einstellungen > Zahlungen > Rechnungsverlauf. "
                   "Rechnungen sind als PDF verfügbar und enthalten alle steuerrelevanten Angaben.",
        "kategorie": "zahlung",
    },
    {
        "frage": "Was passiert bei einer fehlgeschlagenen Zahlung?",
        "antwort": "Bei fehlgeschlagener Zahlung wird der Versuch 3-mal innerhalb von 7 Tagen wiederholt. "
                   "Sie erhalten eine E-Mail-Benachrichtigung. Nach 7 Tagen wird das Abo pausiert.",
        "kategorie": "zahlung",
    },
    {
        "frage": "Kann ich meine Zahlungsmethode ändern?",
        "antwort": "Ja, unter Einstellungen > Zahlungen > Zahlungsmethode ändern. "
                   "Die neue Methode wird ab der nächsten Abrechnung verwendet.",
        "kategorie": "zahlung",
    },

    # --- support ---
    {
        "frage": "Wie lange dauert es bis der Support antwortet?",
        "antwort": "E-Mail-Anfragen werden innerhalb von 24 Stunden bearbeitet. "
                   "Premium-Kunden erhalten bevorzugten Support mit max. 4 Stunden Reaktionszeit.",
        "kategorie": "support",
    },
    {
        "frage": "Gibt es einen Live-Chat?",
        "antwort": "Ja, der Live-Chat ist für Premium-Kunden verfügbar, "
                   "Mo-Fr von 9-20 Uhr und Sa von 10-16 Uhr.",
        "kategorie": "support",
    },
    {
        "frage": "Wo finde ich die Hilfe-Dokumentation?",
        "antwort": "Unsere Wissensdatenbank finden Sie unter help.example.com. "
                   "Dort gibt es Anleitungen, Video-Tutorials und häufig gestellte Fragen.",
        "kategorie": "support",
    },

    # --- technik ---
    {
        "frage": "Welche Browser werden unterstützt?",
        "antwort": "Chrome, Firefox, Safari und Edge in der jeweils aktuellen Version. "
                   "Internet Explorer wird nicht mehr unterstützt.",
        "kategorie": "technik",
    },
    {
        "frage": "Gibt es eine mobile App?",
        "antwort": "Ja, für iOS (ab Version 15) und Android (ab Version 10). "
                   "Download im App Store oder Google Play Store.",
        "kategorie": "technik",
    },
    {
        "frage": "Wie viel Speicherplatz habe ich?",
        "antwort": "Basic: 5 GB, Premium: 50 GB, Familientarif: 100 GB. "
                   "Den aktuellen Verbrauch sehen Sie unter Einstellungen > Speicher.",
        "kategorie": "technik",
    },
    {
        "frage": "Funktioniert der Service auch offline?",
        "antwort": "Die mobile App bietet einen Offline-Modus für Premium-Kunden. "
                   "Inhalte können vorab heruntergeladen und ohne Internetverbindung genutzt werden.",
        "kategorie": "technik",
    },

    # --- datenschutz ---
    {
        "frage": "Wie kann ich meine Daten exportieren?",
        "antwort": "Einstellungen > Datenschutz > Datenexport. "
                   "Sie erhalten eine ZIP-Datei mit allen gespeicherten Daten innerhalb von 24 Stunden per E-Mail.",
        "kategorie": "datenschutz",
    },
    {
        "frage": "Werden meine Daten an Dritte weitergegeben?",
        "antwort": "Nein, Ihre Daten werden nicht an Dritte verkauft. "
                   "Wir nutzen ausschließlich anonymisierte Daten für die Verbesserung unseres Service. "
                   "Details finden Sie in unserer Datenschutzerklärung.",
        "kategorie": "datenschutz",
    },
    {
        "frage": "Wo werden meine Daten gespeichert?",
        "antwort": "Alle Daten werden auf Servern in der EU (Frankfurt) gespeichert. "
                   "Wir sind DSGVO-konform und ISO 27001 zertifiziert.",
        "kategorie": "datenschutz",
    },
]
