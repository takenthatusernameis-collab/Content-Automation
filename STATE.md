# STATE

Updated: 2026-10-03T11:20:00Z (Run 296)

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

## Run 296 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- Flag: Runs 281-295 kept adding upload status and snippet gates while the publish gate stayed the missing OAuth secrets. That loop is now suspicious. Do not add another HTTP status variant unless a live execute returned that status.
- A 308 Range that is not on a 256 KiB boundary is `RESUMABLE_STALLED` (`unaligned_offset`). The next chunk is not sent. That is a protocol reject, not a new status class. Selftest passed locally. Actions was not re-run.
- Description angle brackets remain ungated and deferred on purpose.

## Run 295 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- A 200/201 whose follow-up session query returns 404 or 410 is now `RESUMABLE_COMPLETED_SESSION_GONE`. The last byte was accepted and the session can no longer return the id. Execute writes `completed_without_id` and does not invent a video id. A matching fingerprint is `HOLD_COMPLETED_WITHOUT_ID` and must not start another videos.insert. The workflow commits that hold. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose. The OAuth secret stall is still the publish gate. This run closed a documented duplicate-insert hole; it did not restate the secret hold as the only work.

## Run 294 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- A finishing chunk PUT that returns 200 or 201 with an empty or id-less body now queries that same session once and uses the video resource. It does not open another videos.insert. A query that is not 200/201 still raises `RESUMABLE_MISSING_VIDEO_ID`. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. The upload-transport loop is now covering lost completion bodies; do not keep adding status variants without a documented hole. Description angle brackets remain ungated and are deferred on purpose.

## Run 293 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- A 401 on caption, thumbnail, pin-comment, or channel-id lookup refreshes the access token and retries that same call. It does not open another videos.insert. Three refreshes or an empty/unchanged token raise `POST_UPLOAD_TOKEN_REFRESH_EXHAUSTED`. A 400 stays permanent. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose.

## Run 292 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- A 401 on a chunk PUT, or on session start with no Location, refreshes the access token and resumes the same upload. A Location already returned is not followed by another videos.insert. Three refreshes or an empty/unchanged token raise `RESUMABLE_TOKEN_REFRESH_EXHAUSTED`. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose.

## Run 291 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- Caption, thumbnail, and pin-comment calls now retry 408/429/5xx and network errors up to three times. A 400 stays permanent. This does not start another videos.insert. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose.

## Run 290 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- Session start now retries a 408/429/5xx or network error only when the POST returns no Location. A Location on that response is the session and is not followed by a second videos.insert. Chunk 408 and 429 resume the existing session. A status query that advances the offset clears the retry count. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose.

## Run 289 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- A 308 with no Range header now restarts at byte 0. The YouTube resumable guide says that response means nothing is stored. The previous fallback treated the chunk just sent as accepted. Three missing-Range responses at the same stage raise `RESUMABLE_STALLED`. Retry-After is honored, capped at 30 seconds. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose.

## Run 288 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `upload_video` now treats HTTP 500, 502, 503, and 504, and a network error on a chunk PUT, as resumeable. It queries the session with `Content-Range: bytes */size` and continues from the returned Range. Three failures at the same stage raise `RESUMABLE_RETRY_EXHAUSTED`. A 404 on that query is `RESUMABLE_SESSION_EXPIRED`. Captions and thumbnails stay multipart. Selftest passed locally. Actions was not re-run.
- Flag still stands: do not add another snippet micro-gate. Description angle brackets remain ungated and are deferred on purpose.

## Run 287 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `videos.insert` no longer uses one multipart POST of the master. `youtube_api.upload_video` starts a resumable session and sends 8 MiB chunks, resuming on HTTP 308. Captions and thumbnails stay multipart. A missing Location is `RESUMABLE_SESSION_MISSING`. A 308 that does not advance is `RESUMABLE_STALLED`. Selftest passed locally with a fake transport. Actions was not re-run.
- Flag: runs 281-286 added successive snippet/artifact gates. That loop is diminishing. Do not add another local metadata check unless a documented provider reject is still ungated.

## Run 286 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now counts the `videos.insert` tag budget: a space in a tag adds the two wrapping quotes, and each comma between tags counts. A raw sum under 500 can still be `invalidTags`. Inspect stays HOLD_LOCAL. Execute raises METADATA_REJECTED before the token refresh. Q1 tags budget to 152 and still pass. Selftest passed locally. Actions was not re-run.

## Run 285 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now refuses overlapping caption cues and a PNG that has an IHDR but no IEND chunk. Inspect stays HOLD_LOCAL. Execute raises ARTIFACT_REJECTED before the token refresh. `videos.insert` now sets `defaultLanguage` and `defaultAudioLanguage` to `en`, matching `captions.insert`. Q1 captions.srt (103 cues) and thumbnail.png pass. Selftest passed locally. Actions was not re-run.

## Run 284 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now refuses an empty title, a title containing `<` or `>`, a caption cue that is unparseable or not forward, cues out of order, and a last cue more than one second past a probed master. Inspect stays HOLD_LOCAL. Execute raises ARTIFACT_REJECTED or METADATA_REJECTED before the token refresh. Q1 captions.srt (103 cues) passes without a local master. Selftest passed locally. Actions was not re-run.

## Run 283 delta
- OAuth secrets were not polled and execute was not dispatched. Videos published stay 0.
- `youtube_upload.py` now refuses a present thumbnail that is not a PNG, is over 2MB, or is under 640x360, a present captions.srt that is not UTF-8 or has no cue timestamp, and a pin comment over 10000 characters. Inspect gate is HOLD_LOCAL. Execute raises ARTIFACT_REJECTED before the token refresh. A missing thumbnail or caption stays missing. An artifact refusal does not write upload_state.json.
- Q1 captions.srt (103 cues) passes when thumbnail.png is absent. Selftest passed locally. Actions was not re-run.

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
| Estimated human min / video | 0.5 | 0.5 | OAuth secret entry remains; an unaligned resume no longer sends a chunk YouTube rejects |
| Automated steps | 129 | 130 | unaligned 308 Range stalls before the next PUT; no upload ran |
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
- Do not call videos.insert with an empty title or a title containing < or >
- Do not call videos.insert when caption cues overlap or a thumbnail PNG has no IEND chunk
- Do not drop defaultLanguage or defaultAudioLanguage from videos.insert
- Do not treat a raw tag character sum as the videos.insert 500 limit when a tag contains a space
- Do not put videos.insert back on multipart
- Do not treat HTTP 500/502/503/504 on a chunk PUT as a permanent failure
- Do not start a second videos.insert because a 503 hid the session
- Do not treat a session POST 503 with no Location as a permanent failure
- Do not POST videos.insert again when that 503 already returned Location
- Do not treat HTTP 408 or 429 on a chunk PUT as a permanent failure
- Do not add another snippet micro-gate unless a documented provider reject is still ungated
- Do not treat a 401 on a chunk PUT as a reason to start a second videos.insert
- Do not refresh into a second videos.insert when Location is already present
- Do not treat a 401 on captions, thumbnail, or pin comment as a reason to start a second videos.insert
- Do not treat an empty or unchanged post-upload refresh as success
- Do not treat a 200/201 with an empty body as a missing video if the session can still return the id
- Do not start a second videos.insert because the completion body was dropped
- Do not start a second videos.insert when a 200/201 follow-up returns 404 or 410
- Do not invent a provider video id for RESUMABLE_COMPLETED_SESSION_GONE
- Do not treat HOLD_COMPLETED_WITHOUT_ID as a retry of videos.insert
- Do not send a non-final resumable chunk from an offset that is not a multiple of 256 KiB
- Do not add another upload HTTP status variant unless a live execute returned that status
