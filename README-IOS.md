# CraveCast — iOS app

The source is already an iOS app in everything but the build. Capacitor keeps
one `www` directory for every platform, so `index.html` is as much the iOS app
as it is the Android one, and `npx cap sync ios` copies the same output the
Android build uses.

What is *not* here is the build itself. **Xcode runs only on macOS**, and every
step Apple requires — compiling, code signing, archiving, uploading to App
Store Connect — goes through it. There is no supported way to do any of that
from Windows, so this machine can take the project right up to the point of the
build and no further.

---

## The cheapest way to do this

**$99 a year, and nothing else.** That is the Apple Developer Program fee, it
is the floor, and there is no way around it — free provisioning signs an app
onto your own device for seven days but cannot put anything on the App Store.
Every other cost can be zero.

The build runs on somebody else's Mac, on a free CI tier:

| | Free allowance | What it costs you |
|---|---|---|
| Apple Developer Program | — | **$99/yr**, unavoidable |
| Codemagic | 500 macOS minutes/month, personal account, reset on the 1st | **$0** |
| GitHub Actions, private repo | 2,000 minutes/month, but macOS bills at 10× — so 200 real minutes | **$0** |

A Capacitor build of this size runs in well under ten minutes, so Codemagic's
500 minutes is roughly fifty builds a month. You will not get near it.

**Use Codemagic, not GitHub Actions.** Not because of the minutes, but because
of code signing. Codemagic creates and renews the distribution certificate and
provisioning profile itself, through the App Store Connect API, at build time.
On GitHub Actions you generate a certificate signing request by hand, convert
the result to a .p12, import it into a temporary keychain on the runner, and
manage an exportOptions plist. It is doable from Windows with OpenSSL, and it
is where most of the failures live. `codemagic.yaml` in this repo is already
written for the automatic path.

### What you do once, in a browser

1. Enrol in the Apple Developer Program. Allow a day or two; individual
   enrolment sometimes needs identity verification.
2. Register `com.cravecast.app` as an App ID, and create the app record in App
   Store Connect.
3. App Store Connect → Users and Access → Integrations → App Store Connect API.
   Generate a key with the **App Manager** role and download the `.p8`. It is
   downloadable exactly once.
4. In Codemagic, add that key as an App Store Connect integration named
   `CraveCast ASC key`, which is the name `codemagic.yaml` refers to. Connect
   the repository.
5. Push a tag matching `v*`. That is the build trigger, so ordinary commits do
   not burn minutes.

The build ends by delivering to TestFlight. Promoting a TestFlight build to
review is left as a manual step in App Store Connect, deliberately — it should
follow a run on a real phone, not a green CI check.

### The cost that is not money

**You need an iPhone or iPad to test on.** Not for the build, which is entirely
remote, but because without one there is no way to run this before submitting
it. There is no simulator on Windows, and TestFlight only installs on Apple
hardware. Submitting an app you have never seen running is how you spend two
weeks in rejection cycles over something a five-minute install would have
caught. Borrowing one for an evening is enough; you also need it for the App
Store screenshots.

If you would rather not use CI at all, a rented Mac by the hour (MacinCloud,
MacStadium) is a few dollars for a one-off submission, and a used Apple-silicon
Mac mini is a few hundred. Neither is cheaper than free, and both still need
the $99.

---

## The build, once you have macOS

Only relevant if you go the rented-Mac or owned-Mac route. On CI this is all
`codemagic.yaml`'s job and you never run it yourself.

The repo is the Capacitor project: `package.json`, `package-lock.json` and
`capacitor.config.json` are committed, and everything they generate (`www`,
`ios`, `node_modules`) is not.

```bash
git clone <this repo> ~/Tracker && cd ~/Tracker
npm ci
sudo gem install cocoapods          # or: brew install cocoapods

APP=$PWD ./rebuild-ios.sh           # builds www, cap add ios, cap sync, opens Xcode
```

`rebuild-ios.sh --archive` goes straight to an archive instead of opening the
IDE. `TRACKER=` and `APP=` override the two paths if you lay things out
differently.

In Xcode, once per project:

- **Signing & Capabilities** — check *Automatically manage signing*, pick your
  team. Bundle identifier is `com.cravecast.app`; register it on the developer
  portal first, or let Xcode do it.
- **Deployment target** — Capacitor 8 wants iOS 14 or later. Leave the default
  unless you have a reason.
- **Push Notifications** is *not* needed. Local notifications require no
  capability and no Info.plist string.

Then Product → Archive → Distribute App → App Store Connect.

---

## What changed in the source to make this work

All of it is shared with Android and the web page — there is still exactly one
`index.html`.

- `viewport-fit=cover` on the viewport meta. The `.native` rules already padded
  for `env(safe-area-inset-*)`, but without this iOS reports those insets as
  zero and the masthead sits under the notch.
- Form controls go to 16px inside the native shell. Anything smaller makes
  WKWebView zoom the page when a field takes focus, and it never zooms back.
- Tap highlight and long-press callout suppressed, page-level rubber-band
  scrolling turned off. These are the three things that make a webview read as
  a webview.
- **Export JSON now goes through the OS share sheet on a phone.** WKWebView
  refuses an anchor download with a blob URL, so the button did nothing at all
  in a native shell. It now writes to the app cache via `@capacitor/filesystem`
  and hands the file to `@capacitor/share`; the browser keeps the blob path.
- The armed-state text says "queued with iOS" or "queued with Android" rather
  than assuming Android.
- A disclaimer in the footer saying this is not medical advice — see *Review
  risks* below.

Two Android bugs found on the way, both fixed:

- `build-android.py` was still downloading Archivo, IBM Plex Mono and Public
  Sans while the app had moved to Baloo 2 and Nunito, so the offline bundle
  matched nothing and the installed app fell back to system fonts. It is now
  `build-native.py` and reads the font families out of the source's own
  stylesheet link, so it cannot drift again.
- The Capacitor `backgroundColor` was `#E7EBEF` against an app background of
  `#FBF4E3`, which is a flash of the wrong colour on every launch. Both
  platforms now use the app's own value.

---

## Notifications on iOS

The scheduling code needed no change. Worth knowing anyway:

- iOS allows **64 pending notifications** per app. `MAX_SCHEDULED` is 24.
- `allowWhileIdle`, `channelId` and `smallIcon` are Android-only and are
  ignored rather than erroring.
- Scheduled notifications survive both app termination and reboot, same as the
  Android alarms.
- iOS will not wake the app to re-plan. The queue is refilled on launch and on
  foreground, so a week of never opening the app is a week of no warnings — the
  same limit Android has, for the same reason.

---

## Assets you still have to make

- **App icon** — done, but treat it as a starting point. `make-icon.py` renders
  `assets/icon.png` at 1024×1024 in opaque RGB, since Apple rejects an icon
  carrying an alpha channel. It is the same forecast-ridge mark as the Android
  adaptive icon, scaled up (iOS has no adaptive mask to hide inside) and moved
  off Capacitor's stock teal grid onto the app's own palette. The CI build feeds
  it to `@capacitor/assets`, which cuts every size Xcode wants. Replace the PNG
  and rerun if you want something better drawn.
- **Screenshots** for the largest iPhone size App Store Connect currently asks
  for; it scales them down for smaller devices. Add a 13-inch iPad set only if
  you ship for iPad. Check the current required dimensions in App Store Connect
  rather than trusting a number written here.
- **Privacy policy at a public URL.** Required for every app, no exceptions.
  With accounts off this is short and true: nothing is collected, nothing
  leaves the device.

---

## App Store Connect, in order

1. Register `com.cravecast.app` as an App ID.
2. Create the app record. Check the name **CraveCast** is free — App Store names
   are unique, and a taken name is a common surprise.
3. **App Privacy.** Accounts are off, everything lives in `localStorage`, so the
   honest answer is **Data Not Collected**. If you ever fill in the Supabase
   config, this answer changes and so does the footer text.
4. **Age rating questionnaire.** Expect the alcohol, tobacco and drug reference
   question to apply — the app is about quitting a substance. Answer it; a wrong
   age rating is a rejection.
5. **Export compliance.** No custom cryptography, standard HTTPS only, so the
   exemption applies.
6. Upload the build, attach it, fill in description and keywords, submit.

---

## Review risks, honestly

**Guideline 1.4.1, health and medical.** This is the real one. An app that
forecasts cravings in someone quitting a substance sits close to the line Apple
draws around medical claims, and reviewers give that category extra scrutiny.
Three things help, and the first is now in the app:

- The footer disclaimer: a self-tracking tool, not medical advice, not a
  treatment, and the forecast is a pattern in your own logs rather than a
  clinical prediction.
- Say the same thing in the App Store description, and in the review notes.
- Do not describe it anywhere as preventing relapse, treating dependence, or
  predicting a health outcome. Forecast, pattern and log are the safe words.
  Treat, prevent and diagnose are not.

**Guideline 4.2, minimum functionality.** Webview wrappers get rejected when
they are a website in a shell. CraveCast should clear this: it runs fully
offline, holds its own data, and schedules OS-level notifications. If it is
questioned, that list is the answer.

**Guideline 2.1, completeness.** No login is required, so no demo account is
needed. Mention in the review notes that the forecast starts from a population
baseline, so a reviewer opening it cold still sees a working forecast rather
than an empty state.

**The one nobody here can resolve for you.** The cold-start prior is fitted from
two human-subjects datasets. Whatever agreement those came under may not cover
redistributing derived parameters inside an app on a commercial store, even
though the raw data never ships. That is worth checking with whoever holds the
data before you submit, not after.

---

## Not tested on a device

Everything above is a source and configuration change verified by build and by
running the page in Chrome, which is a different engine from WKWebView. The
Android APK was rebuilt and still builds clean. The iOS-specific behaviour —
safe-area insets, the share sheet export, notification delivery — has not been
run on an iPhone or a simulator, because neither exists on this machine. Budget
a pass on a real device before the first submission.
