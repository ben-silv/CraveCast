# CraveCast — project brief

Context document for an assistant answering questions about this project.
Everything here is current as of 2026-09-07.

---

## What it is

A craving-forecasting app for someone trying to quit something. It predicts
when an urge is likely to hit, warns ahead of it, and turns each day the user
rides one out into a plant or animal growing in a garden.

**One self-contained `index.html`.** No framework, no build step, no runtime
dependencies. Roughly 3,000 lines: CSS, markup and JS in a single file. That
file is the source for three targets:

| Target | How it is produced | Notes |
|---|---|---|
| Web page | `index.html` opened directly | works over `file://` |
| Claude Artifact | `python build-artifact.py` → `artifact.html` | strips the doc wrapper |
| Android app | `python build-android.py` → Capacitor project | swaps Google Fonts for bundled woff2 |

Repo: `github.com/ben-silv/CraveCast` (private).
Live Artifact: `claude.ai/code/artifact/b6ad8efe-77ee-46c4-8043-41624fa77a6f`

---

## The forecasting model

`buildModel()` fits a **recency- and intensity-weighted kernel density
estimate** over time-of-day (circular, σ = 1.15 h) × day-of-week (circular,
σ = 0.85 d), evaluated continuously so risk can be read at any instant.

- Each log is weighted by recency (21-day half-life), intensity (÷3), and
  outcome (a slip counts 1.4× a held urge).
- Normalised against the busiest cell of a full week, so risk is 0–100.
- `findWindows()` scans forward and returns contiguous stretches above the
  alert threshold; `threshold()` is driven by the sensitivity setting.

**Cold start via shrinkage.** With few logs the model blends toward a
population prior:

```
w = n / (n + K),  K = 3
at(hour) = w * personalKDE(hour) + (1 - w) * PRIOR.hour[hour]
```

So the forecast is live from the first visit, half the user's own by the third
log, and ~84% theirs by the sixteenth.

---

## Where the numbers come from (and their limits)

Two study datasets sit behind the model. **Neither is in the repo** — they are
human-subjects data, deliberately gitignored. The scripts that fit them are
committed, so the results are reproducible by anyone holding the data.

### Phone survey stress events → the hourly prior
`fit-prior.py` → `prior.js` (the `PRIOR` block embedded in `index.html`).

99 stress events, 10 participants, four phone surveys a day, Apr 2019 – Feb
2020. Smoothed circularly into a 24-point hourly curve.

Two limits, both surfaced in the app's own UI rather than hidden:
- **These are stress events, not cravings.** The study never asked about
  cravings. It is a starting shape, not a prediction about any individual.
- **06:00–08:59 fell outside every survey window**, so those hours are
  interpolated, not observed. The baseline panel hatches them.

No day-of-week term is fitted: across 10 participants enrolled at different
times, weekday variation is not separable from who was reporting that week.

### Timeline Followback drink calendars → the shrinkage constant
`fit-weekday.py`, reading `tlfb-transcribed.csv` (a hand transcription of
scanned calendars; not committed).

159 participant-days from 11 people, daily standard drinks. **No time of day**,
so this data cannot inform an hour-of-day forecast at all.

It was tested for the one thing it could support, a weekday term, and it did
not hold:
- within-person weekday spread **p = 0.27** (5,000-permutation test)
- weekend minus midweek **+0.67 drinks, 95% CI [−0.08, +1.54]** — includes zero

So no weekday term was fitted. What it did settle: **ICC = 0.76** — 76% of the
variance in daily drinking is between people, not between days. Scaled for the
degrees of freedom in a 24-hour curve, that gives K ≈ 3, replacing a K of 8
that had been chosen by feel.

### Sensor data (no longer held)
The study also had Empatica E4 wristband recordings (ACC/BVP/EDA/HR, ~4.6 GB,
timestamped per session). It was never used and has been deleted; it is
re-downloadable from the original online study. It remains the one dataset that
could genuinely improve the hour-of-day model, since it is the only timed data.

---

## The garden

The motivational layer, and the home page's main event.

- Pick a species; it matures **24 hours later** if no slip is logged in that
  window. A slip wilts it — that one is lost, but nothing already grown is ever
  removed.
- **25 species** unlock by garden size: three flowers at 0, then clover (3),
  rose (4), cactus (5), oak (6), first chicken (7), up through sheep, pig, cow,
  horse to a peacock at 60.
- Growth shows four stages: plants 🌱→🌿→🪴→species, birds 🥚→🐣→🐤→species,
  mammals 🌾→🐾→🍼→species.
- **Ranks** by garden size: Bare plot → Seedling → Sprout → Gardener → Grower →
  Cultivator → Smallholder → Farmer → Homesteader.
- A **clean-day streak** counts back from the last logged slip.
- Data lives in `S.garden = {growing, plot[], wilted}`.

Implementation note: the seed clock is floored to the minute
(`Math.floor(Date.now()/60000)*60000`) because the log form's `datetime-local`
has minute resolution — otherwise a slip logged immediately after planting
lands *before* the seed and fails to wilt it.

---

## The interface

Four tabs: **Today**, **Log an urge**, **Patterns**, **History**.

**Today** is the garden: a scene (sky, sun, clouds, hill) with the growing
species inside a circular progress ring, stats chips, a quest bar to the next
unlock, the collection wall (grown / unlocked-not-grown / locked teasers), and
**craving weather**.

**Craving weather** is the risk curve told as a forecast — the app is called
CraveCast, after all. ☀️ Clear · 🌤️ Fair · ⛅ Changeable · 🌥️ Overcast ·
🌧️ Rough · ⛈️ Stormy, with a twelve-hour strip and one plain-English line.
The technical view (line chart, alert threshold, shaded windows, confidence)
lives in **Patterns** for anyone who wants it.

**Logging** is one question at a time — outcome, intensity, mood, activity,
triggers, when — with everything after the first skippable. Notes and "what got
you through it" are deliberately *not* asked mid-urge; they are added
afterwards from the confirmation panel or any History row.

---

## Accounts (optional, off by default)

Empty `CLOUD` config = everything stays in `localStorage`, no account, no
server. Fill in a Supabase project URL and anon key and the app grows sign-up,
email verification, cross-device sync, password reset and account deletion.

- Reached over plain `fetch` against Supabase's REST API — no SDK, no CDN
  script, so the single-file property survives.
- `supabase-schema.sql` creates one table, row-level-security policies scoping
  every row to `auth.uid()`, and three functions (`cc_save`, `cc_load`,
  `cc_delete_account`, the last `security definer` to reach `auth.users`).
- Signing in **merges** rather than overwrites: habits and logs unioned by id,
  garden unioned by species and completion time, settings preferring the local
  device.
- **Cannot run as an Artifact** — the Artifact sandbox blocks all external
  network requests and has no way to identify a viewer. Multi-user requires
  ordinary static hosting.
- **Not verified against a live Supabase project.** The request handling is
  written from the documented API, not observed traffic.

See `README-ACCOUNTS.md`.

---

## Files

| Path | What |
|---|---|
| `index.html` | the whole app — edit this |
| `artifact.html` | generated fragment for the Artifact |
| `build-artifact.py` / `build-android.py` | the two builds |
| `fit-prior.py` → `prior.js` | fits the hourly cold-start baseline |
| `fit-weekday.py` | tests (and rejects) a weekday term |
| `supabase-schema.sql` | accounts database + policies |
| `README.md`, `README-ACCOUNTS.md`, `README-ANDROID.md` | docs |

Gitignored and local only: the study data, `CraveCast.apk`, `*.bak`.

---

## Things worth knowing when answering questions

- **The APK is stale.** It predates the garden, tabs, weather and the flow
  rewrite. `rebuild.ps1` in `C:\Users\silve\CraveCastApp` regenerates it.
- **The model was never fake.** Early on the *sample data* was invented; the
  KDE always fitted real user logs. Sample data now resamples the fitted study
  curve instead.
- **`[hidden]` needs `!important`** here, because component rules set `display`
  and outrank the UA stylesheet — this caused a real bug where inert account UI
  showed in the Artifact.
- The app is honest in its own UI about the baseline being stress data rather
  than craving data, and about the un-surveyed morning hours. Keep it that way.
