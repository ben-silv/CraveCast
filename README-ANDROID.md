# CraveCast — Android app

`CraveCast.apk` (4.4 MB) is a real Android app. Unlike the web version, its
warnings are handed to **Android's alarm scheduler**, so they fire whether or
not the app is open — including after a reboot.

---

## Install it on your phone

**Route A — USB cable (easiest if the phone is to hand)**

1. On the phone: Settings → About phone → tap **Build number** seven times to
   unlock Developer options.
2. Settings → System → Developer options → turn on **USB debugging**.
3. Plug the phone into the PC and accept the "Allow USB debugging?" prompt.
4. On the PC, run:

   ```powershell
   . "C:\Users\silve\AppData\Local\cravecast-build\env.ps1"
   adb install -r "C:\Users\silve\OneDrive\Desktop\Tracker\CraveCast.apk"
   ```

**Route B — no cable**

Copy `CraveCast.apk` to the phone (email it to yourself, Google Drive, or the
OneDrive folder it already lives in), open it in the phone's Files app, and
approve "install unknown apps" for whichever app you opened it from.

---

## Two settings to check after installing

These are the difference between warnings that arrive and warnings that don't.

1. **Allow notifications.** The app asks the first time you tap
   *Arm early warnings*. If you miss it: Settings → Apps → CraveCast →
   Notifications → allow.

2. **Exempt it from battery optimisation.** Settings → Apps → CraveCast →
   Battery → **Unrestricted**. Android's Doze mode, and the more aggressive
   battery managers on Samsung / Xiaomi / OnePlus phones, will otherwise delay
   or drop scheduled alarms. This is the single most common reason a scheduled
   notification never shows up.

---

## How the alerting differs from the web version

| | Web page | Android app |
|---|---|---|
| Who holds the schedule | a timer in the open tab | Android's `AlarmManager` |
| Fires with the app closed | no | **yes** |
| Survives a reboot | no | yes |
| How far ahead it plans | the live moment | next 7 days, up to 24 warnings |
| Re-planned when | continuously | on log, on settings change, on app open |

The app queues warnings for the next week and re-plans them every time you log
an urge, change a setting, or reopen the app — so the schedule always matches
the current forecast.

---

## Rebuilding after you edit the app

`index.html` in this folder is the **single source of truth** for all three
targets — the web page, the published Artifact, and the Android app. It detects
at runtime whether it's inside the Android shell and switches its alerting
accordingly, so there is only ever one copy of the logic to edit.

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\silve\CraveCastApp\rebuild.ps1
```

That copies `index.html` into the app (swapping the Google Fonts link for the
bundled offline fonts), syncs Capacitor, builds, and drops a fresh
`CraveCast.apk` back into this folder. Takes a few seconds once warm.

To refresh the published web version instead:

```powershell
python C:\Users\silve\OneDrive\Desktop\Tracker\build-artifact.py
```

---

## Where everything lives

| Path | What |
|---|---|
| `Desktop\Tracker\index.html` | the app itself — edit this |
| `Desktop\Tracker\CraveCast.apk` | the installable Android build |
| `Desktop\Tracker\build-android.py` | index.html → app web assets (+ offline fonts) |
| `Desktop\Tracker\build-artifact.py` | index.html → Artifact fragment |
| `Desktop\Tracker\supabase-schema.sql` | database + policies for the optional accounts |
| `Desktop\Tracker\README-ACCOUNTS.md` | how to switch accounts and cloud sync on |
| `Desktop\Tracker\fit-prior.py` | refits the cold-start baseline from the survey workbook |
| `Desktop\Tracker\prior.js` | its output — the `PRIOR` block pasted into index.html |
| `C:\Users\silve\CraveCastApp` | Capacitor + Android project (kept out of OneDrive) |
| `%LOCALAPPDATA%\cravecast-build` | portable Node 24 / JDK 21 / Android SDK |

The toolchain is entirely self-contained: nothing was added to your system
PATH, registry, or Program Files. Deleting
`C:\Users\silve\AppData\Local\cravecast-build` (~2.5 GB) removes every build
tool and leaves the installed app on your phone untouched — you'd just need to
re-download them to build again.

---

## Known limits

- **Debug-signed.** Fine for sideloading onto your own phone. It can't go on
  the Play Store as-is, and `USE_EXACT_ALARM` would need justification there.
- **Keep the debug keystore.** It lives at `%USERPROFILE%\.android\debug.keystore`.
  If it's deleted, future builds get a different signature and Android will
  refuse to upgrade over the installed app — you'd have to uninstall first.
- **Untested on a device.** The build is verified (permissions, signature,
  bundled assets) and the app logic was tested in Chrome, which is the same
  engine as the Android WebView. The Capacitor bridge calls themselves have
  only been verified statically — this machine has virtualisation disabled in
  firmware, so no emulator could run here.
- **Old Android (below 8.0)** falls back to the stock Capacitor launcher icon;
  the custom adaptive icon needs API 26+.
