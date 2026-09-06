# -*- coding: utf-8 -*-
"""Fit CraveCast's cold-start prior from the phone-survey workbook.

WHAT THIS DATA IS: 99 stress events reported by 10 participants over four
phone surveys a day, Apr 2019 - Feb 2020. Each event carries the hour it
happened and a coded reason.

WHAT IT IS NOT: there is no craving, urge, smoking or substance variable
anywhere in the file, so nothing here predicts a craving. What it gives is
an empirical answer to "when does stress actually land, across a day?" —
which is the strongest single driver in CraveCast's own trigger data, and
a far better starting point than an invented curve.

Output: a block of JS constants to paste into index.html, plus a summary.

    python fit-prior.py
"""
import collections
import json
import math

import pandas as pd

SRC = r"C:\Users\silve\OneDrive\Desktop\Tracker\Final Phone Survey Stress Events.xlsm"

HEAD = ["Obs", "newdate", "time submitted", "Databurst", "more_stressed",
        "more_overwhelm", "more_anxious", "reason_stress", "reason_other",
        "time_stress_1", "time_stress_2", "time_stress_3", "time_stress_4"]

# Each of the four daily surveys asks about a different span of the day, so a
# code means a different clock hour depending on which column it sits in.
HOUR_OF = {
    "time_stress_1": {1: 21, 2: 22, 3: 23, 4: 0, 5: 1, 6: 2, 7: 3, 8: 4, 9: 5},
    "time_stress_2": {1: 9, 2: 10, 3: 11, 4: 12},
    "time_stress_3": {1: 13, 2: 14, 3: 15, 4: 16},
    "time_stress_4": {1: 17, 2: 18, 3: 19, 4: 20},
}
# 06:00-08:59 is in none of the four windows: the study never asked about it.
UNSURVEYED = [6, 7, 8]

REASON_LABEL = {
    1: "Conflict with someone",
    2: "Too much to do",
    3: "Money worry",
    4: "Unsafe surroundings",
    5: "Inconvenienced",
    6: "Injury or health",
    7: "Legal problem",
    8: "Started thinking about it",
    9: "Something else",
}

SIGMA_H = 1.3          # hours; matches the app's own SIG_HOUR closely


def read_events():
    df = pd.read_excel(SRC, sheet_name=0, header=None)
    rows, case = [], None
    for i in range(df.shape[0]):
        a = df.iat[i, 0]
        s = "" if pd.isna(a) else str(a).strip()
        if s.lower().startswith("caseid"):
            case = s.split("=")[-1].strip()
            continue
        if s in ("Obs", "KEY", "") or case is None:
            continue
        rec = {"caseid": case}
        for j, name in enumerate(HEAD):
            v = df.iat[i, j] if j < df.shape[1] else None
            rec[name] = None if pd.isna(v) else v
        rows.append(rec)
    return pd.DataFrame(rows)


def num(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def main():
    d = read_events()
    events = []
    for _, r in d.iterrows():
        when = pd.to_datetime(r["newdate"], errors="coerce")
        for col, m in HOUR_OF.items():
            c = num(r[col])
            if c in m:
                events.append({"case": r["caseid"], "hour": m[c],
                               "dow": None if pd.isna(when) else when.dayofweek,
                               "reason": num(r["reason_stress"])})

    n = len(events)
    cases = len({e["case"] for e in events})
    counts = collections.Counter(e["hour"] for e in events)

    # ── exposure: an hour the survey never asked about has no zero to report,
    #    so it must be treated as missing rather than as "no stress happened"
    observed = [h for h in range(24) if h not in UNSURVEYED]

    # ── circular Gaussian smoothing over the observed hours only
    def circ(a, b):
        x = abs(a - b) % 24
        return min(x, 24 - x)

    smooth = []
    for h in range(24):
        wsum = vsum = 0.0
        for o in observed:
            w = math.exp(-(circ(h, o) ** 2) / (2 * SIGMA_H ** 2))
            wsum += w
            vsum += w * counts.get(o, 0)
        smooth.append(vsum / wsum if wsum else 0.0)

    peak = max(smooth) or 1.0
    curve = [round(v / peak * 100, 1) for v in smooth]

    # ── day of week, shrunk hard toward flat: 99 events across 7 days cannot
    #    support a confident weekday effect, so this only nudges
    dcount = collections.Counter(e["dow"] for e in events if e["dow"] is not None)
    dtot = sum(dcount.values())
    k = 40.0                       # shrinkage strength
    dow = []
    for i in range(7):
        raw = dcount.get(i, 0) / dtot * 7 if dtot else 1.0
        dow.append(round((dtot * raw + k * 1.0) / (dtot + k), 3))

    rcount = collections.Counter(e["reason"] for e in events if e["reason"])
    rtot = sum(rcount.values())
    reasons = [{"code": c, "label": REASON_LABEL.get(c, "?"),
                "n": rcount[c], "pct": round(rcount[c] / rtot * 100)}
               for c in sorted(rcount, key=lambda c: -rcount[c])]

    print("=" * 68)
    print("  %d stress events · %d participants · %s to %s"
          % (n, cases, str(d.newdate.min())[:10], str(d.newdate.max())[:10]))
    print("=" * 68)
    print("\nobserved stress events by hour (raw counts):")
    for h in range(24):
        mark = "  [never surveyed]" if h in UNSURVEYED else ""
        print("  %02d:00  %-16s %3d   smoothed %5.1f%s"
              % (h, "#" * counts.get(h, 0), counts.get(h, 0), curve[h], mark))
    print("\nreasons given:")
    for r in reasons:
        print("  %2d%%  %-28s n=%d" % (r["pct"], r["label"], r["n"]))
    print("\nday-of-week, after shrinkage (reported only — deliberately NOT")
    print("used: at n=%d across %d participants this is not separable from" % (n, cases))
    print("which people happened to be enrolled in a given week):")
    print("  " + "  ".join("%s %.2f" % (dn, v) for dn, v in
                           zip(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], dow)))

    js = (
        "/* Fitted by fit-prior.py from 'Final Phone Survey Stress Events.xlsm':\n"
        "   %d stress events reported by %d participants over four phone surveys\n"
        "   a day, %s to %s. These are stress events, NOT cravings — the study\n"
        "   never asked about cravings. Hours %s were outside every survey\n"
        "   window, so their values are interpolated, not observed. There is\n"
        "   deliberately no day-of-week term: across 10 participants enrolled\n"
        "   at different times, weekday variation is not separable from who\n"
        "   happened to be reporting that week. */\n"
        "const PRIOR = {\n"
        "  n: %d, cases: %d,\n"
        "  unsurveyed: %s,\n"
        "  hour: %s,\n"
        "  reasons: %s\n"
        "};\n"
    ) % (n, cases, str(d.newdate.min())[:10], str(d.newdate.max())[:10],
         "06:00-08:59", n, cases, json.dumps(UNSURVEYED), json.dumps(curve),
         json.dumps([{"label": r["label"], "pct": r["pct"]} for r in reasons]))

    out = SRC.rsplit("\\", 1)[0] + r"\prior.js"
    with open(out, "w", encoding="utf-8") as f:
        f.write(js)
    print("\nwrote", out)


if __name__ == "__main__":
    main()
