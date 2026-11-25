"""Feste Befehle, die ohne KI sofort beantwortet werden.

Jeder Befehl ist eine Funktion, die den erkannten Text bekommt und entweder
eine Antwort (str) zurückgibt oder None, wenn sie nicht zuständig ist.
Alles, was kein fester Befehl übernimmt, geht an Claude.
"""

import re
import threading
import urllib.parse
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from typing import Callable

WOCHENTAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
MONATE = [
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
]

WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "wikipedia": "https://de.wikipedia.org",
    "github": "https://github.com",
    "netflix": "https://www.netflix.com",
    "spotify": "https://open.spotify.com",
}

ZAHLWOERTER = {
    "eine": 1, "einen": 1, "ein": 1, "zwei": 2, "drei": 3, "vier": 4, "fünf": 5,
    "sechs": 6, "sieben": 7, "acht": 8, "neun": 9, "zehn": 10, "fünfzehn": 15,
    "zwanzig": 20, "dreißig": 30,
}


@dataclass
class Result:
    text: str
    quit: bool = False


# Wird von main.py gesetzt, damit ein abgelaufener Timer sprechen kann.
announce: Callable[[str], None] = print


def cmd_beenden(text: str):
    if re.search(r"\b(beenden|tschüss|auf wiedersehen|schlafen|ausschalten)\b", text):
        return Result("Bis später.", quit=True)


def cmd_uhrzeit(text: str):
    if re.search(r"\b(uhrzeit|wie spät|wieviel uhr|wie viel uhr)\b", text):
        now = datetime.now()
        return Result(f"Es ist {now.hour} Uhr {now.minute:02d}.")


def cmd_datum(text: str):
    if re.search(r"\b(datum|welcher tag|welches datum|den wievielten)\b", text):
        now = datetime.now()
        return Result(
            f"Heute ist {WOCHENTAGE[now.weekday()]}, der {now.day}. "
            f"{MONATE[now.month - 1]} {now.year}."
        )


def cmd_google_suche(text: str):
    m = re.search(r"(?:google|suche nach|such nach|suche)\s+(?:nach\s+)?(.+)", text)
    if m and not re.search(r"\böffne\b", text):
        query = m.group(1).strip()
        webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote(query))
        return Result(f"Ich suche nach {query}.")


def cmd_website(text: str):
    m = re.search(r"\b(?:öffne|starte|zeig mir)\s+(\w+)", text)
    if m and m.group(1) in WEBSITES:
        name = m.group(1)
        webbrowser.open(WEBSITES[name])
        return Result(f"Ich öffne {name.capitalize()}.")


def _parse_number(word: str) -> int | None:
    if word.isdigit():
        return int(word)
    return ZAHLWOERTER.get(word)


def cmd_timer(text: str):
    m = re.search(r"timer.*?(\d+|\w+)\s+(sekunde|sekunden|minute|minuten|stunde|stunden)\b", text)
    if not m:
        return None
    amount = _parse_number(m.group(1))
    if amount is None:
        return None
    unit = m.group(2)
    seconds = amount * (1 if unit.startswith("sekunde") else 60 if unit.startswith("minute") else 3600)
    t = threading.Timer(seconds, lambda: announce("Dein Timer ist abgelaufen."))
    t.daemon = True
    t.start()
    return Result(f"Timer auf {amount} {unit} gestellt.")


COMMANDS = [cmd_beenden, cmd_uhrzeit, cmd_datum, cmd_timer, cmd_website, cmd_google_suche]


def handle(text: str) -> Result | None:
    """Versucht, den Text als festen Befehl auszuführen."""
    text = text.lower().strip()
    for command in COMMANDS:
        result = command(text)
        if result:
            return result
    return None
