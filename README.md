# FitData & Matchday XI website

Static HTML/CSS/JavaScript, with German and English pages. No application build,
Node dependencies or additional hosting service is required.

## Local preview

From this repository:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

- FitData EN: `http://127.0.0.1:8765/index.html?lang=en`
- FitData DE: `http://127.0.0.1:8765/index-de.html?lang=de`
- Matchday EN: `http://127.0.0.1:8765/matchdayxi/`
- Matchday DE: `http://127.0.0.1:8765/matchdayxi/index-de.html`

Matchday has ten pages: home, support, privacy, terms and imprint, each in DE/EN.
Its future public base URL is `https://fitdata.app/matchdayxi/`. The header and
footer switch between apps without changing the selected language. The language
switch stays on the equivalent page. FitData retains its blog; Matchday has none.

## Editing and verification

- Shared fonts, navigation and shell: `assets/site.css`, `assets/nav.js`.
- Matchday theme: `matchdayxi/assets/matchday.css`; content: `matchdayxi/*.html`.
- FitData article shell: `scripts/build_blog.py`. Keep both app-switch links when
  updating templates. Existing generated articles are rebuilt from their Markdown.
- Matchday sitemap entries are outside the generated blog block.

Run:

```sh
python3 -B scripts/verify_site.py
node --check assets/nav.js
node --check analytics-consent.js
```

The checker validates local links, anchors, image references, language/canonical
metadata, app switches, and an isolated blog regeneration. It writes only to a
temporary directory. CI performs the same checks; the workflow does not deploy.

## Analytics

FitData's existing consent-based analytics can load only on `fitdata.app` or
`www.fitdata.app`. Other hostnames, including localhost, return before reading
consent or contacting Google. Matchday does not include the analytics script.
Its existing app Analytics/Crashlytics behavior is separate from website tracking.

## App image provenance

Six actual app screenshots (DE/EN) are stored under
`matchdayxi/assets/screenshots/`: the Fantasy welcome screen and two onboarding
pages. They were captured on a separate iPhone 17 demo simulator on October 15,
2026 and resized without changing their contents. `sources.json` lists the original
XCTest attachment names. No production account or league was photographed.

The first Xcode run stalled during diagnostic collection and did not produce a
usable result bundle. The repeat with `-collect-test-diagnostics never` and the
English run completed. Their bundles are temporarily available at
`/private/tmp/matchday-website-shots-de-retry.xcresult` and
`/private/tmp/matchday-website-shots-en.xcresult`.

The legacy screenshot test can report success without reaching every intended
screen: its Builder tab selector is outdated and its registration flow did not
complete. Images labelled Pitch/CreateLeague were actually authentication sheets
and were discarded. This is not a successful market/lineup/backend flow test.
Market, lineup and standings images require a separate prepared capture before
using such images in Store material. This website labels onboarding images as
introductions; it does not portray them as those missing gameplay screens.

## Publication is a separate step

This branch is a local implementation. Do not push or deploy as part of previewing.
Before publication:

1. Confirm provider/contact details copied from the existing FitData imprint.
   Matchday uses the app's existing `support@canata.app` contact.
2. Finalize the public privacy/terms text, processing grounds, retention policy,
   relevant provider/hosting details and release/backend state. Current texts
   describe known technical limits; they are not a declaration of legal approval.
   In particular, account deletion retains some historical IDs and does not
   separately erase existing Analytics/Crashlytics records. Do not import
   FitData's blanket 30-day deletion promise or HealthKit/AI/subscription sections.
3. Confirm rights to sports data/media and review the final screenshots and claims.
4. Add the real App Store URL once an ID is assigned. Until then, Matchday shows
   “Coming soon” and contact links, without a fake download button or signup form.
5. After publishing and verifying every URL, update the Matchday app's
   `GSAppLinks` and Store metadata together. They still point to the previous
   `canata.app/rematch` URLs in this local-only phase.
6. Review the existing GitHub Pages setup and workflows before any push to `main`.
   The FitData blog workflow can commit generated content; no deployment settings,
   domain, DNS, repository remote or `CNAME` were changed here.

## Local verification — October 15, 2026

- Both apps in DE/EN: browser checks at 320, 390, 768, 1024 and 1440 px;
  no horizontal overflow or broken loaded images; no injected Google analytics tags.
- App switch in both directions; DE/EN switch on the same privacy page.
- Mobile menu: focus enters links, Escape closes and restores focus to the toggle.
- Navigation without JavaScript: checked on a local CSP-blocked preview for both apps at 390 px; app links remain visible and usable without overflow.
- `verify_site.py`: all local references and isolated blog regeneration passed.
- These checks do not verify live deployment, mail delivery, App Store access,
  legal completeness, real-device app behavior or a productive backend rollout.
