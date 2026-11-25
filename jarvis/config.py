"""Konfiguration aus Umgebungsvariablen bzw. einer .env-Datei."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    wake_word: str = os.getenv("JARVIS_WAKE_WORD", "jarvis").lower()
    language: str = os.getenv("JARVIS_LANGUAGE", "de-DE")
    model: str = os.getenv("JARVIS_MODEL", "claude-opus-5-5")
    # Für Sprachantworten zählt Geschwindigkeit: "low" antwortet am schnellsten.
    effort: str = os.getenv("JARVIS_EFFORT", "low")

    @property
    def tts_language(self) -> str:
        """gTTS erwartet nur den Sprachcode, z. B. 'de' statt 'de-DE'."""
        return self.language.split("-")[0]


config = Config()
