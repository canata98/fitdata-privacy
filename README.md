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

The current website uses the screenshots supplied by the owner in
`/Users/canata/Goalscorer - Weiteres/Goalscorer-Screenshots/`:

- `Fantasy/DE` and `Fantasy/EN`: `Market.png`, `Lineup.png`.
- `Builder/DE` and `Builder/EN`: `Pitch.png`.

These six screenshots replace the earlier provisional onboarding captures.
They are only resized, without retouching the UI. `sources.json` records the
source paths, original and website SHA-256 checksums, and output dimensions.
Some supplied files have mismatched names or partially translated UI; only the
visually verified market, lineup and builder views are used in matching sections.
No claim is made that supplied images prove current backend or device behavior.

The phone frame is the **same** `assets/iphone17-frame.svg` used by FitData,
rendered as a CSS overlay with the same screen inset and clipping geometry.
No black-border substitute or AI-generated phone mockup is used.

The alternate app follows Imprint directly in both header and footer, on both
sites and in blog templates. Language and download controls remain separate.
The static checker verifies this placement, including generated articles.

Landing-page, support, FAQ, metadata, privacy, terms and contact copy have been
reviewed in both languages. Legal processing/deletion limits and provider details
remain consistent with the earlier technical draft; the review is editorial,
not legal approval or a change to the app's data processing.

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
