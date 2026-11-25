# Jarvis-Sprachassistent

Ein deutschsprachiger Sprachassistent für den PC, geschrieben in Python.

- **Aktivierungswort:** „Jarvis“ (z. B. „Jarvis, wie spät ist es?“)
- **Spracherkennung:** Google Speech Recognition (über `SpeechRecognition`)
- **Sprachausgabe:** Google Text-to-Speech (`gTTS`), abgespielt mit `pygame`
- **Feste Befehle:** werden sofort und ohne KI beantwortet
- **Alles andere:** beantwortet Claude (Anthropic API) – mit Gesprächsgedächtnis

## Feste Befehle

| Beispiel | Aktion |
|---|---|
| „Wie spät ist es?“ | Uhrzeit ansagen |
| „Welches Datum haben wir?“ | Datum ansagen |
| „Stell einen Timer auf fünf Minuten“ | Timer, Ansage bei Ablauf |
| „Öffne YouTube“ | Website öffnen (YouTube, Google, Wikipedia, GitHub, Netflix, Spotify) |
| „Suche nach Dart Regeln“ | Google-Suche im Browser |
| „Neues Gespräch“ / „Vergiss das“ | Gesprächsverlauf mit Claude zurücksetzen |
| „Tschüss“ / „Beenden“ | Jarvis beenden |

Nach einer Antwort hört Jarvis noch einige Sekunden weiter zu – Rückfragen
gehen also ohne erneutes „Jarvis“.

## Installation

Voraussetzung: Python 3.10 oder neuer.

```bash
git clone https://github.com/nschmitz463/Jarvis-Sprachassistent.git
cd Jarvis-Sprachassistent
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

**PyAudio (Mikrofon) braucht unter Umständen Systempakete:**

- Windows: `pip install pyaudio` funktioniert normalerweise direkt.
- macOS: `brew install portaudio`
- Linux (Debian/Ubuntu): `sudo apt install portaudio19-dev python3-dev`

## Einrichtung

1. `.env.example` nach `.env` kopieren.
2. API-Key von https://console.anthropic.com/ bei `ANTHROPIC_API_KEY` eintragen.

Optionale Einstellungen in der `.env`:

| Variable | Standard | Bedeutung |
|---|---|---|
| `JARVIS_WAKE_WORD` | `jarvis` | Aktivierungswort |
| `JARVIS_LANGUAGE` | `de-DE` | Sprache für Erkennung und Ausgabe |
| `JARVIS_MODEL` | `claude-opus-5-5` | Claude-Modell |
| `JARVIS_EFFORT` | `low` | Denkaufwand (`low` = schnellste Antworten, bis `max`) |

## Starten

```bash
python -m jarvis          # Sprachmodus mit Mikrofon
python -m jarvis --text   # Textmodus zum Testen über die Tastatur
```

## Projektstruktur

```
jarvis/
  main.py      Hauptschleife, Aktivierungswort, Text-/Sprachmodus
  commands.py  feste Befehle (hier neue Befehle ergänzen)
  brain.py     Anbindung an Claude
  stt.py       Spracherkennung
  tts.py       Sprachausgabe
  config.py    Einstellungen aus .env
tests/         Tests für die festen Befehle (pytest)
```

### Eigenen Befehl hinzufügen

In `jarvis/commands.py` eine Funktion schreiben, die bei passendem Text ein
`Result` zurückgibt, und sie in die Liste `COMMANDS` eintragen:

```python
def cmd_hallo(text: str):
    if "guten morgen" in text:
        return Result("Guten Morgen! Ich hoffe, du hast gut geschlafen.")
```

## Tests

```bash
pip install pytest
pytest
```
