"""Build the Artifact fragment from index.html.

The Artifact host wraps the file in its own <!doctype>/<html>/<head>/<body>,
so strip our document wrapper and the head tags it already provides
(charset, viewport, preconnects). Everything else -- title, font stylesheet,
styles, markup, script -- carries over verbatim.

Every check below either passes silently or exits non-zero. Nothing here
prints a warning and then ships the file anyway.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
src = HERE / "index.html"
out = HERE / "artifact.html"


def die(msg):
    sys.exit("build-artifact: " + msg)


if not src.is_file():
    die(f"{src} not found")

html = src.read_text(encoding="utf-8")

# The body match is greedy, running to the LAST </body>. A non-greedy match
# stops at the first one, which silently truncates the fragment when a stray
# </body> sits mid-document -- the content just disappears with no error.
# Greedy keeps it in, where the stray-tag check below catches it.
m_head = re.search(r"<head>(.*?)</head>", html, re.S)
m_body = re.search(r"<body>(.*)</body>", html, re.S)
if not m_head:
    die("no <head>...</head> in index.html -- the document wrapper is malformed")
if not m_body:
    die("no <body>...</body> in index.html -- the document wrapper is malformed")

# head is matched non-greedily, so an early </head> would cut it short and
# drop whatever followed. Nothing but whitespace may sit between the two.
gap = html[m_head.end():m_body.start()]
if gap.strip():
    die("unexpected content between </head> and <body>: " + repr(gap.strip()[:60]))

head, body = m_head.group(1), m_body.group(1)

for pat in (r'\s*<meta charset="utf-8">',
            r'\s*<meta name="viewport"[^>]*>',
            r'\s*<link rel="preconnect"[^>]*>'):
    head = re.sub(pat, "", head)

fragment = head.strip() + "\n\n" + body.strip() + "\n"

# ── checks ───────────────────────────────────────────────────────────
# Match real wrapper tags, not substrings: the old test looked for "<head"
# and so fired on every <header> in the markup, which made it cry wolf on
# every build. Comments are dropped first, since a comment mentioning
# <body> is prose, not a tag.
visible = re.sub(r"<!--.*?-->", "", fragment, flags=re.S)
stray = sorted(set(re.findall(r"(?i)<!doctype|</?(?:html|head|body)\s*>", visible)))
if stray:
    die("wrapper tags survived the strip: " + ", ".join(stray))

if "<title>" not in fragment:
    die("no <title> -- the Artifact would be untitled")
if "fonts.googleapis.com" not in fragment:
    die("no Google Fonts link -- Baloo 2 / Plus Jakarta Sans / JetBrains Mono would fall back")

out.write_text(fragment, encoding="utf-8")
print(f"wrote {out.name}  {len(fragment)/1024:.1f} KB")
