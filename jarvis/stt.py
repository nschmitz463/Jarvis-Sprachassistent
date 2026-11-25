"""Spracherkennung (Speech-to-Text) über die Google-Spracherkennung."""

import speech_recognition as sr

from .config import config


class Listener:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.microphone = sr.Microphone()
        with self.microphone as source:
            print("Kalibriere Mikrofon auf Umgebungsgeräusche ...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

    def listen(self, timeout: float | None = None, phrase_limit: float = 10) -> str | None:
        """Hört auf einen Satz und gibt ihn als Text zurück (oder None)."""
        with self.microphone as source:
            try:
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_limit
                )
            except sr.WaitTimeoutError:
                return None
        try:
            return self.recognizer.recognize_google(audio, language=config.language)
        except sr.UnknownValueError:
            return None  # nichts Verständliches gesagt
        except sr.RequestError as e:
            print(f"Spracherkennung nicht erreichbar: {e}")
            return None
