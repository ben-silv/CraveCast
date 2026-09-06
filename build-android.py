"""Build the Android web assets from index.html.

index.html is the single source of truth for all three targets (web page,
Artifact, Android app). The app build differs in exactly one way: it must run
with no network, so the Google Fonts <link> is swapped for locally bundled
woff2 files. Everything else -- including the Capacitor detection that switches
alerting from an in-page timer to the OS scheduler -- is already in the source.

Run:  python build-android.py          (add --fonts to re-download the fonts)
"""
import re, sys, pathlib, urllib.request

SRC = pathlib.Path(r"C:\Users\silve\OneDrive\Desktop\Tracker\index.html")
WWW = pathlib.Path(r"C:\Users\silve\CraveCastApp\www")
FONTDIR = WWW / "fonts"

GF_CSS = ("https://fonts.googleapis.com/css2?"
          "family=Archivo:wdth,wght@75..125,400..800"
          "&family=IBM+Plex+Mono:wght@400;500;600"
          "&family=Public+Sans:ital,wght@0,300..700;1,400"
          "&display=swap")

# a modern UA is what makes Google serve woff2 + variable axes
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


def build_fonts():
    """Download every face referenced by the Google Fonts CSS, rewrite to local."""
    FONTDIR.mkdir(parents=True, exist_ok=True)
    css = fetch(GF_CSS)
    urls = sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css)))
    if not urls:
        raise SystemExit("no font urls found -- Google Fonts response changed?")

    mapping = {}
    for i, u in enumerate(urls):
        name = f"f{i:02d}.woff2" if u.endswith(".woff2") else f"f{i:02d}" + pathlib.Path(u).suffix
        (FONTDIR / name).write_bytes(fetch(u, binary=True))
        mapping[u] = name
        print(f"  {name:14} {len(( FONTDIR / name).read_bytes())/1024:7.1f} KB")

    for u, name in mapping.items():
        css = css.replace(u, name)
    (FONTDIR / "fonts.css").write_text(css, encoding="utf-8")
    print(f"  fonts.css      {len(css)/1024:7.1f} KB  ({len(mapping)} faces)")


def build_html():
    html = SRC.read_text(encoding="utf-8")
    new, n = re.subn(
        r'<link rel="preconnect"[^>]*>\s*',
        "", html)
    new, n2 = re.subn(
        r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]*">',
        '<link rel="stylesheet" href="fonts/fonts.css">',
        new)
    if n2 != 1:
        raise SystemExit(f"expected exactly 1 Google Fonts link, replaced {n2}")
    WWW.mkdir(parents=True, exist_ok=True)
    (WWW / "index.html").write_text(new, encoding="utf-8")
    print(f"  www/index.html {len(new)/1024:7.1f} KB  (dropped {n} preconnects)")


if __name__ == "__main__":
    if "--fonts" in sys.argv or not (FONTDIR / "fonts.css").exists():
        print("fonts:")
        build_fonts()
    else:
        print("fonts: cached (pass --fonts to refresh)")
    print("html:")
    build_html()
    print("done")
