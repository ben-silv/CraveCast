"""Build the Artifact fragment from index.html.

The Artifact host wraps the file in its own <!doctype>/<html>/<head>/<body>,
so strip our document wrapper and the head tags it already provides
(charset, viewport, preconnects). Everything else -- title, font stylesheet,
styles, markup, script -- carries over verbatim.
"""
import re, pathlib

src = pathlib.Path(r"C:\Users\silve\OneDrive\Desktop\Tracker\index.html")
out = pathlib.Path(r"C:\Users\silve\OneDrive\Desktop\Tracker\artifact.html")

html = src.read_text(encoding="utf-8")

head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
body = re.search(r"<body>(.*?)</body>", html, re.S).group(1)

for pat in (r'\s*<meta charset="utf-8">',
            r'\s*<meta name="viewport"[^>]*>',
            r'\s*<link rel="preconnect"[^>]*>'):
    head = re.sub(pat, "", head)

fragment = head.strip() + "\n\n" + body.strip() + "\n"
out.write_text(fragment, encoding="utf-8")

# sanity: no wrapper tags survived
bad = [t for t in ("<!doctype", "<html", "<head", "<body", "</html>", "</body>", "</head>")
       if t in fragment.lower()]
print("wrote", out, len(fragment), "bytes")
print("stray wrapper tags:", bad or "none")
print("has <title>:", "<title>" in fragment)
print("has fonts link:", "fonts.googleapis.com" in fragment)
