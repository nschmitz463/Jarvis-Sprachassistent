"""Hauptschleife des Jarvis-Sprachassistenten.

Start:
    python -m jarvis          # Sprachmodus (Mikrofon + Lautsprecher)
    python -m jarvis --text   # Textmodus zum Testen über die Tastatur
"""

import argparse
import random
import re

from . import commands
from .config import config

FOLLOW_UP_SECONDS = 6  # so lange wartet Jarvis nach einer Antwort auf eine Rückfrage


def respond(text: str, brain) -> bool:
    """Verarbeitet eine Eingabe. Gibt False zurück, wenn Jarvis beenden soll."""
    result = commands.handle(text)
    if result:
        commands.announce(result.text)
        return not result.quit
    if re.search(r"\b(vergiss|neues gespräch|neues thema)\b", text.lower()):
        brain.reset()
        commands.announce("Erledigt, Sir. Ich habe alles vergessen. Diskretion ist mein zweiter Vorname.")
        return True
    commands.announce(brain.ask(text))
    return True


def strip_wake_word(text: str) -> str | None:
    """Gibt den Text nach dem Aktivierungswort zurück, oder None ohne Aktivierungswort."""
    lower = text.lower()
    idx = lower.find(config.wake_word)
    if idx == -1:
        return None
    return text[idx + len(config.wake_word):].strip(" ,.!?")


def run_text_mode(brain) -> None:
    commands.announce = lambda t: print(f"Jarvis: {t}")
    print("Textmodus – tippe deine Frage (\"beenden\" zum Verlassen).")
    while True:
        try:
            text = input("Du: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not text:
            continue
        request = strip_wake_word(text)
        if request == "":
            commands.announce(random.choice(commands.GREETINGS))
            continue
        if not respond(request if request is not None else text, brain):
            break


def run_voice_mode(brain) -> None:
    from .stt import Listener
    from .tts import speak

    commands.announce = speak
    listener = Listener()
    speak(f"Guten Tag, Sir. Rufen Sie einfach {config.wake_word.capitalize()}, wenn Sie etwas brauchen.")

    while True:
        heard = listener.listen()
        if not heard:
            continue
        print(f"(gehört: {heard})")
        request = strip_wake_word(heard)
        if request is None:
            continue
        if not request:  # nur "Jarvis" gesagt → auf die eigentliche Frage warten
            speak(random.choice(commands.GREETINGS))
            request = listener.listen(timeout=8)
            if not request:
                continue
            print(f"Du: {request}")

        # Gespräch fortführen, solange direkt weitergesprochen wird
        while request:
            if not respond(request, brain):
                return
            request = listener.listen(timeout=FOLLOW_UP_SECONDS)
            if request:
                print(f"Du: {request}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Jarvis-Sprachassistent")
    parser.add_argument("--text", action="store_true", help="Textmodus ohne Mikrofon")
    args = parser.parse_args()

    from .brain import Brain

    brain = Brain()
    try:
        if args.text:
            run_text_mode(brain)
        else:
            run_voice_mode(brain)
    except KeyboardInterrupt:
        pass
    print("Jarvis beendet.")


if __name__ == "__main__":
    main()
