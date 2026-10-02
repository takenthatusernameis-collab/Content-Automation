# STATE

Updated: 2026-10-02T12:25:00Z (Run 274)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter + labeled generated fallback + local card generator + WORDS timeline planner + fail-closed media QA + authenticated YouTube uploader (dry-run default, execute path) + authenticated feedback ingestion (dry-run default, execute path) + fail-closed ffmpeg assemble planner + fail-closed feedback/experiment/complete gates + documented experiment baseline contract + gate-machine drop recipe + Actions materialize/dry-run verified -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning` status `ready_for_vo`
- Durable fetch: private release `q1-media-r253` (padded master) plus r249 wav/cards
- r249 master is truncated (308.40s). Finished local export is `q1-media-r253` `q1-master-r253.mp4` (328.40s).
- Actions dry-run 36983196381 materialized that set and reached `YOUTUBE_AUTH_REQUIRED`. Execute was not dispatched.
- Executive: SHIP after the three YouTube OAuth secrets exist and `youtube-production.yml` is dispatched with execute=true. Do not re-encode. Do not upload r249. Do not expand architecture. Do not spend a run only restating the secret hold.

## Run 274 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `experiment_loop.py` now computes one numeric primary-metric delta when a documented baseline and one collected value exist. Action is `COMPARED`. Decision stays `pending`. `result` stays null.
- A missing, non-numeric, or conflicting primary metric is `COMPARE_BLOCKED_METRIC`. `complete.py` requires a keep/discard/retest decision, so a delta cannot mark COMPLETE.
- No Q1 baseline file was written. Selftest passed locally.

## Run 273 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `experiment_loop.py` now loads `experiment_baseline.json` when present. Invalid or invented sources stay `COMPARE_BLOCKED_NO_BASELINE`. A valid file becomes `COMPARE_READY` and still does not choose keep/discard.
- No Q1 baseline file was written. There is no prior observation to cite.
- Selftest passed locally.

## Run 272 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `tools/oauth_preflight.py` now runs before ffmpeg and materialize when `youtube-production.yml` is dispatched with execute=true. Missing or blank secrets exit 3 and print names only.
- Dry-run path is unchanged. Selftest passed locally.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 0.5 | 0.5 | OAuth secret entry remains; post-publish comparison no longer needs a hand-computed delta |
| Automated steps | 108 | 109 | numeric delta is computed; keep/discard still pending |
| Videos produced | 0 | 0 | no provider write |

## Active constraints
- Do not upload q1-media-r249 q1-master.mp4 as the finished export
- Do not abort materialize merely because that banned asset is present in the r249 release
- Finished local export is q1-media-r253 q1-master-r253.mp4 (328.40s, sha256 4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546)
- Do not re-encode while q1-media-r253 exists
- Do not scaffold Q2
- Do not restore the stub sentence `No upload happened`
- Do not dispatch youtube-production.yml with execute=true until the three OAuth secrets exist
- Do not remove the oauth_preflight step or move it after materialize
- Do not regenerate thumbnail.png, chapters.md, or captions.srt while source checksums are unchanged
- Do not invent experiment_baseline.json for Q1
- Do not treat COMPARED or a numeric delta as a keep/discard
- Do not invent experiment_baseline.json for Q1
