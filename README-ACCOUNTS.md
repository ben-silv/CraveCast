# CraveCast — accounts and cloud sync

Off by default. CraveCast works exactly as it always has with nothing
configured: everything stays in the browser, no account, no server.

Turn this on and anyone can sign up with an email and password, verify that
email, and have their habits, logs and garden follow them to any device they
sign in on. Each account sees only its own data — the database enforces that,
not the page.

---

## Why this can't run as an Artifact

The published Artifact at `claude.ai/code/artifact/...` **cannot** use accounts.
Two hard blocks: the Artifact sandbox forbids network requests to any external
host (Google Fonts is the only exception), and its runtime has no way to tell
one viewer from another. Multi-user means a real backend, which means the app
has to be served from ordinary web hosting.

The Artifact and the Android APK keep working as the single-device version.
`index.html` is still the one source of truth for all of them.

---

## Setup — about five minutes

### 1. Create the database

1. Sign up at [supabase.com](https://supabase.com) and create a project (the
   free tier is enough). Pick a region near you.
2. In the project, open **SQL Editor → New query**.
3. Paste the whole of `supabase-schema.sql` from this folder and press **Run**.

That creates one table, locks it down so an account can only ever read or write
its own row, and adds the three functions the page calls.

### 2. Turn on email verification

In **Authentication → Sign In / Providers → Email**, make sure **Confirm email**
is on. That is the whole of "email verification" — Supabase sends the message
and will not issue a session until the link is clicked. CraveCast handles the
rest: it tells people to check their inbox, and offers a resend button if they
try to sign in too early.

> The built-in mail service is rate limited and only really suitable for
> trying this out. For real use, set your own SMTP under
> **Project Settings → Authentication → SMTP Settings**, or verification
> emails will start silently failing once a few people sign up.

### 3. Point the app at it

In Supabase, go to **Project Settings → API** and copy:

- the **Project URL** (`https://<something>.supabase.co`)
- the **anon / public** key

Open `index.html`, find the `CLOUD` block near the top of the `<script>`, and
fill both in:

```js
const CLOUD = {
  url: "https://abcdefghijklm.supabase.co",
  key: "eyJhbGciOi..."          // the anon / public key
};
```

**Use the anon key, never the service role key.** The anon key is designed to
sit in public HTML and grants nothing by itself; the row level security
policies are what confine each account to its own data. The service role key
bypasses all of them and must never leave a server.

### 4. Put it on the web

`index.html` is self-contained — no build step, no dependencies. Drag the file
onto [Netlify Drop](https://app.netlify.com/drop), or push the folder to a
GitHub repo and switch on GitHub Pages, or use Vercel. Any static host works.

Then add that URL under **Authentication → URL Configuration → Site URL** in
Supabase, so the verification links point back to your site rather than
`localhost`.

---

## What people get

| | |
|---|---|
| **Create account** | Email + password, minimum 8 characters. |
| **Verify email** | Supabase sends the link; no session is issued until it's clicked. |
| **Sign in** | Signing in on a device merges that browser's data into the account — nothing is overwritten in either direction. |
| **Sync** | Every change saves to the server about a second and a half after you stop. Opening the app anywhere pulls the latest. |
| **Forgot password** | Sends a reset link. It answers the same whether or not the address has an account, so it can't be used to find out who's registered. |
| **Delete account** | Two confirmations, then the login and all server-side data are gone for good. Data already in that browser is left alone — "Erase everything" in the footer is what clears that. |

Signed out, the app behaves as it always did and keeps everything locally.

---

## How the merge works

Signing in is not allowed to cost anyone data, in either direction, so nothing
is ever replaced wholesale:

- **Habits and logs** are unioned by id; duplicates collapse.
- **The garden** is unioned by species and the moment each thing finished
  growing. Wilted counts take the higher of the two. If something was growing
  in both places, the one planted more recently continues.
- **Settings** prefer the device in front of you, and take anything missing
  from the server.

Two devices editing at the same time is last-writer-wins on the whole document.
That's fine for one person on a phone and a laptop, which is what this is for.

---

## What has and hasn't been tested

Verified: the app is completely unaffected with `CLOUD` left empty; the merge
is correct across every case above, including a first sync, an empty account,
and an account whose selected habit no longer exists; the endpoints and
function arguments the page calls match `supabase-schema.sql` and Supabase's
documented REST API.

**Not verified against a live Supabase project.** The browser used to build
this couldn't complete outbound requests from the page, so the request/response
handling is written from the documented API rather than observed traffic. Your
first sign-up is the real test. If something fails, open the browser console —
every failure surfaces the server's own message in the account dialog, which is
usually enough to say what's wrong.

Most likely first-run snags:

- **"Email not confirmed"** on sign-in — the link hasn't been clicked yet, or
  the mail never arrived. Use the resend button; check spam.
- **Nothing happens / network error** — the Project URL is wrong, or has a
  stray path on the end. It should be just `https://<ref>.supabase.co`.
- **"permission denied for function cc_save"** — `supabase-schema.sql` hasn't
  been run, or was only partly run.
- **Verification links go to localhost** — set the Site URL (step 4).

---

## Privacy, plainly

Turning this on means addiction data leaves the device and sits in a database
you control. That is a real change from how CraveCast has worked, and the
footer text changes to say so. Anyone you give the URL to can create their own
account; they cannot see yours. You, as the project owner, *can* read the
`cravecast_state` table in the Supabase dashboard — row level security stops
other accounts, not the owner of the database. If that matters for whoever else
ends up using it, say so up front.
