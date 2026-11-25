"""Sprachausgabe (Text-to-Speech) über Google TTS (gTTS) und pygame."""

import io

from gtts import gTTS

from .config import config

_mixer_ready = False


def _init_mixer():
    global _mixer_ready
    if not _mixer_ready:
        import pygame

        pygame.mixer.init()
        _mixer_ready = True


def speak(text: str) -> None:
    """Gibt den Text auf der Konsole aus und spricht ihn vor."""
    print(f"Jarvis: {text}")
    if not text.strip():
        return
    try:
        buffer = io.BytesIO()
        gTTS(text=text, lang=config.tts_language).write_to_fp(buffer)
        buffer.seek(0)

        import pygame

        _init_mixer()
        pygame.mixer.music.load(buffer, "mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    except Exception as e:  # Sprachausgabe darf den Assistenten nicht abstürzen lassen
        print(f"(Sprachausgabe fehlgeschlagen: {e})")
