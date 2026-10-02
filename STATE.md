# STATE

Updated: 2026-10-02T21:13:00Z (Run 282)

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

## Run 282 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now reads granted scopes after refresh and raises `SCOPE_INSUFFICIENT` before `videos.insert` when caption or thumbnail scope is missing. An upload-only token cannot create a private video that then loops on caption failure. A scope refusal does not write `upload_state.json`.
- Required consent scopes are documented as `youtube.upload` plus `youtube.force-ssl`, or the full `youtube` scope. Analytics scope remains collect-only. Selftest passed locally. Actions was not re-run.

## Run 281 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now refuses a title over 100 characters, a description over 5000, more than 12 tags, tags whose characters sum over 500, or a tag with a comma or angle bracket. Inspect gate is HOLD_LOCAL. Execute raises METADATA_REJECTED before the token refresh and refuses a non-private privacy status.
- Tags are no longer silently sliced to 12. Q1 publish copy passes the new limit. Selftest passed locally. Actions was not re-run.

## Run 280 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- Upload identity no longer includes export mtime. The same bytes keep the same fingerprint after rematerialize.
- A persisted video id with a matching fingerprint and incomplete caption, thumbnail, or failed comment is gate RESUME. Execute retries those artifacts and does not upload a second video.
- A matching finished upload stays HOLD_IDEMPOTENT. A different fingerprint stays HOLD_FINGERPRINT_MISMATCH and execute refuses EXISTING_VIDEO_FINGERPRINT_MISMATCH.
- Selftest passed locally. Actions was not re-run.

## Run 279 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now exits non-zero with `POST_UPLOAD_INCOMPLETE` when caption, thumbnail, or requested comment upload fails after a provider video id exists. The video id and any existing `uploaded_at` stay in `upload_state.json`.
- `youtube-production.yml` persists that state even when the execute step fails. A same-dispatch `collect_feedback` is skipped because the 7-day window cannot be due. Selftest passed locally. Actions was not re-run.

## Run 278 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now copies an existing `uploaded_at` onto a resumed upload. A missing stamp stays missing. A fresh upload writes the same stamp on `video_upload.uploaded_at` and `uploaded_at`. Selftest passed locally. Actions was not re-run.

## Run 277 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_feedback.py` now refuses a collect until `upload_state.json` has `video_upload.uploaded_at` or `uploaded_at` at least 7 days old. Missing time is `OBSERVATION_WINDOW_UNKNOWN`. An earlier time is `OBSERVATION_WINDOW_NOT_DUE`. Neither path writes COLLECTED. Selftest passed locally. Actions was not re-run.

## Run 276 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube-production.yml` now accepts `collect_feedback` (default false). Collect-only skips media materialize, runs `youtube_feedback.py --execute`, then writes experiment state. It commits feedback only when gate is COLLECTED. It does not invent a baseline or decision.
- Authenticated dispatches still fail closed in `oauth_preflight.py` before media or provider calls. Selftest passed locally. Actions was not re-run.

## Run 275 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `experiment_loop.py` now loads `experiment_decision.json` only after a numeric comparison. Valid keep/discard/retest with a reason and a non-invented source sets action `DECISION_RECORDED` and fills `result`. A missing, invented, or pre-comparison file stays pending.
- No Q1 decision file was written. Selftest passed locally.

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
| Estimated human min / video | 0.5 | 0.5 | OAuth secret entry remains; invalid snippet fields now fail before the token refresh |
| Automated steps | 116 | 117 | caption scope fails closed before videos.insert; no upload ran |
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
- Do not invent experiment_decision.json for Q1
- Do not treat a decision file written before COMPARED as a result
- Do not treat a collect before uploaded_at plus 7 days as COLLECTED
- Do not invent uploaded_at
- Do not drop an existing uploaded_at when an upload resumes
- Do not treat a failed caption or thumbnail as a finished upload
- Do not skip persisting upload_state.json after a post-upload failure
- Do not collect feedback in the same dispatch as execute
- Do not treat HOLD_IDEMPOTENT as the retry path for a failed caption or thumbnail
- Do not put export mtime back into the upload fingerprint
- Do not upload a second video when a provider video id already exists
- Do not silently slice tags to 12
- Do not call videos.insert with a title over 100 characters, a description over 5000, or tags over the provider limit
- Do not upload with privacy other than private
- Do not call videos.insert with only youtube.upload when captions.srt still needs force-ssl
- Do not write upload_state.json for a SCOPE_INSUFFICIENT refusal
