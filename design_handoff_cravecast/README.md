# Handoff: CraveCast — craving forecasting + garden reward

## Overview
CraveCast is an addiction-recovery app that forecasts when a craving is likely to hit, warns the user before it does, and turns every day they ride one out into a plant that grows in a persistent 3D garden. This handoff covers six mobile screens and a full responsive web app: dashboard (light + dark), quick-log flow, prediction result, history & trends, and My Garden.

The emotional target: **modern, calming, friendly but high-tech — serious and trustworthy, never clinical.**

## About the Design Files
The files in this bundle are **design references created in HTML** — prototypes showing intended look and behavior, not production code to copy directly. The task is to **recreate these designs in the target codebase's existing environment** (React Native, SwiftUI, React web, etc.) using its established patterns, component library, and styling approach. If no environment exists yet, choose the most appropriate framework for the product and implement there.

They are authored as "Design Components" — a single HTML file per design with a template plus a logic class. Ignore that wrapper format; read them for layout, values, copy, and interaction logic only.

## Fidelity
**High-fidelity.** Final colors, typography, spacing, radii, shadows, copy, and interactions are all specified. Recreate pixel-accurately using the codebase's existing primitives. Every hex value, font size, and animation timing below is taken directly from the prototypes.

---

## Design Tokens

### Color — brand
| Token | Hex | Use |
|---|---|---|
| Primary / teal | `#06B6D4` | Primary actions, active nav, selected chips |
| Primary deep | `#0891B2` | Button gradient end, link text |
| Primary shadow | `#0E7490` | Solid bottom edge on teal buttons; dark card gradient |
| Primary light | `#22D3EE` | Dark-mode primary |
| Primary pale | `#67E8F9` | Chart mid-values, dark-mode accent text |
| Primary tint bg | `#ECFEFF` | Icon wells, insight cards |
| Secondary / orange | `#F59E0B` | Risk ring fill, FAB, high-risk bars, rank progress |
| Secondary light | `#FBBF24` | Gradient end on orange |
| Secondary shadow | `#C2760A` | Solid bottom edge on orange FAB |
| Secondary deep | `#B45309` / `#92400E` | Warning text on amber chips |
| Amber chip bg | `#FEF3C7` | "Rising", "Peak", rank badges |
| Amber card bg | `#FFFBEB` → `#FFF7ED` | Rank progress card gradient |

### Color — garden (green family)
| Token | Hex | Use |
|---|---|---|
| Green | `#10B981` | Plant CTA, selected tray item, stage bars |
| Green deep | `#059669` | Plant button gradient end |
| Green shadow | `#047857` | Solid bottom edge on plant button; label text |
| Green light | `#34D399` / `#6EE7B7` | Dark-mode garden accents |
| Green head | `#064E3B` | Plant card headline (light) |
| Green sub | `#357266` | Plant card body (light) |
| Green tint | `#ECFDF5` / `#F0FDF4` | Plant card gradient start, selected tray bg |
| Sky (plot top) | `#DCF2FF` | Garden plot gradient start |
| Plot mid | `#E8F7EC` (58%) | Garden plot gradient mid |
| Plot base | `#D5EEDA` | Garden plot gradient end |
| Soil dark | `#A9D9AE` | Empty tile, checker A |
| Soil light | `#B7E2BB` | Empty tile, checker B |
| Soil planted dark | `#8FCB93` | Occupied tile, checker A |
| Soil planted light | `#9FD6A3` | Occupied tile, checker B |

### Color — status
| Token | Hex | Use |
|---|---|---|
| Calm / low | `#10B981` | Craving 1–3, low stress |
| Caution / mid | `#F59E0B` | Craving 4–6, medium stress |
| Alert / high | `#FB7185` / `#F43F5E` | Craving 7–10, high stress |
| Alert bg | `#FFE4E6` / text `#9F1239` | Rough-day chip |

### Color — light theme surfaces
| Token | Hex |
|---|---|
| Page bg | `#EAF2F1` |
| Phone screen bg | `#F3F8F8` |
| Card bg | `#FFFFFF` |
| Top bar bg | `rgba(255,255,255,.85)` + `backdrop-filter: blur(18px)` |
| Hairline border | `rgba(17,24,39,.08)` (cards use `.07`) |
| Ink (headings) | `#111827` |
| Soft (body) | `#5B6572` |
| Muted (labels) | `#8A94A0` |
| Well bg (inset) | `#F7FAFB` |
| Track bg (bars) | `#EDF1F3`; ring track `#E9EEF1` |
| Segmented bg | `#E2E9EA` (mobile `#E7ECEF`) |

### Color — dark theme surfaces
| Token | Hex |
|---|---|
| Page bg | `#0B1220` |
| Card bg | `#131C2B` |
| Top bar bg | `rgba(11,18,32,.88)` + blur(18px) |
| Hairline border | `rgba(255,255,255,.08)` |
| Ink | `#F3F4F6` |
| Soft | `#CBD5E1` (mobile `#94A3B8`) |
| Muted | `#64748B` |
| Well bg | `rgba(255,255,255,.04)` |
| Track bg | `rgba(255,255,255,.1)`; ring track `rgba(255,255,255,.09)` |

### Typography
Three families, loaded from Google Fonts:
- **Baloo 2** (600/700/800) — display face. ALL headings, numbers, button labels, nav labels, chips. This is what makes the app read friendly rather than clinical.
- **Plus Jakarta Sans** (400/500/600/700/800) — body copy, descriptions, helper text.
- **JetBrains Mono** (400/500/700) — small uppercase eyebrow labels, axis ticks, counters, timestamps.

Scale as used (mobile → web):
| Role | Spec |
|---|---|
| Page title | `800 24px` → `800 34px` Baloo 2, `letter-spacing:-.02em` |
| Greeting | `800 27px/1.18` → `800 34px/1.15` Baloo 2, `-.02em` |
| Hero number (risk) | `800 34px/1` ring, `800 86px/1` → `800 96px/1` result, `-.03em`/`-.05em` |
| Card title | `700 15–17px` → `700 17–18px` Baloo 2 |
| Step question | `700 20px/1.3` → `700 24px/1.3` Baloo 2 |
| Button label | `800 17px` → `800 18px` Baloo 2 |
| Body | `500 13–14px/1.5` → `500 14–15px/1.55` Plus Jakarta Sans |
| Helper / caption | `500 12–12.5px` Plus Jakarta Sans, muted |
| Eyebrow label | `500 10.5–11px` JetBrains Mono, `letter-spacing:.1em`, `text-transform:uppercase` |
| Chip / badge | `700 11–13.5px` Baloo 2 |
| Nav label | `700 10px` → `700 14px` Baloo 2 |

### Radius scale (deliberately round — this carries the "cute")
`7–8px` garden tiles · `14px` small controls · `16–18px` inner wells, tray items · `22px` collection cells, cope rows · `24px` stat cards · `26px` primary buttons, rank card · `28–30px` main cards · `30–32px` hero/plot cards · `100px` all pills, chips, progress bars, segmented controls · `50%` avatars, rings, plant wells · phone bezel `46px` outer / `37px` inner.

### Spacing
Base rhythm of 4px. Common: card padding `18–22px` mobile / `22–28px` web; card-to-card gap `14px` mobile / `18px` web; screen padding `20px` mobile / `24px` web (max-width `1240px` centered); grid gaps `9–12px`.

### Shadows
- Card lift: `0 10px 30px -18px rgba(9,24,38,.38)`
- Hero card (teal): `0 22px 44px -22px rgba(14,116,144,.9)`
- Garden plot: `0 16px 40px -26px rgba(6,95,70,.6)`
- Phone bezel: `0 26px 60px -18px rgba(9,24,38,.45), 0 2px 6px rgba(9,24,38,.18)`
- **Chunky button (signature)**: `0 5px 0 <shadowColor>, 0 16px 26px -16px <glow>` — a solid bottom edge plus a soft glow. On `:active` it becomes `transform: translateY(4px); box-shadow: 0 1px 0 <shadowColor>`, so the button physically presses into the page. Teal buttons use `#0E7490`, green `#047857`, orange `#C2760A`.
- Standing plant in the 3D plot: `filter: drop-shadow(0 5px 4px rgba(6,60,40,.35))`
- Occupied garden tile (block depth): `0 0 0 1.5px rgba(6,95,70,.22), 0 7px 0 -1px rgba(6,95,70,.28)`

### Keyframe animations
```css
@keyframes rise  { from{opacity:0;transform:translateY(14px)} to{opacity:1;transform:none} }      /* .5s ease both — card entrance */
@keyframes halo  { 0%,100%{transform:scale(1);opacity:.55} 50%{transform:scale(1.09);opacity:.16} } /* 3.4–3.8s ease-in-out infinite — breathing ring behind risk + plant */
@keyframes sheen { from{transform:translateX(-120%)} to{transform:translateX(220%)} }             /* 3.6s ease-in-out infinite — light sweep across primary CTA */
@keyframes sway  { 0%,100%{transform:rotate(-4deg)} 50%{transform:rotate(4deg)} }                 /* 4.2–6s ease-in-out infinite — plants, logo leaf, sun */
```
The sheen element is a `40%`-wide absolutely-positioned span inside the button: `linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent)`.

---

## Screens / Views

### 1. Dashboard / Home (light) — `1a`
**Purpose:** The daily landing. Answer "what's my risk right now?" and "what am I growing today?" in one glance, and make logging one tap away.

**Layout (mobile, 390×844):** vertical scroll, `20px` side padding, `108px` bottom padding to clear the tab bar. Order top to bottom:
1. **Greeting block** — eyebrow `Thu · Sep 19 · Evening` (mono, uppercase, `#8A94A0`); headline "Hey Ben 👋" on line 1, "how are you right now?" on line 2 at `font-weight:500`, color `#5B6572`. A `44px` circular avatar sits right, `linear-gradient(145deg,#06B6D4,#0E7490)`, white `800 15px` initial.
2. **Today's plant card** (see §"Plant card" below) — **this is the first card, above the risk ring.**
3. **Risk card** — white, radius `30px`, padding `22px 20px 18px`, with an absolutely-positioned overlay `linear-gradient(120deg,rgba(6,182,212,.07),rgba(245,158,11,.06))` for a faint iridescence. Contains:
   - **Risk ring**, `118px` square. Layers, outermost in: a `halo`-animated disc at `inset:-6px` in `rgba(245,158,11,.16)`; a `conic-gradient(#F59E0B <risk>%, #E9EEF1 0)` full-size; a white disc at `inset:11px` holding the number `800 34px` with a `17px` `%` in `#8A94A0`, and under it `WATCH` in `700 9.5px` JetBrains Mono, `letter-spacing:.12em`, `#B45309`.
   - Right column: amber pill "▲ Rising"; title "A bumpy stretch ahead" `700 17px/1.3`; body "Your usual 6–8 PM wobble starts in about 45 minutes. Nothing you haven't handled."
   - **"Why this number? 🤔" disclosure** — full-width well button (`#F7FAFB`, radius `18px`) with a `⌄` chevron that rotates `180deg` over `.25s`. Expands a `max-height` 0→`180px` + opacity transition (`.35s ease` / `.25s`) revealing three teal-check reasons.
4. **Stat pair** — two-column grid, `12px` gap. "Streak": big number + "days" + a `6px` progress bar `linear-gradient(90deg,#06B6D4,#10B981)` at `streak/30`. "This week": 18 logs + a 7-bar sparkline (bars `>=80` are orange, rest teal).
5. **Next 12 hours** — 8 bars in a `58px`-tall row, each with a mono hour tick below. Color by value: `>=70` `#F59E0B`, `>=45` `#67E8F9`, else `#CBD5E1`. Heights transition `.4s ease`.
6. **Quote card** — `linear-gradient(135deg,#ECFEFF,#F8FAFB)`, teal hairline, peer quote + attribution.

**Floating action button:** `58px` circle, `#F59E0B`, `+` glyph, fixed `right:20px; bottom:96px`, chunky shadow `0 4px 0 #C2760A, 0 12px 24px -10px rgba(245,158,11,.85)`.

**Tab bar:** 4-column grid, `rgba(255,255,255,.88)` + blur(18px), top hairline, padding `10px 14px 26px` (the 26px is the home-indicator inset). Items: 🏠 Home · ✍️ Log · 🌿 Garden · 📈 History. Active = full opacity icon + `#0891B2` label; inactive = `.45` opacity + `#9AA4AF`.

### 2. Dashboard (dark) — `1e`
Identical structure with the dark token set. Differences worth noting:
- Greeting is "Hey Ben 🌙", eyebrow reads `Thu · Sep 19 · Late`, and the state is the **falling** case: teal "▼ Falling" chip, "You rode out the peak 🌤️", ring label `EASING` in `#22D3EE`, risk 28%.
- Risk card gets a `200px` blurred teal orb at `top:-80px; right:-60px` in `rgba(34,211,238,.16)`.
- Avatar gradient flips to `linear-gradient(145deg,#22D3EE,#0E7490)` with dark `#06232B` text; primary buttons use dark ink on light teal/green for contrast.
- Bottom card is a "Tonight" note: early warning armed for 6:15 PM tomorrow.

### 3. Quick log — `1b`
**Purpose:** Capture craving intensity, mood, stress, and context in under a minute, with no page-to-page friction.

**Key interaction — one smooth scroll, not a wizard.** All four steps live in a single scrolling column. A **sticky header** holds the title "Quick log ✍️" and a `4px` progress rail whose width is driven by scroll position: `8 + 92 * (scrollTop / (scrollHeight - clientHeight))` percent, filled with `linear-gradient(90deg,#06B6D4,#F59E0B)`, transition `.25s ease`. The step counter text is `ceil(progress/25)` clamped to 1–4. Scrolling *is* the progress — implement with an onScroll listener, not step state.

**Step 1 — Craving intensity (1–10).** Emoji face at `38px` + the number at `800 56px`, both color-coded by `cravColor()`. Custom slider: a `10px` track with the full `linear-gradient(90deg,#10B981,#F59E0B,#FB7185)` at `.22` opacity, an opaque fill of the same gradient clipped to `(v-1)/9`, a `32px` white thumb with a `3px` border in the current status color, and a transparent native `<input type=range>` overlaid at `opacity:0` for accessibility and input. Track ends labelled "barely there" / "overwhelming".
Face map: `<=2 😊`, `<=4 🙂`, `<=6 😐`, `<=8 😟`, else `😣`. Color map: `<=3 #10B981`, `<=6 #F59E0B`, else `#F43F5E`.

**Step 2 — Mood (1–10) + stress.** Same slider pattern in teal→green, no emoji, with a word label: `<=2` "running on empty 🫠", `<=4` "a bit flat 😐", `<=6` "doing okay 🙂", `<=8` "pretty good 😄", else "great ✨". Stress is a 3-up grid of Low/Medium/High; selected fills with its status color, white text, and `transform:scale(1.03)`.

**Step 3 — Context.** Multi-select pill row: Alone, With others, Work, Home, Out, After work, Evening, Late night. Selected = `#06B6D4` fill, white text, `scale(1.03)`. All chips transition `all .18s ease`. Default selection: Alone, Home, After work.

**Step 4 — Optional note.** A single soft textarea well with placeholder "Had a tough meeting, feeling triggered…".

**Submit:** "Check my risk 💪", full-width chunky teal button, followed by reassurance copy "We'll save it and read your patterns — takes a second."

### 4. Prediction result — `1c`
**Purpose:** Deliver the number with enough transparency to be trusted, then immediately offer something to *do*.

- **Header row:** back chevron in a `34px` rounded-square, "Your reading ✨", right-aligned mono timestamp.
- **Hero card:** `linear-gradient(160deg,#0E7490,#155E75 55%,#1E3A46)`, radius `28px` (web `32px`), with a `190px` amber orb bleeding off the top-right at `rgba(245,158,11,.22)`, `filter:blur(6px)`. Centered: amber-outlined "Medium-high risk window" pill; the number at `800 86px` white with a `36px` `%` at `.6` opacity; explanatory line "Chance a strong urge shows up in the next two hours."; then a `9px` bar filled `linear-gradient(90deg,#22D3EE,#F59E0B)` that animates to width over `1s cubic-bezier(.2,.8,.2,1)`, with "calm" / "your usual peak · 74%" ticks. Card enters with `rise .55s`.
- **"Why we think so":** three rows, each a `22px` teal check tile + reason text + a `5px` confidence bar. Values: 86% orange / 72% teal / 38% pale teal.
- **"Things that might help 🌱":** three tappable cards — 📞 Call Maya ("Worked 4 of the last 5 times" · Call), 🚶 Walk the block ("Changing rooms breaks the loop" · Start), 🧘 5-minute breathing ("Guided, with a timer" · Open). Each has a `42px` tinted icon well (`#ECFEFF`, `#FFF7ED`, `#ECFDF5`), and on selection the border goes `#06B6D4` with `scale(1.015)`.
- **Footer actions:** "I've got this" (neutral) and "Remind me in 30 min" (amber), 50/50.
- **Privacy line:** "Built from your 118 logs. Stays on your phone, always. 🔒"

### 5. History & trends — `1d`
**Purpose:** Turn accumulated logs into a small number of statements the user can act on.

- **Header:** "Your patterns" + a Week/Month segmented control (active pill = white card on `#E7ECEF` with `0 2px 6px rgba(9,24,38,.12)`).
- **Week bar chart:** 7 bars, `96px` tall (web `150px`), value label above and day letter below each. `>=75` uses `linear-gradient(180deg,#F59E0B,#FBBF24)` with `#B45309` label, else `linear-gradient(180deg,#06B6D4,#67E8F9)` with `#0E7490`. Heights transition `.5s ease`. Values M–S: 42, 58, 35, 81, 66, 74, 49. Below: amber "Peak · Thu 7 PM · 81%" chip.
- **Heatmap:** 5 rows (M–F) × 6 columns (6a, 10a, 2p, 6p, 8p, 11p) as a `grid-template-columns: 26px repeat(6,1fr)` of square cells, radius `6px`. Six-step scale from `#ECFEFF` → `#CFF5FB` → `#8CE3F2` → `#FCD9A0` → `#F8B454` → `#FB7185` at thresholds 18/35/52/68/82, each with its own readable foreground.
- **Insight cards:** three tinted cards with mono eyebrows — Timing (teal), Combination (amber), What helps (green).
- **Recent days list:** rows of date + summary + a risk chip colored by band, with a `›` affordance.

### 6. My Garden — `1f`
**Purpose:** The reward loop and the reason to come back. This is the emotional center of the product.

**The 3D plot.** A real, manipulable isometric garden built in CSS 3D — not an illustration.
- Container: `perspective: 820px` (web `1000px`), `perspective-origin: 50% 42%`, `height:250px` (web `360px`), contents centered.
- Plane: `width:266px` (web `340px`), `transform-style: preserve-3d`, `transform: rotateX(60deg) rotateZ(<rot>deg) scale(<fit>)`, transition `.55s cubic-bezier(.3,.9,.3,1)`. Laid out as `display:grid; grid-template-columns: repeat(n,1fr); gap:5px`.
- **Fit scale is load-bearing:** when the plane rotates, its diagonal would overflow the card, so scale by `1 / (cos θ + sin θ)` where `θ = (rot mod 90)` in radians. At 0° this is 1; at 45° it is ~0.707. Without it, corners clip.
- Tiles: `aspect-ratio:1`, radius `7px`, checkerboarded by `(row + col) % 2`. Empty tiles are flat; occupied tiles gain a `7px` solid drop (`0 7px 0 -1px rgba(6,95,70,.28)`) so they read as raised blocks of soil.
- Plants: an emoji span absolutely centered in its tile and **counter-rotated back to face the camera** — `translate(-50%,-50%) rotateZ(-<rot>deg) rotateX(-60deg) translateY(-9px)` — so they stand upright out of the ground at any viewing angle, with a drop-shadow pooling on the soil.

**Editing.** A tray of the user's **unlocked** species (see §Unlock progression) plus 🪨 Stone and 🚿 Clear acts as a brush. Select one, then click any square to place it there; the Clear brush digs a square up and outlines empty tiles in `rgba(244,63,94,.35)` while active. The tray heading reflects the mode: "Planting: Tulip" / "Clearing squares".

**Layout controls.** `↺` and `↻` rotate the plot ±45° per press. A 4×4 / 5×5 / 6×6 segmented control resizes the plot; **each size keeps its own independent layout**, so switching back restores what was there.

**Surrounding content.** Rank badge (see §Unlock progression); a plot counter ("Your plot · N planted"); a `24px` swaying ☀️ in the corner; a "Growing today" card mirroring the dashboard plant; a **Next unlock** progress card; and the **Collection** grid of all 28 species — owned cells are white with a green hairline and teal label, locked cells are grey with `grayscale(1)` at `.38` opacity and the label shows the requirement ("18 grown") rather than a generic "Locked". Footer: "Nothing already grown is ever taken away. 💚"

---

## Unlock progression (species catalog)
New species are earned by **total plants successfully grown** (`grownCount`) — one per clean day. This is the long-arc retention loop: there is always a next thing coming.

Single source of truth — `[emoji, name, grownRequired]`:

| # | Species | Unlocks at | | # | Species | Unlocks at |
|---|---|---|---|---|---|---|
| 1 | 🌻 Sunflower | 0 | | 15 | 🪻 Bluebell | 16 |
| 2 | 🌷 Tulip | 0 | | 16 | 🪷 Lotus | 18 |
| 3 | 🌿 Herb | 0 | | 17 | 🌾 Wheat | 20 |
| 4 | 🌼 Daisy | 0 | | 18 | 🎋 Bamboo | 22 |
| 5 | 🍀 Clover | 2 | | 19 | 🍁 Maple | 24 |
| 6 | 🌹 Rose | 4 | | 20 | 🌴 Palm | 26 |
| 7 | 🌵 Cactus | 5 | | 21 | 🍄 Toadstool | 28 |
| 8 | 🌺 Hibiscus | 7 | | 22 | 🌰 Chestnut | 30 |
| 9 | 🌳 Oak | 8 | | 23 | 🎄 Spruce | 32 |
| 10 | 🌲 Pine | 10 | | 24 | 🪵 Log bench | 34 |
| 11 | 🌸 Cherry | 12 | | 25 | 🐝 Beehive | 38 |
| 12 | 🪴 Fern | 14 | | 26 | 🐔 Chicken | 42 |
| 13 | — | — | | 27 | 🐰 Rabbit | 46 |
| 14 | — | — | | 28 | 🦆 Duck 50 · 🐑 Sheep 55 · 🐈 Barn cat 60 |

Spacing is deliberate: four free starters, then every 1–2 days early (fast, visible reward), stretching to every 4–5 days in the animal tier (long-term goals). Flowers and trees alternate so neither runs out.

**Derived values — compute these, never hard-code:**
```js
unlocked   = CATALOG.filter(c => grown >= c.at)
nextLock   = CATALOG.find(c => grown < c.at)          // undefined when complete
prevAt     = last unlocked threshold (0 if none)
unlockPct  = round(100 * (grown - prevAt) / (nextLock.at - prevAt))
```

**Where unlocks surface — three places, all driven by the same list:**
1. **Dashboard species picker** — shows only `unlocked` species. The row grows as the user progresses, so the picker itself is a visible record of their streak.
2. **Garden tray** — `unlocked` species plus two always-available utilities: 🪨 Stone (decor) and 🚿 Clear (erase brush).
3. **Collection grid** — the full catalog. Locked cells stay visible and greyed, labelled with their requirement, so the goal is always legible.

**Next unlock card** (amber gradient card in the garden): heading "Next unlock · <name> <emoji>", a `grown / required` mono counter, a `9px` amber progress bar animating `width` over `.5s ease`, and the line "N more blooms and the <species> joins your seed tray." (singular "bloom" at N = 1). When everything is unlocked: "Every species unlocked. Your garden is complete. 🏆"

**Rank badge** — a title derived from the same counter: Sprout (0–9) → Grower (10–23) → Cultivator (24–39) → Master gardener (40+). Shown in the garden header beside the collection count.

**Product note:** unlocks should be permanent and never revocable — the privacy/safety line "Nothing already grown is ever taken away" is a deliberate anti-shame commitment. A relapse ends a *streak*; it must not delete a *garden*.

### Plant card (appears on Dashboard light, Dashboard dark, and Garden)
The core daily ritual. **Placed at the top of the dashboard, above the risk ring** — planting is the primary action; logging a craving is secondary.

- Container: `linear-gradient(160deg,#F0FDF4,#ECFEFF)`, `1.5px` border `rgba(16,185,129,.28)`, radius `30px`, with a `150px` green orb bleeding off the top-right.
- Header row: mono eyebrow "Today's plant" + a green status chip showing the growth clock.
- Body: an `88px` circular well (halo-animated ring, white inner disc, swaying plant emoji) beside the headline, subcopy, and a 4-segment stage bar.
- **Species picker:** horizontally scrollable row of `62px` cards — one per **unlocked** species, so the row lengthens as the user progresses. Unselected are desaturated (`filter: saturate(.5)`) on a translucent background; the selected one goes opaque white with a green border and `scale(1.05)`.
- **CTA:** before planting, "Plant my tulip 🌱" (label tracks the chosen species). After planting it becomes "Water it 💧", then "Blooming 🌸" at the final stage. Chunky green button with the sheen sweep.
- **Secondary link:** "Having a craving? Log it 💧" — quiet text button, `700 13px` Baloo 2, `#5B8B80`.

**Growth model:** four stages, emoji `🌱 → 🌿 → 🪴 → <species>`, with the icon scaling `26 → 32 → 38 → 44px` (web `30 → 38 → 44 → 52px`) over `.4s cubic-bezier(.2,1.4,.4,1)` — a slight overshoot so each advance feels earned. Stage bar segments fill green, with the final segment amber. Clock labels: "just planted" / "4h in" / "growing well" / "in bloom". In production the stages should advance on elapsed clean time, not taps; the prototype advances on press so reviewers can see all four.

---

## The web app (`CraveCast Web.dc.html`)
Same product, desktop-first responsive layout, same tokens.

- **Sticky top bar:** logo (🌱 swaying + "Crave" in ink, "Cast" in `#06B6D4`), pill nav (Home / Log / Garden / History — active pill is solid `#06B6D4` with white text), then a **light/dark toggle** and a user chip on the right. The toggle themes the entire page through the token map; every surface, border, and text color is driven from it.
- **Home:** two columns via `repeat(auto-fit,minmax(340px,1fr))` — plant card left, risk ring + stat trio + forecast right. Stats become a third card ("Garden · 14 grown"). Collapses to one column below ~700px.
- **Garden:** plot card (`340px` plane, `rotateX(58deg)`) beside a column holding the tray, rank progress, and the collection grid (`repeat(auto-fill,minmax(86px,1fr))`).
- **Log:** single `720px` centered column; submitting navigates to the result view.
- **History:** two-up charts, then a 3-up insight row, then the recent-days list.
- **Result:** `760px` centered; reasons and coping cards side by side.
- Content max-width `1240px`, `24px` gutters, `26px 24px 72px` main padding. All tracks use `minmax`/`auto-fit` and wrap — nothing is fixed-width.

---

## Interactions & Behavior

| Interaction | Behavior |
|---|---|
| Any primary button press | `translateY(4px)` + shadow collapses to `0 1px 0` over `.12s` — the "chunky press". Small controls use `translateY(2px)` / `scale(.97)`. |
| Primary CTA idle | `sheen` light sweep every `3.6s`. |
| Risk ring / plant well | `halo` breathing pulse, `3.4–3.8s`, infinite. |
| Plants, logo leaf, sun | `sway` ±4° rotation, `4.2–6s`, staggered per plant by index so the garden doesn't move in lockstep. |
| Card entrance | `rise` `.5s ease both`. |
| "Why this number?" | Chevron rotates `180deg`; body expands via `max-height` + `opacity`. |
| Sliders | Fill and thumb follow at `.12s`; the status color crossfades at `.3s`. |
| Chips / pills / tray items | `all .18s ease`, selected scales to `1.03–1.06`. |
| Quick-log progress rail | Driven by scroll offset, `.25s ease` width. |
| Garden rotate | `.55s cubic-bezier(.3,.9,.3,1)`; plants counter-rotate in the same transition. |
| Garden tile click | Places or clears the current brush; hover brightens the tile (`filter: brightness(1.07)`, web only). |
| Plot resize | Swaps to that size's stored layout. |
| Risk number on load | Counts up from 0 to target over `900–1100ms` with cubic ease-out. **Guard this:** only run when `document.visibilityState === 'visible'`, and set the final value on a timeout backstop, so a backgrounded tab or an export never captures 0%. |

**Reduced motion:** honor `prefers-reduced-motion` — drop `halo`, `sway`, `sheen`, and the count-up; keep state-change transitions.

---

## State Management

```
view            'home' | 'log' | 'result' | 'garden' | 'history'   (web only; mobile is separate screens)
dark            boolean — theme toggle (web)
craving         1–10
mood            1–10
stress          'Low' | 'Medium' | 'High'
picked          string[] — context tags
why             boolean — risk explanation expanded
cope            number — index of selected coping card, -1 for none
range           'Week' | 'Month'
chosen          species id for today's plant (must be an unlocked species)
grownCount      number (prop, default 14) — total plants grown; drives every unlock
planted         boolean
stage           0–3 growth stage
plot            4 | 5 | 6 — garden size
rot             rotation in degrees (multiples of 45)
brush           emoji string, or 'erase'
layouts         { 4: string[16], 5: string[25], 6: string[36] } — one saved layout per plot size
riskScore       number (prop, default 65)
streakDays      number (prop, default 12)
```

**Transitions:** submitting the log → result view. Tapping a species → `chosen`. Tapping the CTA → `planted:true, stage:0`, then `stage+1` capped at 3. Tapping a tile → writes `brush` (or `''`) into `layouts[plot][index]`. Rotate → `rot ± 45`.

**Data the real app needs:** current risk score + trend direction, an hourly forecast series, streak and log counts, a week-by-day series, a day×hour risk matrix, ranked contributing factors with weights, personalized coping strategies with efficacy, the total grown count (which derives the entire unlock state — persist the counter, not a list of unlocked ids), and the saved plot layouts per plot size. The prototypes hard-code representative values — every number here is placeholder data, not a real model output.

---

## Assets
No image or icon files. All iconography is **system emoji** (plants, animals, weather, activity glyphs) and CSS-drawn shapes (conic-gradient ring, gradient bars, CSS-3D tiles). Fonts come from Google Fonts: Baloo 2, Plus Jakarta Sans, JetBrains Mono.

If the target platform needs consistent cross-device rendering, replace emoji with a licensed icon or illustration set — the garden species in particular would benefit from real art. The layout assumes roughly square glyphs at the sizes given.

---

## Files
| File | Contents |
|---|---|
| `CraveCast Mockups.dc.html` | All six mobile screens in one canvas: `1a` dashboard light, `1b` quick log, `1c` prediction result, `1d` history & trends, `1e` dashboard dark, `1f` my garden. Fully interactive. Both prototypes expose a `grownCount` control (0–60) — slide it to preview any point in the unlock progression. |
| `CraveCast Web.dc.html` | Responsive web app — all five views plus the light/dark toggle. |
| `CraveCast Mockups v1.dc.html` | Earlier revision, before the friendlier pass and the garden. Reference only. |
| `support.js` | Runtime for the prototype file format. Not part of the design; do not port. |

Open any `.dc.html` directly in a browser to interact with it. Read the template for markup and inline styles, and the logic class at the bottom for state, color mapping, and data.
