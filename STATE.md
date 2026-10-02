# STATE

Updated: 2026-10-02T09:15:00Z (Run 271)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter + labeled generated fallback + local card generator + WORDS timeline planner + fail-closed media QA + authenticated YouTube uploader (dry-run default, execute path) + authenticated feedback ingestion (dry-run default, execute path) + fail-closed ffmpeg assemble planner + fail-closed feedback/experiment/complete gates + gate-machine drop recipe + Actions materialize/dry-run verified -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning` status `ready_for_vo`
- Durable fetch: private release `q1-media-r253` (padded master) plus r249 wav/cards
- r249 master is truncated (308.40s). Finished local export is `q1-media-r253` `q1-master-r253.mp4` (328.40s).
- Actions dry-run 36983196381 materialized that set and reached `YOUTUBE_AUTH_REQUIRED`. Execute was not dispatched.
- Executive: SHIP after the three YouTube OAuth secrets exist and `youtube-production.yml` is dispatched with execute=true. Do not re-encode. Do not upload r249. Do not expand architecture.

## Run 271 delta
- OAuth secrets remain unset. Execute was not dispatched. Videos published stay 0.
- `experiment_loop.py` and `complete.py` now read metrics only from a collected `feedback_state.json` whose video id matches `upload_state.json`.
- A dry-run or mismatched feedback file stays HOLD_NO_EVIDENCE. Collected metrics become READY_TO_COMPARE / INCOMPLETE_LEARNING and still do not invent a keep/discard.
- Selftest passed locally after the change.

## Run 270 delta
- Dispatched the production workflow. First run 36982959831 failed because materialize treated the expected truncated r249 master as fatal.
- Guard now ignores that known sha, refuses an unexpected r249 master sha, and still refuses installing the banned sha as export/master.mp4.
- Second run 36983196381 succeeded: ignored truncated master, installed r253 master, 7 cards, and wav. Dry-run gate YOUTUBE_AUTH_REQUIRED. Captions and thumbnail uploaded=false. No provider write.
- Remaining manual boundary: add YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN as GitHub Actions secrets.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 0.5 | 0.5 | OAuth secret entry remains; post-upload evidence path no longer drops collected metrics |
| Automated steps | 105 | 106 | collected feedback is visible to experiment and complete gates |
| Videos produced | 0 | 0 | no provider write |

## Active constraints
- Do not upload q1-media-r249 q1-master.mp4 as the finished export
- Do not abort materialize merely because that banned asset is present in the r249 release
- Finished local export is q1-media-r253 q1-master-r253.mp4 (328.40s, sha256 4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546)
- Do not re-encode while q1-media-r253 exists
- Do not scaffold Q2
- Do not restore the stub sentence `No upload happened`
- Do not dispatch youtube-production.yml with execute=true until the three OAuth secrets exist
- Do not regenerate thumbnail.png, chapters.md, or captions.srt while source checksums are unchanged
