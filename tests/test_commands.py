from unittest import mock

import pytest

from jarvis import commands
from jarvis.main import strip_wake_word


@pytest.mark.parametrize("text", ["Wie spät ist es?", "Sag mir die Uhrzeit"])
def test_uhrzeit(text):
    assert commands.handle(text).text.startswith("Es ist")


def test_datum():
    assert commands.handle("Welches Datum haben wir?").text.startswith("Heute ist")


def test_beenden():
    assert commands.handle("Tschüss").quit


@mock.patch("webbrowser.open")
def test_website(open_):
    assert commands.handle("Öffne YouTube").text == "Sehr wohl, Sir. Ich öffne Youtube."
    open_.assert_called_once_with("https://www.youtube.com")


@mock.patch("webbrowser.open")
def test_google_suche(open_):
    assert commands.handle("Suche nach Dart Regeln").text == "Sehr wohl, Sir. Ich suche nach dart regeln."
    assert "dart%20regeln" in open_.call_args[0][0]


@mock.patch("threading.Timer")
def test_timer(timer):
    assert commands.handle("Stell einen Timer auf fünf Minuten").text == "Sehr wohl, Sir. Timer auf 5 minuten gestellt."
    assert timer.call_args[0][0] == 300


def test_unbekannt_geht_an_claude():
    assert commands.handle("Erzähl mir etwas über Mars") is None


def test_wake_word():
    assert strip_wake_word("Jarvis, wie spät ist es?") == "wie spät ist es"
    assert strip_wake_word("Hey Jarvis") == ""
    assert strip_wake_word("Hallo zusammen") is None


def test_antworten_mit_sir():
    assert "Sir" in commands.handle("Wie spät ist es?").text
    assert "Sir" in commands.handle("Welches Datum haben wir?").text
    assert all("Sir" in g for g in commands.GREETINGS)
