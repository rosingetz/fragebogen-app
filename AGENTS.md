# AGENTS.md – Fragebogen-App (Psychometrisches Recruiting-Tool)

## Projekt
Interaktive Web-App zur Soft-Skill-Erfassung für Vorarbeiter im gewerblich-technischen Bereich.

## Tech-Stack
- **Python 3** + **Streamlit** (Frontend & Server)
- **Plotly** (Radar-Charts)
- **SQLite** (Datenhaltung)

## Projektstruktur
```
Fragebogen-App/
├── app.py              # Hauptanwendung (Streamlit)
├── questions.py        # Fragenkatalog (15 Fragen, 4 Kategorien)
├── database.py         # SQLite-Zugriff (Vorarbeiter + Bewerber)
├── scoring.py          # Benchmark-Berechnung + Matching-Algorithmus
├── requirements.txt    # Abhängigkeiten
└── data/
    └── responses.db    # SQLite-Datenbank (automatisch erstellt)
```

## Architektur
### Phasen
1. **PHASE 1 (IST-Analyse):** Bestands-Vorarbeiter füllen Fragebogen aus → Daten werden in SQLite gespeichert → Benchmark wird berechnet
2. **PHASE 2 (Matching):** Bewerber füllen Fragebogen aus → System vergleicht mit Benchmark → Radar-Chart + Übereinstimmung in %

### Datenfluss
```
Fragebogen → JSON-String → SQLite (vorarbeiter/bewerber Tabelle)
Benchmark ← AVG über alle Vorarbeiter pro Kategorie
Matching ← |Abweichung| / 4 * 100 → % pro Kategorie + Gesamt %
```

### Algorithmus
- **Pro-Kategorie-Score:** Mittelwert der Fragen-Antworten (1–5)
- **Benchmark:** Arithmetisches Mittel aller Vorarbeiter-Scores pro Kategorie
- **Match %:** `max(0, (1 - |bewerber - benchmark| / 4) * 100)` — pro Kategorie
- **Gesamt-Match:** Mittelwert aller Kategorien

## Datenbank-Schema
```sql
CREATE TABLE vorarbeiter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT (datetime('now','localtime')),
    profile_name TEXT DEFAULT '',
    answers TEXT NOT NULL  -- JSON
);
CREATE TABLE bewerber (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT (datetime('now','localtime')),
    answers TEXT NOT NULL  -- JSON
);
```

## Start
```bash
cd ~/Dokumente/Projekte/Fragebogen-App
pip install --break-system-packages streamlit plotly
streamlit run app.py
# → http://localhost:8501
```

## Admin-Funktionen
- Sidebar → Admin-Bereich
- Daten exportieren (JSON-Download)
- Einzelne/alle Datensätze löschen

## Skills / Kategorien
1. **Führungskompetenz & Durchsetzungsvermögen** (Fragen 1–4)
2. **Organisations- & Methodenkompetenz** (Fragen 5–8)
3. **Sozial- & Kommunikationskompetenz** (Fragen 9–12)
4. **Fachliche & persönliche Zuverlässigkeit** (Fragen 13–15)

## Status
- [x] Fragenkatalog (15 Fragen)
- [x] App-Code (Streamlit + Plotly + SQLite)
- [x] Matching-Algorithmus
- [x] Admin-Bereich (Export, Löschen)
- [ ] Phase 1: Datenerfassung Vorarbeiter
- [ ] Phase 2: Bewerber-Matching mit Live-Visualisierung
