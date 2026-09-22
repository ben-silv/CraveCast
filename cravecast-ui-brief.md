# CraveCast UI/UX Design Brief

**For Claude Design: Create a friendly, high-tech, smooth interface for addiction craving prediction app**

---

## Design Philosophy

**"Calm, Clear, Empowering"**

This is a mental health + recovery app. Users are in vulnerable moments. The UI should:
- Reduce friction (minimal clicks to log or get a prediction)
- Feel supportive, not clinical or judgmental
- Look modern and trustworthy (not "clinical boring")
- Make the ML model feel magic but transparent
- Guide users toward coping strategies without being preachy

---

## Visual Identity

### Color Palette
- **Primary:** Soft teal/cyan (#06B6D4 or #14B8A6) — calming, hopeful, modern
- **Secondary:** Warm orange/amber (#F59E0B or #FBBF24) — warmth, support, energy
- **Neutral:** Clean white background, dark gray/near-black text (#1F2937 or #111827)
- **Accent:** Subtle sage green (#10B981) for positive feedback, success states
- **Alert:** Soft red/rose (#F87171 or #FB7185) for high-risk warnings (not scary, just clear)

**Why these colors?**
- Teal: High-tech, modern, calming (common in health/wellness apps)
- Warm accents: Humanity, hope (breaks up the digital coldness)
- Soft tones: No harsh reds or alarming colors (users are vulnerable)

### Typography
- **Headings:** Modern sans-serif (Inter, System UI) — bold, clear, friendly
- **Body text:** Same sans-serif, readable at all sizes
- **Input labels:** Slightly smaller, medium weight (clear but not dominant)
- **Risk predictions:** Large, bold numbers (62%) — that's the key info

### Layout Approach
- **Mobile-first** — Most users will check on their phone when about to use
- **Card-based** — Each action (log, predict, view history) is a distinct, tappable card
- **Breathing room** — Generous whitespace, not cramped
- **Bottom nav** — Easy thumb access for mobile (Home, Log, History, Settings)

---

## Key Screens & Interactions

### 1. **Dashboard / Home**
*What users see when they open the app*

**Layout:**
- Large greeting ("Hey Ben, how are you right now?")
- Current time + date (contextual)
- **Big card: Quick prediction** 
  - Shows risk score (65%) in huge, readable text
  - One-line explanation ("High-risk window detected")
  - Green/amber/red indicator (non-scary visual cue)
- **"Log Now" button** (primary, teal, easy to tap)
- **Quick summary cards below:**
  - Streak (days logged consistently)
  - This week's high-risk times
  - Last 3 predictions (mini sparkline chart)
- **Floating action button (FAB)** in bottom right: Quick log shortcut

**Interaction:**
- Smooth scroll down reveals more insights
- Tap risk score card → see detailed explanation of why
- Tap "Log Now" → transitions to logging flow (not a new page)

**Tone:** Supportive, not alarmist. If high risk: "You might want to check in with yourself" not "WARNING: CRAVING IMMINENT"

---

### 2. **Quick Log Flow**
*The core action: user enters their current state*

**Approach: Multi-step, but feels like one smooth interaction**

**Step 1: Current Craving Level**
- Large slider (1-10)
- Visual gradient (green at 1, orange at 10)
- Emoji indicators to make it feel human (😊 at 1, 😟 at 10)
- Text shows selected number large
- Single label: "How strong is your craving right now?"

**Step 2: Context**
- Mood slider (same visual as craving)
- Label: "How's your mood?" (1 = sad/tired, 10 = happy/energized)
- Below it: Quick toggle buttons for **Stress level** (Low / Medium / High)

**Step 3: Activity/Context**
- **Quick selection buttons** (toggle, not radio):
  - Alone / With others
  - Work / Home / Out
  - Just finished work / Evening / Night
- Multiple selections allowed (you can be "alone" + "at home")
- Visual: Pills/tags that light up when selected (teal background, darker text)

**Step 4: Optional Note**
- Text input: "Anything else? (optional)"
- Placeholder: "E.g., had a tough meeting, feeling triggered, etc."
- Small, friendly prompt text

**Step 5: Submit**
- **Large "Check My Risk" button** (teal, full-width, satisfying tap)
- Below it: "Save & Get Insight" (secondary text, not a separate button)

**Interaction Flow:**
- Entire log happens on one smooth-scrolling screen
- No page transitions (feels fast, not clunky)
- Each selection animates slightly (color change, scale, subtle bounce)
- After submit: Smooth scroll down to see the prediction immediately on same page

---

### 3. **Prediction Result**
*What the model outputs after logging*

**Design:**

Large risk score card:
```
        ┌─────────────────────┐
        │    Risk Level: 68%   │
        │   (High-Risk Window) │
        └─────────────────────┘
```
- Number is huge (48pt+), teal or warm color based on level
- Underneath: "You're in a medium-high risk window"

**Why this prediction?**
- Bulleted explainer (clear, short):
  - ✓ Time is 7:15 PM (your usual high-risk hour)
  - ✓ Stress level is high + feeling alone
  - ✓ Recent pattern: This combo led to cravings 8/10 times
- Not overwhelming, just transparent

**What to do now:**
- **3 suggested coping strategies** (cards, tappable):
  - 📞 Call a friend / support person
  - 🚶 Go for a walk or change environment
  - 🧘 5-min breathing exercise
- Not prescriptive, just options
- Tap to see more details or a timer (if you pick the exercise)

**Bottom:**
- "I already handled this" button (gray, secondary) — teaches the model you're good
- "Log your craving in 30 min" button — creates a reminder

---

### 4. **History & Trends**
*User sees patterns over time*

**Layout:**

**Top card: This week's summary**
- Sparkline chart showing predictions over the week
- "You've logged 18 times this week — great consistency!"
- Peak risk time highlighted

**Timeline view (scrollable):**
- Cards for each day (shows recent logs)
- Each card: Date, highest risk score that day, how many logs
- Tap to expand and see details

**Pattern insights (unique feature):**
- "Your highest-risk time is 6-8 PM"
- "Stress + alone combination predicted 82% of your high cravings"
- "You're 40% less likely to crave on days you exercised"
- These insights animate in as the user scrolls

**Chart options:**
- Toggle between Week / Month view
- Risk over time (line chart)
- Heat map: Time of day × Risk level (visual grid showing when you're most vulnerable)

**Interaction:**
- Swipe between charts
- Tap any data point to see what you logged that day
- Pull-to-refresh to recalculate insights

---

### 5. **Settings & Profile**
*Simple, not overwhelming*

- **Profile:** Name, recovery focus (alcohol/nicotine/other), sobriety date (optional)
- **Notifications:** Toggle for reminders ("Check in at your high-risk time?")
- **Dark mode:** Toggle (respects OS preference)
- **Data export:** Download logs as JSON
- **Privacy:** Explanation that all data stays on your device
- **About:** Info on the model, links to resources

**Tone:** Simple and clear. Privacy is a trust signal — emphasize it.

---

## Unique Features & Interactions

### 1. **Prediction Explanation Card**
- Tap the risk score → expands to show **exactly why** the model made that prediction
- Visual: Highlights the factors that contributed most
- Makes the ML feel transparent, not magical

### 2. **"You're Winning" Streak Indicator**
- Shows consecutive days logged
- Celebration animation when you hit milestones (7 days, 30 days)
- Subtle: Not gamified to the point of being annoying
- Motivates without being preachy

### 3. **Smooth Micro-Interactions**
- Slider values animate as you drag
- Buttons have satisfying tap feedback (color + slight scale)
- Numbers count up when you view them (62% animates from 0 to 62)
- Transitions between screens are smooth (fade, slide, not jarring)

### 4. **Contextual Nudges**
- If user hasn't logged in a week: "Gentle reminder: Logging helps the model learn"
- If user consistently ignores high-risk warnings: "Want to talk about what's working for you?"
- Not pushiness, just supportive check-ins

### 5. **Peer Feedback (Future)**
- Anonymous quote from someone in recovery (rotates daily)
- "I used this to catch myself before a relapse. It works." — Alex, 6 months sober
- Human connection element

### 6. **Haptic Feedback (Mobile)**
- Subtle vibration when you hit the "Check My Risk" button
- Stronger vibration for high-risk alerts (but only if enabled)
- Communicates urgency without sound (important for private moments)

---

## User Flow (Complete Journey)

```
1. Open app
   ↓
2. See dashboard (prediction from last log or "log now" prompt)
   ↓
3. Tap "Log Now"
   ↓
4. Smooth scroll through: Craving → Mood/Stress → Context → Note → Submit
   ↓
5. Prediction result appears (same page, no load screen)
   ↓
6. See risk score, explanation, suggested actions
   ↓
7. Choose a coping strategy (tap to see details/timer)
   ↓
8. Tap "Back to Dashboard" or "History"
   ↓
9. View trends, streaks, insights
```

**Key principle:** No unnecessary navigation. Minimal clicks. Smooth, modern feeling.

---

## Dark Mode Variant

- Same color scheme, but inverted
- Background: Near-black (#0F172A or #1F2937)
- Text: Light gray/white
- Cards: Slightly lighter near-black with subtle borders
- Teal and warm accents pop more in dark mode
- Respects OS dark mode preference (auto-switch)

---

## Animations & Transitions

- **Page transitions:** Fade + subtle slide (smooth, 300-400ms)
- **Button presses:** Slight scale down + color shift (100-150ms, satisfying)
- **Slider interactions:** Smooth follow of thumb, instant feedback
- **Numbers counting up:** 500ms animation (e.g., 0 → 62%)
- **Confetti on milestones:** Optional, subtle (not cheesy)
- **Predictions appearing:** Fade in from bottom, like floating up
- **No over-animation:** Only enhance UX, not distract

---

## Accessibility

- **Text contrast:** All text meets WCAG AA standard (easy with teal + white)
- **Touch targets:** All buttons >= 44x44 pixels (thumb-friendly)
- **Font size:** Minimum 16px body text (readable without zooming)
- **Color independence:** Don't rely on color alone to convey info (use icons + text)
- **Keyboard navigation:** Works fully on desktop/tablet
- **Screen reader:** Semantic HTML, alt text for charts

---

## Tone & Copywriting

- **Friendly, not clinical:** "How are you feeling?" not "Patient Assessment"
- **Supportive, not judgmental:** "You're in a high-risk window" not "DANGER ALERT"
- **Empowering, not scary:** "Here's what might help" not "You're going to fail"
- **Transparent:** Explain the model honestly, show the math
- **Genuine:** Use real language, not corporate-speak

---

## Suggested Tech Stack (For Build)

- **Frontend:** React (component-based, animations)
- **Styling:** Tailwind CSS (for consistent design system)
- **Animations:** Framer Motion (smooth, professional animations)
- **Charts:** Recharts or Chart.js (for history/trends)
- **Storage:** Browser localStorage (client-side, private)
- **Dark mode:** CSS variables + React context
- **Deployment:** GitHub Pages or Vercel (same as main portfolio)

---

## Success Criteria

✅ User can log a craving in <30 seconds (from opening app)
✅ Prediction feels fast (<1 sec inference time)
✅ Design feels friendly but modern (not clinical, not childish)
✅ Colors use accessible contrast ratios
✅ Works smoothly on mobile (primary use case)
✅ Coping suggestions feel genuinely helpful (not generic)
✅ Trends/insights are motivating without being gamified to death
✅ Dark mode looks as good as light mode
✅ No animation feels janky or distracting
✅ Users want to come back (good UX retention signal)

---

## Design System Token Reference

| Element | Value |
|---------|-------|
| Primary color | #06B6D4 (teal) |
| Secondary color | #F59E0B (amber) |
| Success color | #10B981 (sage) |
| Alert color | #F87171 (soft red) |
| Background | #FFFFFF or #0F172A |
| Text primary | #1F2937 or #F3F4F6 |
| Border radius | 12px (rounded, modern) |
| Padding (cards) | 20px |
| Gap (spacing) | 16px (standard) |
| Font family | Inter, System UI sans-serif |
| Heading size | 32px (H1), 24px (H2), 18px (H3) |
| Body size | 16px (default), 14px (secondary) |
| Line height | 1.5 (readable) |

---

## Next Steps

1. **Claude Design creates mockups:**
   - Dashboard screen
   - Quick log flow (all steps)
   - Prediction result card
   - History/trends view
   - Dark mode variant

2. **Review & iterate:**
   - Feedback on color, layout, interactions
   - Refine based on feel

3. **Claude Code builds it:**
   - HTML/CSS/React structure
   - Implement animations with Framer Motion
   - Build chart components for history
   - Local storage for data persistence
   - Dark mode toggle

4. **Polish & deploy:**
   - Test on mobile (primary use case)
   - Accessibility audit
   - Performance optimization
   - Deploy to GitHub Pages
