"""Render assets/icon.png -- the 1024x1024 App Store icon.

Same mark as the Android adaptive icon (the forecast ridge: a foothill, a peak,
and the moment the warning fires), but rebuilt for iOS, which differs in two
ways that matter. There is no adaptive mask, so the mark is scaled up to fill
the canvas instead of hiding inside a 72/108 safe zone; and Apple rejects any
icon carrying an alpha channel, so this is flattened to opaque RGB.

The Android background is still Capacitor's stock teal grid. This uses the
app's own palette instead.

Run:  python make-icon.py
"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Circle
from PIL import Image

OUT = pathlib.Path(__file__).resolve().parent / "assets" / "icon.png"
PX = 1024

BG     = "#FBF4E3"   # --bg, the app's paper
RIDGE  = "#E09A4C"   # the forecast curve
PEAK   = "#C64F36"   # --r5, the top of the scale: where a warning fires
RING   = "#FBF4E3"
BASE   = "#8C5A24"

# the ridge, transcribed from ic_launcher_foreground.xml (108x108 viewport)
VERTS = [
    (23, 74),
    (30, 74), (32, 64), (40, 62),
    (47, 60.5), (48, 70), (55, 68),
    (63, 65.5), (62, 33), (70, 33),
    (77, 33), (79, 54), (85, 58),
    (85, 77), (23, 77), (23, 74),
]
CODES = [Path.MOVETO,
         Path.CURVE4, Path.CURVE4, Path.CURVE4,
         Path.CURVE4, Path.CURVE4, Path.CURVE4,
         Path.CURVE4, Path.CURVE4, Path.CURVE4,
         Path.CURVE4, Path.CURVE4, Path.CURVE4,
         Path.LINETO, Path.LINETO, Path.CLOSEPOLY]

# the mark's own bounds, so the framing does not depend on the 108 canvas
X0, X1, Y0, Y1 = 23, 85, 22.5, 79.5
FILL = 0.72                      # share of the icon the mark spans
cx, cy = (X0 + X1) / 2, (Y0 + Y1) / 2
half = max(X1 - X0, Y1 - Y0) / FILL / 2

fig = plt.figure(figsize=(PX / 100, PX / 100), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(cx - half, cx + half)
ax.set_ylim(cy + half, cy - half)     # SVG y grows downward
ax.axis("off")
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.add_patch(PathPatch(Path(VERTS, CODES), facecolor=RIDGE, edgecolor="none"))
ax.add_patch(plt.Rectangle((23, 77), 62, 2.5, facecolor=BASE, edgecolor="none"))
ax.add_patch(Circle((70, 27), 6.4, facecolor=RING, edgecolor="none"))
ax.add_patch(Circle((70, 27), 4.5, facecolor=PEAK, edgecolor="none"))

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=100, facecolor=BG)
plt.close(fig)

# Apple rejects an alpha channel outright -- flatten to opaque RGB.
im = Image.open(OUT).convert("RGB").resize((PX, PX), Image.LANCZOS)
im.save(OUT, "PNG")
print(f"{OUT}  {im.size[0]}x{im.size[1]}  mode={im.mode}  {OUT.stat().st_size/1024:.1f} KB")
