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

**The garden.** Pick something to grow. Stay clean 24 hours and it's yours. Slip and that one's lost, but nothing else disappears. 25 species unlock as your garden fills.

**Logging.** One question at a time. Notes and "what helped" go in after, so you're not stuck filling forms mid-urge.

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

- `index.html` — the whole app
- `build-artifact.py` — generates Claude Artifact version
- `build-android.py` — builds Android app
- `fit-prior.py` / `fit-weekday.py` — fitted the model from study data
- `supabase-schema.sql` — optional database schema

## Sources

- Ramesh Kumar Sah et al. (2022). Alcohol and Drug Abuse Research Program (ADARP) Dataset. https://doi.org/10.5281/zenodo.664029
- Sah et al. (2020). Mobile Health for Alcohol Recovery and Relapse Prevention. CHASE. https://doi.org/10.1145/3384420.3431779
- Alinia et al. (2021). Associations Between Physiological Signals and Self-reported Outcomes in Alcohol Use Disorder Recovery. JMIR Form Res. https://doi.org/10.2196/27891
