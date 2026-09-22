"""Build the shared native web assets from index.html.

index.html is the single source of truth for every target (web page, Artifact,
iOS app, Android app). Capacitor keeps one webDir for all platforms, so this
script writes that directory once and `cap sync ios` / `cap sync android` each
copy the same output.

The native build differs from the web page in exactly one way: it must run with
no network, so the Google Fonts <link> is swapped for locally bundled woff2
files. Everything else -- including the Capacitor detection that switches
alerting from an in-page timer to the OS scheduler -- is already in the source.

The font families are read out of index.html's own <link>, not hard-coded here,
so changing a typeface in the source cannot leave the bundle behind.

Run:  python build-native.py          (add --fonts to re-download the fonts)
"""
import os, re, sys, pathlib, urllib.request

# The iOS half of this project is built on a Mac, so neither path is hard-coded.
# Defaults match the layout on this machine; override with TRACKER= / APP=.
HERE = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(os.environ.get("TRACKER", HERE)) / "index.html"
APP = pathlib.Path(os.environ.get("APP", pathlib.Path.home() / "CraveCastApp"))
WWW = APP / "www"
FONTDIR = WWW / "fonts"

GF_LINK = re.compile(
    r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/[^"]*)">')

# a modern UA is what makes Google serve woff2 + variable axes
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


def gf_url(html):
    m = GF_LINK.search(html)
    if not m:
        raise SystemExit("no Google Fonts <link> in index.html")
    return m.group(1).replace("&amp;", "&")


def build_fonts(url):
    """Download every face referenced by the Google Fonts CSS, rewrite to local."""
    FONTDIR.mkdir(parents=True, exist_ok=True)
    for stale in FONTDIR.glob("*"):
        stale.unlink()
    css = fetch(url)
    urls = sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css)))
    if not urls:
        raise SystemExit("no font urls found -- Google Fonts response changed?")

    fams = sorted(set(re.findall(r"font-family:\s*'([^']+)'", css)))
    print(f"  families: {', '.join(fams)}")

    mapping = {}
    for i, u in enumerate(urls):
        name = f"f{i:02d}.woff2" if u.endswith(".woff2") else f"f{i:02d}" + pathlib.Path(u).suffix
        (FONTDIR / name).write_bytes(fetch(u, binary=True))
        mapping[u] = name
        print(f"  {name:14} {len((FONTDIR / name).read_bytes())/1024:7.1f} KB")

    for u, name in mapping.items():
        css = css.replace(u, name)
    (FONTDIR / "fonts.css").write_text(css, encoding="utf-8")
    (FONTDIR / "source.txt").write_text(url, encoding="utf-8")
    print(f"  fonts.css      {len(css)/1024:7.1f} KB  ({len(mapping)} faces)")


def build_html(html):
    new, n = re.subn(r'<link rel="preconnect"[^>]*>\s*', "", html)
    new, n2 = GF_LINK.subn('<link rel="stylesheet" href="fonts/fonts.css">', new)
    if n2 != 1:
        raise SystemExit(f"expected exactly 1 Google Fonts link, replaced {n2}")
    WWW.mkdir(parents=True, exist_ok=True)
    (WWW / "index.html").write_text(new, encoding="utf-8")
    print(f"  www/index.html {len(new)/1024:7.1f} KB  (dropped {n} preconnects)")


if __name__ == "__main__":
    html = SRC.read_text(encoding="utf-8")
    url = gf_url(html)
    cached = FONTDIR / "source.txt"
    stale = not cached.exists() or cached.read_text(encoding="utf-8").strip() != url
    print("fonts:")
    if "--fonts" in sys.argv or stale:
        if stale and cached.exists():
            print("  bundled fonts are for a different family set -- refetching")
        build_fonts(url)
    else:
        print("  cached (pass --fonts to refresh)")
    print("html:")
    build_html(html)
    print("done")
