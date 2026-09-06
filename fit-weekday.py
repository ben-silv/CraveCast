# -*- coding: utf-8 -*-
"""Test whether the TLFB data supports a day-of-week term in the forecast.

The Timeline Followback records DRINKS PER DAY, with no time of day, so it
cannot touch CraveCast's hour-of-day curve. The one thing it could add is a
weekday effect. This checks whether that effect is real or noise before any
of it is allowed near the app.

Between-person differences here are enormous (one participant is abstinent
for 14 days, another drinks 12-18 every day), so the only defensible test is
a within-person one: centre each participant on their own mean, then ask
whether what is left still varies by weekday.

    python fit-weekday.py
"""
import collections
import csv

import numpy as np

SRC = r"C:\Users\silve\OneDrive\Desktop\Tracker\tlfb-transcribed.csv"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
RNG = np.random.default_rng(20260906)


def load():
    rows = []
    with open(SRC, encoding="utf-8") as f:
        for line in f:
            if line.startswith("\u00ab") or line.startswith("participant,"):
                continue
            p, d, wd, dr, *rest = next(csv.reader([line]))
            rows.append({"p": p, "date": d, "wd": wd, "drinks": float(dr)})
    return rows


def main():
    rows = load()
    people = sorted({r["p"] for r in rows})
    print("=" * 70)
    print("  %d participants, %d participant-days" % (len(people), len(rows)))
    print("=" * 70)

    print("\nper participant:")
    for p in people:
        v = [r["drinks"] for r in rows if r["p"] == p]
        dd = sum(1 for x in v if x > 0)
        print("  %s  %2d days  drinking days %2d  mean %5.2f  max %4.1f"
              % (p, len(v), dd, np.mean(v), max(v)))

    drinking = [r for r in rows if r["drinks"] > 0]
    print("\ndrinking days overall: %d of %d (%.0f%%)"
          % (len(drinking), len(rows), 100 * len(drinking) / len(rows)))

    # ── raw weekday means (the naive, misleading view) ──────────────────
    print("\nraw mean drinks by weekday (NOT adjusted for who was reporting):")
    for d in DAYS:
        v = [r["drinks"] for r in rows if r["wd"] == d]
        print("   %s  n=%2d  mean %5.2f" % (d, len(v), np.mean(v)))

    # ── within-person: each participant centred on their own mean ───────
    cent = []
    for r in rows:
        mu = np.mean([x["drinks"] for x in rows if x["p"] == r["p"]])
        cent.append({**r, "c": r["drinks"] - mu})

    print("\nwithin-person deviation by weekday (each person centred on their own mean):")
    obs = {}
    for d in DAYS:
        v = [r["c"] for r in cent if r["wd"] == d]
        obs[d] = np.mean(v)
        print("   %s  n=%2d  %+6.2f drinks vs that person's own average" % (d, len(v), obs[d]))

    # ── permutation test: shuffle weekday labels within each person ─────
    def spread(assign):
        by = collections.defaultdict(list)
        for r, d in zip(cent, assign):
            by[d].append(r["c"])
        return max(np.mean(by[d]) for d in DAYS) - min(np.mean(by[d]) for d in DAYS)

    actual = spread([r["wd"] for r in cent])
    idx_by_person = collections.defaultdict(list)
    for i, r in enumerate(cent):
        idx_by_person[r["p"]].append(i)

    null = []
    for _ in range(5000):
        assign = [None] * len(cent)
        for p, idxs in idx_by_person.items():
            labs = [cent[i]["wd"] for i in idxs]
            RNG.shuffle(labs)
            for i, l in zip(idxs, labs):
                assign[i] = l
        null.append(spread(assign))
    null = np.array(null)
    pval = float((null >= actual).mean())

    print("\npermutation test (5000 shuffles of weekday within each person)")
    print("  observed spread Mon..Sun : %.2f drinks" % actual)
    print("  spread expected by chance: %.2f  (95th pct %.2f)" % (null.mean(), np.percentile(null, 95)))
    print("  p = %.3f" % pval)

    # ── weekend vs weekday, the single contrast most likely to hold ─────
    we = [r["c"] for r in cent if r["wd"] in ("Fri", "Sat", "Sun")]
    wk = [r["c"] for r in cent if r["wd"] in ("Mon", "Tue", "Wed", "Thu")]
    diff = np.mean(we) - np.mean(wk)
    boot = []
    for _ in range(5000):
        samp = RNG.choice(people, len(people), replace=True)
        a, b = [], []
        for p in samp:
            pr = [r for r in cent if r["p"] == p]
            a += [r["c"] for r in pr if r["wd"] in ("Fri", "Sat", "Sun")]
            b += [r["c"] for r in pr if r["wd"] in ("Mon", "Tue", "Wed", "Thu")]
        if a and b:
            boot.append(np.mean(a) - np.mean(b))
    lo, hi = np.percentile(boot, [2.5, 97.5])
    print("\nweekend (Fri-Sun) minus midweek, within person:")
    print("  %+.2f drinks   95%% CI by participant bootstrap [%+.2f, %+.2f]" % (diff, lo, hi))
    print("  CI %s zero" % ("EXCLUDES" if lo > 0 or hi < 0 else "INCLUDES"))

    print("\n" + "=" * 70)
    if pval < 0.05 and (lo > 0 or hi < 0):
        print("  VERDICT: a weekday effect survives. Safe to fit.")
    else:
        print("  VERDICT: no weekday effect distinguishable from noise at this")
        print("  sample size. Fitting one would be dressing up chance as signal.")
    print("=" * 70)


if __name__ == "__main__":
    main()
