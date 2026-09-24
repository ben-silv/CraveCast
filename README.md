# CraveCast

A forecasting app to help you fight your addiction. Unlike other addiction apps, CraveCast is meant to be fun and help you stay on track. The gamification and reward aspect makes logging your cravings and staying clean something to look forward to, not another chore.

## If you're in crisis

- SAMHSA: 1-800-662-4357 (24/7)
- Crisis Text Line: text HOME to 741741
- 988 Suicide & Crisis Lifeline: call or text 988

CraveCast is a tool to help you notice patterns and attempt to support you during tough times.

## How it works

**The forecast.** Log when you get cravings -> the model learns when you're most at risk -> shows it to you as a weather report. Clear skies or stormy — you see what's coming.

**The garden.** Pick something to grow. Stay clean 24 hours and it's yours to plant. Slip and that one's lost, but nothing already grown ever disappears. 28 species unlock as your garden fills, rewarding you for staying strong.

**Logging.** When you feel a craving click a few buttons and we log it for you. Tell us how strong it is, your mood and stress, where you are, and how it went. The last one is what the model learns from. A note is optional and can go in after, saving you that mid-craving annoyance.

## Try it

Live: https://ben-silv.github.io/CraveCast/index.html

## Important stuff

This is beta. Based on real research but still built by a student. It is not meant to get you clean, but to provide an extra tool.

**The Model:**
- Learns from your logs, gets smarter over time
- Starts with a population baseline, personalizes as you log
- By log 16 it's ~84% based on your data

**Your data:**
- Stays in your browser. No servers, no account needed
- If you clear browser data it's gone
- Optional: set up a private account for cross-device sync later

**What it won't do:**
- Stop all cravings
- Replace therapy or a support group
- It's awareness, not a cure

## The Model

Kernel density estimate over time-of-day and day-of-week, weighted by recency (21-day half-life), intensity, and whether it was a slip or held urge.

Starts with a baseline from 99 stress events across 10 people (phone surveys, April 2019 – Feb 2020). Blends toward your own logs as you add them. By your third entry it's half you, by the sixteenth it's ~84% you.

Honest limits:
- Baseline is stress data, not craving data
- 6–9 AM is interpolated (fell outside survey windows)
- No weekday term fitted (tested in 159 participant-days of drink calendars, didn't hold)

## Data

Stays in your browser by default.

## Sources

- Ramesh Kumar Sah et al. (2022). Alcohol and Drug Abuse Research Program (ADARP) Dataset. https://doi.org/10.5281/zenodo.664029
- Sah et al. (2020). Mobile Health for Alcohol Recovery and Relapse Prevention. CHASE. https://doi.org/10.1145/3384420.3431779
- Alinia et al. (2021). Associations Between Physiological Signals and Self-reported Outcomes in Alcohol Use Disorder Recovery. JMIR Form Res. https://doi.org/10.2196/27891
