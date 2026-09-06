/* Fitted by fit-prior.py from 'Final Phone Survey Stress Events.xlsm':
   99 stress events reported by 10 participants over four phone surveys
   a day, 2019-04-30 to 2020-02-21. These are stress events, NOT cravings — the study
   never asked about cravings. Hours 06:00-08:59 were outside every survey
   window, so their values are interpolated, not observed. There is
   deliberately no day-of-week term: across 10 participants enrolled
   at different times, weekday variation is not separable from who
   happened to be reporting that week. */
const PRIOR = {
  n: 99, cases: 10,
  unsurveyed: [6, 7, 8],
  hour: [54.0, 37.6, 23.9, 16.8, 14.6, 14.3, 17.7, 45.6, 83.3, 97.9, 99.0, 85.4, 71.9, 72.6, 75.2, 69.4, 67.3, 75.3, 82.5, 86.5, 95.3, 100.0, 88.2, 70.1],
  reasons: [{"label": "Started thinking about it", "pct": 29}, {"label": "Conflict with someone", "pct": 21}, {"label": "Inconvenienced", "pct": 9}, {"label": "Money worry", "pct": 8}, {"label": "Unsafe surroundings", "pct": 8}, {"label": "Too much to do", "pct": 6}, {"label": "Something else", "pct": 6}, {"label": "Injury or health", "pct": 6}, {"label": "Legal problem", "pct": 6}]
};
