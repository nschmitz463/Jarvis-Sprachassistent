"""Erzeugt web/index.html (eigenständige Seite) aus web/jarvis.html.

jarvis.html ist der Seiteninhalt ohne <html>/<head>-Gerüst, so wie er auch
als claude.ai-Artifact veröffentlicht wird. index.html ergänzt das Gerüst,
damit die Seite auf jedem Webserver (z. B. GitHub Pages) läuft.
"""

from pathlib import Path

here = Path(__file__).parent
body = (here / "jarvis.html").read_text(encoding="utf-8")
head = (
    '<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="theme-color" content="#0b0f17">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
    "body{margin:0}[hidden]{display:none!important}</style>\n"
    "</head>\n<body>\n"
)
(here / "index.html").write_text(head + body + "\n</body>\n</html>\n", encoding="utf-8")
print("web/index.html geschrieben")
