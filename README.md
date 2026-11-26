# Jarvis-Sprachassistent

Ein deutschsprachiger KI-Butler: Sie sagen „Jarvis“, er antwortet mit
„Sir“ – höflich, charmant und mit trockenem Humor. Es gibt ihn als
**Web-App fürs Handy** (`web/`) und als **Python-App für den PC** (`jarvis/`).

## Auf dem Handy

Die Web-App läuft direkt im Handy-Browser – keine Installation nötig.

**Variante A – über claude.ai (ohne API-Schlüssel):**
Den veröffentlichten Jarvis-Link öffnen, auf „Zuhören starten“ tippen,
„Jarvis“ sagen. Claude antwortet über Ihren eigenen Claude-Zugang.
Freihändige Spracheingabe gibt es dort in **Chrome** (Android oder Desktop).
In Safari und in der Claude-App funktioniert die Spracheingabe nicht; dort kann
man aber das Mikrofon der Tastatur im Textfeld benutzen.

**Variante B – eigenständige Seite `web/index.html` (mit API-Schlüssel):**
Funktioniert auch auf dem iPhone (Safari) mit der Spracherkennung des
Browsers. Die Datei muss über HTTPS erreichbar sein, z. B.:

- GitHub Pages: Repository öffentlich machen, unter *Settings → Pages* den
  Branch und den Ordner wählen und dann `…/web/` öffnen.
  (Bei privaten Repositories braucht GitHub Pages ein kostenpflichtiges Konto.)
- oder den Ordner `web/` per Drag & Drop bei einem Static-Hosting-Dienst hochladen.

Beim ersten Öffnen den Anthropic-API-Schlüssel eintragen. Er bleibt nur auf
dem Handy gespeichert.

**Tipps fürs iPhone:**
- In **Safari** öffnen (nicht in der Claude-App) und das Mikrofon erlauben.
  Damit Safari nicht jedes Mal fragt: *Einstellungen → Apps → Safari →
  Mikrofon → Erlauben*.
- Während Jarvis spricht, ist das Mikrofon kurz aus. Er hört sich also nicht
  selbst und spricht über den Lautsprecher statt leise über die Hörmuschel.
- Bildschirm an lassen: Wird das iPhone gesperrt, hört Safari auf zuzuhören.
  Danach einfach wieder auf „Zuhören starten“ tippen.
- Optional „Hey Siri, Jarvis“: In der Kurzbefehle-App einen Kurzbefehl
  „Jarvis“ mit der Aktion *URL öffnen* (Adresse der Seite) anlegen.

`web/jarvis.html` ist der Quelltext der Seite, `web/index.html` wird daraus
mit `python web/build.py` erzeugt.

**Sprachbefehle in der Web-App:** „Jarvis“ (Begrüßung mit „Sir“), danach beliebige
Fragen an Claude; fest eingebaut sind Uhrzeit, Datum, „Timer auf 5 Minuten“,
„Neues Gespräch“ und „Schlafen“ (beendet das Zuhören).

## Auf dem PC (Python)

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
