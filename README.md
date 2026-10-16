# FitData & Matchday XI website

## Published — October 16, 2026

The owner authorized publication after the local review. Content commit `d23fbe8`
was fast-forwarded to `main`; GitHub Pages built it successfully. All ten Matchday
pages and the two FitData landing pages returned HTTP 200 with HTML identical to
the reviewed local files. The publication did not include the 23 existing untracked
FitData media variants; an isolated `git archive` verification confirmed they are
not required by the committed pages. Earlier local-only notes below describe the
implementation stages before this publication.

Public Matchday DE/EN privacy and terms pages are now reachable. The app repository
was updated separately in commit `474e2ff` to use these pages in the app's language.
The previous `canata.app/rematch/...` URLs are no longer the current app targets.
The publication itself does not complete the remaining signed-device, provider
retention or data/media-rights checks documented in the refresh report.

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
switch stays on the equivalent page. FitData keeps its blog sources, but the refreshed navigation hides the blog. Matchday has no blog.

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
Its app Analytics/Crashlytics choices are separate from website tracking: two optional switches, both initially disabled, under Profile → Privacy.

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
reviewed in both languages. The October 16 Matchday refresh now reflects the deployed deletion flow, two optional telemetry choices, guest authentication, direct sports-data/image requests, processing locations and website hosting. It does not change the app's processing or establish legal approval; actual Analytics retention and historical-identity review remain explicit publication checks.

## Publication is a separate step

This branch is a local implementation. Do not push or deploy as part of previewing.
Before publication:

1. Confirm provider/contact details copied from the existing FitData imprint.
   Matchday uses the app's existing `support@canata.app` contact.
2. Review the October 16 DE/EN privacy/terms update against the final distributed
   app. The backend deletion rollout is complete; actual Analytics retention,
   necessary historical identity retention and provider agreements still need
   owner verification. Current texts describe known technical limits; they are
   not a declaration of legal approval.
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

## FitData refresh — October 15, 2026

FitData DE/EN now includes nutrition, structured runs and an iPhone Duo showcase.
Current screenshot derivatives, native Duo stills, 25-second MP4/WebM demos and posters
are under `assets/fitdata-2026/`; `sources.json` records provenance and processing.
Originals stay in `02-Screenshots/2026-10-15-duo` outside this repository.

The Duo player uses `data-user-playback`, native controls and a localized Play button.
It loads sources near the viewport, pauses offscreen, and does not autoplay.
`assets/fitdata-refresh.css` is loaded only by the FitData landing pages.
Changed script/style URLs are versioned to avoid stale cached assets.

See [the refresh and simulator report](FITDATA-REFRESH-2026-10-15.md) for verification,
recording details, the existing legacy UI-test selector failure and PRD/specs follow-up.
Publication remains separate from this local branch.

## Matchday privacy and support refresh — October 16, 2026

See [the comparison and verification report](MATCHDAY-PRIVACY-REFRESH-2026-10-16.md).
All ten Matchday pages were reviewed after the FitData 3.4 website refresh.
Privacy is now aligned in DE/EN with optional Analytics/Crashlytics, technical guest
accounts, shared league data, direct sports/image requests, current processing
locations and the deployed account-deletion flow. Support and landing FAQs explain
the privacy choices; the FitData discovery card now includes nutrition and progress.
Phone frames, screenshots, app-switch placement and all FitData pages/assets are preserved.

The public root returned HTTP 200, while both Matchday privacy URLs returned HTTP 404
on October 16. GitHub Pages is configured to publish from `main` at `/`, with HTTPS
required. This refresh is local on `codex/matchdayxi-website`; no push, merge or deployment
was performed. App `GSAppLinks` still needs the separate agreed change after the new
public URLs have been published and verified.
