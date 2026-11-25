"""Gesprächs-Logik über die Claude API (Anthropic)."""

import anthropic

from .config import config

SYSTEM_PROMPT = """Du bist JARVIS, ein KI-Butler mit trockenem britischen Humor. \
Du sprichst Deutsch.
Regeln für jede Antwort:
- Sprich den Nutzer immer mit »Sir« an und sieze ihn.
- Sei höflich, charmant und lustig: eine kleine geistreiche Bemerkung oder ein \
Augenzwinkern pro Antwort, nie gemein oder albern.
- Deine Antworten werden laut vorgelesen: höchstens drei kurze Sätze, keine \
Markdown-Formatierung, keine Listen, keine Emojis, keine Links.
- Die Eingaben kommen aus einer Spracherkennung und können Hörfehler \
enthalten. Rate wohlwollend, was gemeint war."""

MAX_HISTORY_TURNS = 20  # ältere Gesprächsrunden werden verworfen


class Brain:
    def __init__(self) -> None:
        self.client = anthropic.Anthropic()  # liest ANTHROPIC_API_KEY
        self.messages: list[dict] = []

    def reset(self) -> None:
        self.messages = []

    def ask(self, text: str) -> str:
        self.messages.append({"role": "user", "content": text})
        try:
            response = self.client.beta.messages.create(
                model=config.model,
                max_tokens=16000,
                system=SYSTEM_PROMPT,
                messages=self.messages,
                output_config={"effort": config.effort},
                # Lehnt das Modell eine Anfrage ab, übernimmt automatisch ein
                # passendes Ersatzmodell.
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            )
        except anthropic.AuthenticationError:
            self.messages.pop()
            return "Mein Schlüssel passt leider nicht ins Schloss, Sir. Bitte prüfen Sie die Datei .env."
        except anthropic.RateLimitError:
            self.messages.pop()
            return "Ich brauche eine kurze Verschnaufpause, Sir. Fragen Sie mich gleich noch einmal."
        except anthropic.APIConnectionError:
            self.messages.pop()
            return "Ich erreiche gerade meinen Verstand nicht, Sir. Ist das Internet verbunden?"
        except anthropic.APIStatusError as e:
            self.messages.pop()
            print(f"API-Fehler {e.status_code}: {e.message}")
            return "Verzeihung, Sir, da ist etwas schiefgelaufen."

        if response.stop_reason == "refusal":
            self.messages.pop()
            return "Darauf antworte ich lieber nicht, Sir. Ein guter Butler weiß, wann er schweigt."

        # Vollständigen Inhalt anhängen (inkl. Thinking-Blöcken), damit das
        # Gespräch korrekt fortgesetzt werden kann.
        self.messages.append({"role": "assistant", "content": response.content})
        self._trim_history()

        return " ".join(b.text for b in response.content if b.type == "text").strip()

    def _trim_history(self) -> None:
        # Immer ganze Runden (user + assistant) entfernen, damit die Historie
        # mit einer user-Nachricht beginnt.
        while len(self.messages) > MAX_HISTORY_TURNS * 2:
            self.messages = self.messages[2:]
