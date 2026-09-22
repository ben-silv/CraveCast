# CraveCast

A craving forecasting app. Predicts when an urge is likely to hit, warns you before it, and turns every day you stay clean into something growing in a garden.

No sign-up. No tracking. Everything stays in your browser.

## If you're in crisis

- SAMHSA: 1-800-662-4357 (24/7)
- Crisis Text Line: text HOME to 741741
- 988 Suicide & Crisis Lifeline: call or text 988

CraveCast is a tool to help you notice patterns. It's not therapy.

## How it works

**The forecast.** Logs when you get cravings, learns when you're most at risk, shows it as a weather report. Clear skies or stormy — you see what's coming. By your third log it's half your own pattern.

**The garden.** Pick something to grow. Stay clean 24 hours and it's yours to plant. Slip and that one's lost, but nothing already grown ever disappears. 28 species unlock as your garden fills, and the plot itself grows a dimension each time you fill it.

**Logging.** One short scroll: how strong it is, your mood and stress, where you are, and how it went. The last one is what the forecast learns from. A note is optional and goes in after, so you're not stuck filling forms mid-urge.

## Try it

Live: https://ben-silv.github.io/CraveCast/index.html

Local: 
```bash
git clone https://github.com/ben-silv/CraveCast
open CraveCast/index.html
```

## Important stuff

This is beta. Built by a student, based on real research.

**The forecast:**
- Learns from your logs, gets smarter over time
- Starts with a population baseline, personalizes as you log
- By log 16 it's ~84% you

**Your data:**
- Stays in your browser. No servers, no account needed
- If you clear browser data it's gone
- Optional: set up a private account for cross-device sync later

**What it won't do:**
- Stop all cravings
- Replace therapy or a support group
- It's awareness, not a cure

## Running it locally

```bash
python -m http.server 8000
# then open http://127.0.0.1:8000/index.html
```

Or just open `index.html` directly in your browser.

## Deploying

GitHub Pages (free, public):
1. Settings → Pages
2. Source: main branch, root directory
3. Wait a minute
4. Live at `https://username.github.io/CraveCast/index.html`

## The forecast

Kernel density estimate over time-of-day and day-of-week, weighted by recency (21-day half-life), intensity, and whether it was a slip or held urge.

Starts with a baseline from 99 stress events across 10 people (phone surveys, April 2019 – Feb 2020). Blends toward your own logs as you add them. By your third entry it's half you, by the sixteenth it's ~84% you.

Honest limits:
- Baseline is stress data, not craving data
- 6–9 AM is interpolated (fell outside survey windows)
- No weekday term fitted (tested in 159 participant-days of drink calendars, didn't hold)

## Data

Stays in your browser by default. Optional: enable a Supabase account for cross-device sync. See `README-ACCOUNTS.md`.

## What's in the repo

| Path | What |
|---|---|
| `index.html` | the whole app — edit this |
| `artifact.html` | generated; the fragment published as a Claude Artifact |
| `build-artifact.py` | `index.html` → Artifact fragment |
| `build-native.py` | `index.html` → shared native web assets, with fonts bundled offline |
| `codemagic.yaml` | the iOS build, on a hosted Mac — signs and ships to TestFlight |
| `rebuild-ios.sh` | the same build by hand, if you have a Mac in front of you |
| `capacitor.config.json`, `package.json` | the Capacitor project; CI clones this repo and reads them |
| `make-icon.py` | renders `assets/icon.png`, the 1024px app icon |
| `fit-prior.py` | fits the cold-start baseline from the phone-survey workbook |
| `prior.js` | its output — the `PRIOR` block embedded in `index.html` |
| `fit-weekday.py` | tests whether the drink calendars support a weekday term |
| `supabase-schema.sql` | tables and row-level-security policies for optional accounts |
| `design_handoff_cravecast/` | the design this UI was built from, and the icon sprite |
| `README-ACCOUNTS.md` | how to switch accounts and cloud sync on |
| `README-ANDROID.md` | installing and rebuilding the Android app |
| `README-IOS.md` | building the iOS app and submitting it to the App Store |

One self-contained `index.html` — no framework, no build step, no dependencies.
The same file is the source for four targets: the web page, a published Claude
Artifact, an Android app and an iOS app.

## Sources

- Ramesh Kumar Sah et al. (2022). Alcohol and Drug Abuse Research Program (ADARP) Dataset. https://doi.org/10.5281/zenodo.664029
- Sah et al. (2020). Mobile Health for Alcohol Recovery and Relapse Prevention. CHASE. https://doi.org/10.1145/3384420.3431779
- Alinia et al. (2021). Associations Between Physiological Signals and Self-reported Outcomes in Alcohol Use Disorder Recovery. JMIR Form Res. https://doi.org/10.2196/27891
