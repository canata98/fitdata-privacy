# Matchday website refresh — October 16, 2026

> Publication follow-up, October 16: owner approved publishing after this local review. Content commit `d23fbe8` is live on `fitdata.app`; all twelve checked pages returned HTTP 200 and matched the reviewed HTML exactly. The app links were updated separately in app commit `474e2ff`. Earlier 404/local-only observations below record the pre-publication stage.

## Scope

Compared the current FitData website commit `7acd97b` (FitData 3.4 content,
iPhone Duo, updated legal pages and hidden blog) with all ten Matchday DE/EN pages.
App/backend evidence: Matchday source `1cdcb10`, privacy collection documentation
and completed production rollout documented in app repository commit `46b7bff`.
This task updates website content only; no app, backend, account, consent, domain,
DNS or hosting configuration was changed.

## What changed

- Privacy DE/EN: twelve matching sections plus a short overview and direct links
  to choices, account deletion and rights. Updated date October 16, 2026.
- Explain technical Firebase guest accounts, necessary shared league data,
  purposes/legal bases, local choices and caches, APNs/FCM, two initially disabled
  optional telemetry switches, withdrawal/reset behavior and Crashlytics buffering.
- Remove the obsolete statement that the current app attaches the account UID to
  crash reports. Preserve the distinction between no app-supplied account ID and
  technical SDK/installation identifiers; no complete-anonymity claim.
- Describe direct BSD data/image requests and the conditional football-data badge
  fallback. Do not claim all requests go through the backend. Do not reintroduce
  TheSportsDB as an active provider.
- Describe actual processing locations (EU Firestore, US Cloud Functions), GitHub
  Pages hosting and technical IP logs. Matchday continues to load no website analytics.
- Explain the deployed deletion flow and surviving league history/technical references.
  No invented automatic season-end cleanup or blanket 30-day deletion promise.
  Google's 90-day Crashlytics period is described as the start of removal, not a
  guarantee that every backup copy is already erased at day 90.
- Support DE/EN: privacy-choice answer and linked deletion guidance, including
  possible reauthentication and not emailing credentials.
- Landing DE/EN: privacy FAQ, matching FAQ structured data and refreshed FitData
  discovery wording covering training, running, nutrition and progress.
- Terms DE/EN: provider link, virtual nature of game money and optional telemetry.
  Imprint: reviewed provider/contact data; German DDG reference added.
- Shared Matchday document styles: paragraph/list spacing and sticky-header anchor
  offsets for the longer privacy pages. Versioned stylesheet reference on all ten pages.

## FitData similarities and boundaries

| Topic | Current FitData website | Matchday update |
|---|---|---|
| Design | Existing typography, navigation, frames and app discovery | Same visual structure, Matchday green preserved |
| App switches | Alternate app after Imprint | Placement preserved in header and footer; language preserved |
| Guest mode | FitData describes local guest data | Matchday describes a technical Firebase guest account |
| Telemetry | FitData text describes disabling collection | Matchday accurately describes two separate, initially disabled opt-ins |
| Processing region | FitData text describes Frankfurt Functions | Matchday uses verified EU Firestore and US Functions locations |
| Account deletion | FitData text states a 30-day period | Matchday retains necessary historical league references; no borrowed deadline |
| Features | Fitness, nutrition, AI, Apple Health, subscription, Watch and Duo | No unrelated health/AI/subscription claims imported into Matchday |
| Blog | FitData navigation currently hides the blog | No Matchday blog introduced |

FitData app source/data behavior was not audited in this website task. Its newer
text is a reference for structure, not proof that every statement transfers to Matchday.

## Verification

- Before changes: existing checker passed, 24 pages and 801 local references.
- After changes: checker passed, 24 pages and 819 local references, including local
  targets/anchors, image assets, canonical/language metadata, app-switch placement
  and isolated blog regeneration preserving Matchday sitemap entries.
- `node --check assets/nav.js` and `node --check analytics-consent.js`: passed.
- Browser at the current narrow in-app viewport: DE and EN privacy pages rendered
  with the October 16 date, readable paragraphs/lists and no observed clipping.
  The privacy jump link scrolled below the sticky navigation.
- Mobile menu showed FitData immediately after Imprint. DE → EN stayed on Privacy.
  Matchday EN → FitData EN → Matchday EN worked; the updated privacy FAQ expanded
  and displayed the corresponding answer.
- No new JavaScript, analytics tag, external font, signup form, download URL or
  media processing was introduced. The original screenshots and FitData frames remain.
- Existing FitData root HTML and asset hashes were compared with the pre-change
  baseline. Existing untracked FitData image/video files were preserved and excluded
  from this commit.
- Browser screenshot saved locally at
  `/private/tmp/matchday-website-privacy-de-20261016.png`.
- Local preview: `http://127.0.0.1:8766/matchdayxi/privacy-de.html`.

## Public deployment status

Read-only HTTP checks: `https://fitdata.app/` returned **200** with GitHub hosting;
both `/matchdayxi/privacy-de.html` and `/matchdayxi/privacy-en.html` returned **404**.
GitHub Pages configuration: `main`, root `/`, HTTPS enforced, status built.
No push, merge or deployment was performed. The local implementation remains on
`codex/matchdayxi-website`; publishing it is a separate step from this preview.
The app still points to the old `canata.app/rematch/...` privacy/terms URLs;
changing website files does not change the binary. Change app links only after
publishing and checking the actual new DE/EN targets.

## Remaining owner checks

- Read the actual Analytics property retention settings and reconcile the public
  retention wording with the configured duration. This setting was not available
  from the local source; no default period was invented.
- Document the necessity/duration and manual review of surviving historical
  identifiers. The season-end-plus-30-day proposal is not an implemented scheduler.
- Verify provider agreements/international-transfer safeguards and remaining
  sports/media rights. Naming a provider in the privacy page does not grant image rights.
- Verify support mailbox delivery and signed-device optional-upload behavior.
- No full legal review or public reachability of the new content is claimed.

Provider references checked October 16, 2026:
[Firebase privacy, processing and retention](https://firebase.google.com/support/privacy),
[BSD privacy](https://sports.bzzoiro.com/docs/privacy/),
[GitHub Pages IP logging](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection),
[GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng).
