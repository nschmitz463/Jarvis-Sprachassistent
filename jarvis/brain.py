"""Gesprächs-Logik über die Claude API (Anthropic)."""

import anthropic

from .config import config

SYSTEM_PROMPT = """Du bist Jarvis, ein freundlicher, leicht britisch-höflicher \
Sprachassistent. Antworte immer auf Deutsch.
Deine Antworten werden laut vorgelesen. Halte dich deshalb kurz (meist ein \
bis drei Sätze) und verwende keine Markdown-Formatierung, keine Listen, \
keine Emojis und keine Links. Schreibe Zahlen und Abkürzungen so, dass sie \
gut vorgelesen werden können."""

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
            return "Mein API-Schlüssel ist ungültig. Bitte prüfe die Datei .env."
        except anthropic.RateLimitError:
            self.messages.pop()
            return "Ich bekomme gerade zu viele Anfragen. Versuch es gleich noch einmal."
        except anthropic.APIConnectionError:
            self.messages.pop()
            return "Ich kann gerade keine Verbindung zum Internet herstellen."
        except anthropic.APIStatusError as e:
            self.messages.pop()
            print(f"API-Fehler {e.status_code}: {e.message}")
            return "Da ist leider etwas schiefgelaufen."

        if response.stop_reason == "refusal":
            self.messages.pop()
            return "Dabei kann ich leider nicht helfen."

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
