# FitData website refresh and Duo verification — 15 October 2026

## Delivered

The German and English FitData landing pages now cover workout planning, active training,
structured runs, performance, nutrition, weight, AI meal review, and iPhone Duo. The
existing phone frames, visual language, Matchday pages, app switches, and download links
are preserved. Related support answers and FAQ/SEO metadata were updated. The refreshed
hero fits 320 px screens; an intrinsic grid-width problem found during review was fixed.

Website branch: `codex/matchdayxi-website`, based on `24e0c9e`. Changes remain local;
there was no push or deployment. The old `/Users/canata/fitdata-privacy-main` folder
contains privacy-only files and was not the website checkout used here.

- [Asset manifest](assets/fitdata-2026/sources.json): original paths, SHA-256 checksums,
  output dimensions, languages, build information, and video processing details.
- 34 localized October iPhone screenshot sets plus four native Duo screenshot sets,
  with WebP variants and PNG fallbacks. Original images were not retouched.
- Two 25-second silent demos: [German MP4](assets/fitdata-2026/de/duo-demo.mp4) and
  [English MP4](assets/fitdata-2026/en/duo-demo.mp4), plus WebM and localized posters.
  Each MP4 is under 1 MB.
- Playback requires a click or keyboard activation. Sources are hydrated near the
  viewport; leaving it pauses playback. Reduced-motion behavior was checked with
  a DOM-policy harness; no OS preference was changed.

Original recordings and native captures are preserved in:
`/Users/canata/FitData - Weiteres/02-Screenshots/2026-10-15-duo/`.
Only `Duo_Demo_DE_publish.mov` and `Duo_Demo_EN_publish.mov` are the published source takes.
Other takes are retained as trials and are not embedded. Window-only recording lost frames;
the published takes use a verified fixed desktop region. They have no internal cuts and
are uniformly sped up to 25 seconds; the German opening launch splash is trimmed by 1.5 s.
Captions disclose the speed change. Native transitions, including temporary blur during
pose animations, are retained.

## Simulator findings

Built the existing `feature/iphone-duo-migration` checkout with Xcode **27.1 (27A9275)**,
iOS 27.1 simulator **24A94401**, bundle `com.CanAta.FitData`, version **3.4**.
All Xcode commands used an explicit `DEVELOPER_DIR`; the global Xcode selection stayed unchanged.
Existing app-source changes were preserved. No app code, production seed, catalog data,
account data, or app settings values were edited. The local draft below was discarded.

| Check | Result |
|---|---|
| Overview | Closed carousel and open paired charts; inner portrait/landscape inspected |
| Nutrition | Paired streaks, macro tiles and weight chart inspected in Open/Book and portrait |
| Training | Paired streak/performance and two-column plans; portrait and fold/reopen inspected |
| Running | Paired cards/plans; portrait and Book inspected; loading card resolved |
| Settings | Native sidebar/detail in landscape, selected Goals detail and sidebar control in portrait |
| Route continuity | A recorded run detail remained on the same session after close/reopen |
| Settings selection | Explicitly selected Goals survived expansion and collapse |
| Draft continuity | Unsaved custom run-plan name survived unfold, rotate, close and reopen; backed out without saving |
| Ordinary iPhone | Existing four-root native-navigation test passed on iPhone 17 / iOS 27.0 |

No blocking layout or state-loss defect was observed in these inspected flows. This is a
simulator check of the listed screens, not real-device, active-session, VoiceOver, or
all-workflow certification. The test account has older populated history but sparse current-week
activity and food values; zero charts in the Duo footage reflect that data. No values were invented.
The outer-display app keeps its existing portrait orientation policy; rotating the simulated
hardware can temporarily show that portrait content upside down before reopening.

The app declares a launch screen, all four iPad orientations, and no required-full-screen
opt-out. No project-setting migration was necessary for capture.

## Verification

- `python3 -B scripts/verify_site.py`: **PASS**, 24 pages and 833 local references,
  responsive sources, video/poster files, shared app switches, and isolated blog rebuild.
- JavaScript syntax checks for navigation, consent and video loading: **PASS**.
- `git diff --check`: **PASS**.
- Browser checks in DE and EN at **320, 390, 768, 1024 and 1440 px**: hero text fits,
  no document overflow, no broken loaded images, native player controls present.
- Actual single-click EN and keyboard DE video playback: **PASS**, ready state 4, 25 s duration.
- Mobile menu Enter/Escape and focus restoration: **PASS**. German FitData → Matchday →
  FitData navigation retained language. Static checking covers all app switches.
- `FDDuoHomeLayoutTests`: **8 passing tests**, including the parameterized fallback cases.
- `TabBarUITests.testMigrationHomeRootsRemainReachable`: **PASS on Duo and iPhone 17**.
- Separate legacy failure: `NavigationUITests.testSettingsProfileNavigationAndBack` stops
  at its obsolete `homeTab` selector before entering Settings. The test was not modified;
  Settings was checked manually as above. The first combined runner stalled while finalizing
  that failed result and was stopped; the focused geometry/native-tab rerun completed successfully.

Reproduction logs, browser measurements, preview screenshots, and completed result bundles
are in the capture folder's `Verification/` directory. The focused Duo summary reports
9 passing tests (8 geometry tests plus one native-navigation test), zero failures.

## Publication follow-up outside the landing-page refresh

The retained FitData privacy pages still omit the food diary/meal-photo categories and
name only a generic AI provider; they also say provider messages are not stored beyond
the session. Synchronize these passages with the approved current in-app privacy text
before publishing the feature launch. This refresh did not rewrite legal policies or
change Matchday's legal copy.

## Documentation and source freshness

There is no new app feature or schema in this change, so the app PRD/specs were not edited.
Please reconcile their existing Duo descriptions: the PRD still calls Settings/downstream
layouts deferred, while the technical specs and this build already contain Settings split
navigation and adaptive detail layouts. The technical section also contains both root-only
and router-wide modifier descriptions.

Nutrition-source check for this editorial work: the [BLS home page](https://www.blsdb.de/)
still advertises 4.0; [Swiss downloads](https://naehrwertdaten.ch/en/downloads/) and its
[update history](https://naehrwertdaten.ch/en/versions-and-updates/) list 7.1. No later
Swiss correction was listed. The BLS download/erratum flow could not be fully revalidated,
and [Open Food Facts](https://world.openfoodfacts.org/data) blocked automated inspection.
Do not treat this as a completed catalog freshness audit. At the next catalog update,
recheck the BLS erratum and refresh the dated OFF export through the existing rebuild/reseed
runbook; production seeding remains a separate user-run step. No catalog freshness table
was changed because no import occurred.
