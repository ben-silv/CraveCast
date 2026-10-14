"""Build index.html -- the published web page -- from app.html plus the Apple layer.

The layer lives in apple/ -- apple.css after the base stylesheet, apple.js
after the base script -- so the web page always tracks the real app
instead of being a fork that drifts. The Google Fonts request is dropped,
since the layer sets type in the system face.

Every check below either passes silently or exits non-zero.
"""
import re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
src = HERE / "app.html"
css = HERE / "apple" / "apple.css"
js = HERE / "apple" / "apple.js"
out = HERE / "index.html"


def die(msg):
    sys.exit("build-apple: " + msg)


for f in (src, css, js):
    if not f.is_file():
        die(f"{f} not found")

html = src.read_text(encoding="utf-8")

# exactly one of each anchor, or the splice lands somewhere unintended
for tag in ("</style>", "</head>", "</body>"):
    n = html.count(tag)
    if n != 1:
        die(f"expected one {tag} in app.html, found {n}")

fonts = r'\s*<link rel="preconnect" href="https://fonts\.g[^>]*>|\s*<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>'
html, dropped = re.subn(fonts, "", html)
if dropped != 3:
    die(f"expected to drop 3 font tags (2 preconnects + stylesheet), dropped {dropped}")

html = html.replace("</head>",
                    '<style id="apple-layer">\n' + css.read_text(encoding="utf-8") + "</style>\n</head>")
html = html.replace("</body>",
                    '<script id="apple-motion">\n' + js.read_text(encoding="utf-8") + "</script>\n</body>")

out.write_text(html, encoding="utf-8")
print(f"wrote {out.name}  {len(html)/1024:.1f} KB")
