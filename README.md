# CraveCast

Forecasts when a craving is likely to hit, warns you before it does, and turns
every day you ride one out into something growing in a garden.

One self-contained `index.html`. No framework, no build step, no dependencies —
open the file and it runs. The same file is the source for three targets: the
web page, a published Artifact, and an Android app.

---

## What it does

**Forecast.** A recency- and intensity-weighted kernel density estimate over
time-of-day (circular) × day-of-week, evaluated continuously so risk can be read
at any instant. On the home page it's shown as weather — ☀️ Clear through
⛈️ Stormy, twelve hours at a glance. The underlying curve, the alert threshold
and the predicted windows are in **Patterns** for anyone who wants them.

**Cold start.** The forecast doesn't sit dead waiting for data. It opens on a
baseline fitted from real phone-survey stress reports and shrinks toward your
own pattern as you log — half yours by the third entry. See *Where the numbers
come from* below.

**Early warnings.** Arm it and it fires ahead of a predicted window, with what
usually drives that window and what has worked for you before. In the Android
build the schedule is handed to the OS alarm manager so warnings arrive with the
app closed; in a browser it's an in-page timer.

**The garden.** Pick something to grow. Twenty-four hours without logging that
you gave in and it's yours permanently; log a slip and that one is lost, though
nothing already grown is ever taken away. Twenty-five species unlock as the
garden fills — flowers, then trees, then farm animals — with ranks, a clean-day
streak, and a collection wall.

**Logging.** One question at a time, everything after the first skippable.
Notes and "what got you through it" are deliberately not asked mid-urge; you add
those afterwards, from the confirmation panel or any row in History.

**Accounts (optional, off by default).** Empty config = everything stays in the
browser, no account, no server. Fill it in and you get sign-up, email
verification, cross-device sync and account deletion. See
[README-ACCOUNTS.md](README-ACCOUNTS.md).

---

## Files

| Path | What |
|---|---|
| `index.html` | the whole app — edit this |
| `artifact.html` | generated; the fragment published as a Claude Artifact |
| `build-artifact.py` | `index.html` → Artifact fragment |
| `build-android.py` | `index.html` → Android web assets, with fonts bundled offline |
| `fit-prior.py` | fits the cold-start baseline from the phone-survey workbook |
| `prior.js` | its output — the `PRIOR` block embedded in `index.html` |
| `fit-weekday.py` | tests whether the drink calendars support a weekday term |
| `supabase-schema.sql` | table, row-level-security policies and functions for accounts |
| `README-ACCOUNTS.md` | how to switch accounts and cloud sync on |
| `README-ANDROID.md` | installing and rebuilding the Android app |

---

## Where the numbers come from

Two study datasets sit behind the model. **Neither is in this repository** —
they are human-subjects data and stay local. The scripts that read them are
here, so the fits are reproducible by anyone who holds the data.

**Phone survey stress events** — 99 stress events from 10 participants
answering four surveys a day. `fit-prior.py` turns these into the hourly
cold-start curve. Two honest limits, both carried into the app's own UI:

- These are *stress* events, not cravings. The study never asked about
  cravings. It's a starting shape, not a prediction about any individual.
- 06:00–08:59 fell outside every survey window, so those hours are
  interpolated rather than observed, and are marked as such.

No day-of-week term is fitted from it: across 10 participants enrolled at
different times, weekday variation isn't separable from who was reporting.

**Timeline Followback calendars** — daily standard drinks for 11 participants
over 159 monitored days. These contain no time of day, so they cannot inform an
hour-of-day forecast. `fit-weekday.py` tests the one thing they could support
and finds it doesn't hold: within-person weekday spread p = 0.27, weekend-minus-
midweek 95% CI [−0.08, +1.54], which includes zero. No weekday term was fitted.

What they *did* settle is how fast to stop trusting the population and start
trusting the user. 76% of the variance in daily drinking is between people
rather than between days (ICC = 0.76). Scaled for the degrees of freedom in a
24-hour curve, that puts the shrinkage constant at K ≈ 3 — so the forecast is
half yours by the third log instead of the eighth.

---

## Running it

```
python -m http.server 8000
```

then open `http://127.0.0.1:8000/index.html`. Or just open the file directly —
everything except the optional account sync works over `file://`.

To rebuild the Artifact fragment after editing:

```
python build-artifact.py
```

---

## Acknowledgements
- Ramesh Kumar Sah, Michael McDonell, Patricia Pendry, Sara Parent, Hassan Ghasemzadeh, & Michael J Cleveland. (2022). Alcohol and Drug Abuse Research Program (ADARP) Dataset (1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.664029

- Ramesh Kumar Sah, Hassan Ghasemzadeh, Assal Habibi, Michael McDonell, Patricia Pendry, and Michael Cleveland. 2020. Poster: Mobile Health for Alcohol Recovery and Relapse Prevention. In 2020 IEEE/ACM International Conference on Connected Health: Applications, Systems and Engineering Technologies (CHASE). IEEE Press, 18–19. https://doi.org/10.1145/3384420.3431779

- Alinia P, Sah RK, McDonell M, Pendry P, Parent S, Ghasemzadeh H, Cleveland MJ. Associations Between Physiological Signals Captured Using Wearable Sensors and Self-reported Outcomes Among Adults in Alcohol Use Disorder Recovery: Development and Usability Study. JMIR Form Res. 2021 Jul 21;5(7):e27891. DOI: 10.2196/27891. PMID: 34287205; PMCID: PMC8339978.

## Privacy

With accounts off, nothing leaves the browser: habits, logs and garden live in
`localStorage` and there is no server to send them to. Turning accounts on moves
that data to a database you control, and the footer text changes to say so.
