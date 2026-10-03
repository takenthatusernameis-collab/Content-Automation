## 2026-10-03T22:20:00Z — Run 303

- **Objective:** Stop a slow upload from being killed before the video id is persisted, without adding an HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, BLOCKED, youtube-production.yml, youtube_api.py. OAuth secrets were not polled (Actions secret list returned 403).
- **Action taken:** Raised the production job timeout from 20 to 60 minutes. Chunk PUT timeout is now 180 seconds via `CHUNK_PUT_TIMEOUT`. Selftest refuses a 20-minute job and a retry budget that does not fit. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the timeout contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The job budget was shorter than one 600-second PUT plus retries. A timeout kill is not an HTTP status; it just never writes `upload_state.json`.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not restore the 20-minute job timeout. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-03T21:15:00Z — Run 302

- **Objective:** Stop an omitted made-for-kids flag from uploading a video that Studio then blocks, without adding an upload HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, BLOCKED, youtube_upload.py, youtube_api.py, channel.md. OAuth secrets were not polled (Actions secret list returned 403).
- **Action taken:** `docs/channel.md` records `audience_designation: not_made_for_kids`. Inspect holds when that line is missing or other. Execute raises `AUDIENCE_UNKNOWN` before the token refresh. `upload_video` no longer defaults a missing flag to false. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the audience gate and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The field was already hardcoded false on the execute path, but a missing flag was still treated as false in the transport. YouTube treats absence as unset, not as false.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not add another HTTP status variant unless a live execute returned that status. Do not change `audience_designation` unless the channel decision changes. Do not scaffold Q2.

## 2026-10-03T20:20:00Z — Run 301

- **Objective:** Stop a drafted chapter list from being dropped at videos.insert, without adding an upload HTTP status variant or polling OAuth.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, BLOCKED, youtube-production.yml, youtube_upload.py. OAuth secrets were not polled. Concurrency group already exists.
- **Action taken:** `chapter_sync_reason()` refuses a chapters.md list that is under 3 lines, does not start at 0:00, has a gap under 10 seconds, or is missing or reordered in the publish description. Inspect is HOLD_LOCAL. Execute raises METADATA_REJECTED before the token refresh. A missing chapters.md stays missing. Q1 lines already match. Extended the selftest. Did not dispatch. Did not regenerate chapters.md or publish.md.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the chapter-sync gate and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The workflow already has `concurrency: youtube-production` with cancel-in-progress false. The publish gate is still the missing OAuth secrets. Chapter drop was a silent viewer miss, not an HTTP status.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not add another HTTP status variant unless a live execute returned that status. Do not regenerate chapters.md while captions.srt is unchanged. Do not scaffold Q2.

## 2026-10-03T19:20:00Z — Run 300

- **Objective:** Turn the recurring OAuth secret stall into a non-secret setup recipe, without adding another upload HTTP status variant or re-opening closed publish boxes.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, `docs/human_session.md`, `docs/youtube_integration.md`, `tools/youtube_upload.py`. OAuth secrets were not polled.
- **Action taken:** Added `tools/oauth_setup.py`. It prints console steps, the required scopes, and `gh secret set` commands that read from the prompt. It reports missing secret names only and does not call Google. `docs/human_session.md` no longer asks to check Description edited or First comment approved. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the recipe and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The live human page still told the operator to re-check boxes Run 297 already closed. That was recurring labor, not the credential gate. The upload-status loop remains frozen.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Follow `python3 tools/oauth_setup.py`, store the three secrets, then dispatch `youtube-production.yml` with execute=true. Do not add another HTTP status variant unless a live execute returned that status. Do not re-open Description edited or First comment approved. Do not scaffold Q2.

## 2026-10-03T15:20:00Z — Run 299

- **Objective:** Disclose generated narration on the first videos.insert, without adding another upload HTTP status variant.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, youtube_upload.py, youtube_api.py, Q1 vo_origin.md. OAuth secrets were not polled.
- **Action taken:** videos.insert now sets status.containsSyntheticMedia from vo_origin.md. kind generated is true. kind human is false. An unknown kind is SYNTHETIC_DISCLOSURE_UNKNOWN before the token refresh and does not insert. Q1 is generated. Extended the selftest. Did not dispatch.
- **Result:** Local python3 tools/selftest.py printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the disclosure flag and local selftest. Actions was not re-run. No provider write. prove_locks.py still fails on the pre-existing words_contract.py placeholder check; not caused by this change.
- **Important discovery:** The upload path set selfDeclaredMadeForKids but omitted containsSyntheticMedia. Q1 narration is edge-tts, so the first private upload would have left the altered-content disclosure for a Studio click.
- **Blocker:** GitHub Actions secrets YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Add those three secrets from a token granted youtube.upload and youtube.force-ssl (or full youtube), then dispatch youtube-production.yml with execute=true. Do not drop containsSyntheticMedia. Do not invent a vo origin. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-03T14:20:00Z — Run 298

- **Objective:** Stop a rejected provider-state push from dropping the video id on the shallow Actions checkout, without adding another upload status variant.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, `youtube-production.yml`, `tools/persist_provider_state.py`. OAuth secrets were not polled.
- **Action taken:** `push_with_retry` unshallows when the clone is shallow, then fetches and rebases. A failed rebase aborts. No force-push. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the shallow retry order and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 297's retry still fails on the default checkout depth. The publish gate is still the missing OAuth secrets.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not force-push provider state. Do not rebase a shallow checkout without unshallow. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-03T12:20:00Z — Run 297

- **Objective:** Stop a successful upload from being lost when the provider-state push is rejected, without adding another upload status variant.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, `youtube-production.yml`, `next_action.py`, `hint.py`, `pipeline_status.py`. OAuth secrets were not polled.
- **Action taken:** Added `tools/persist_provider_state.py`. Upload and feedback persist now classify before commit and retry a non-fast-forward push after fetch and rebase. No force-push. Q1 board copy no longer asks to check already approved publish boxes. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the persist classifier, retry order, and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The video-id hold was only durable if `git push origin HEAD:main` succeeded on the first try. The publish gate is still the missing OAuth secrets.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not force-push provider state. Do not re-open the approved Q1 boxes. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-03T11:20:00Z — Run 296

- **Objective:** Stop the upload status-variant loop and close the unaligned resume hole that would send a chunk YouTube rejects.
- **Inspected:** STATE, NEXT, ROADMAP, HANDOFF, FAILURES, BLOCKED, `youtube_api.py`, `youtube-production.yml`. OAuth secrets were not polled.
- **Action taken:** A 308 Range that is not a multiple of 256 KiB is `RESUMABLE_STALLED` (`unaligned_offset`). The next chunk is not sent. Tiny-chunk tests stay exempt. Extended the selftest. Did not dispatch. Flagged Runs 281-295 as a suspicious loop.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the alignment guard and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** The client resumed any advancing Range. Byte 100 is not a legal non-final chunk start. More status classes would not fix that, and the publish gate is still the missing secrets.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Flagged, not re-worked as the only work.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not send an unaligned resumable chunk. Do not add another HTTP status variant unless a live execute returned that status. Do not scaffold Q2.

## 2026-10-03T10:20:00Z — Run 295

- **Objective:** Stop a finished resumable upload whose session then returns 404 or 410 from inviting a second videos.insert.
- **Inspected:** STATE, NEXT, FAILURES, `tools/youtube_api.py`, `tools/youtube_upload.py`, `youtube-production.yml`. OAuth secrets were not polled (Actions secret list is 403 for this token).
- **Action taken:** A 200/201 with no id still queries the same session once. A 404 or 410 on that query is `RESUMABLE_COMPLETED_SESSION_GONE`. Execute persists `completed_without_id` and does not invent a video id. A matching fingerprint is `HOLD_COMPLETED_WITHOUT_ID`. The workflow commits that hold. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the completed-session-gone contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 294 recovered an id only when the follow-up query returned 200/201. The documented expired-session responses after an accepted last byte were still a duplicate-insert path, and the workflow would not have committed the failure.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall since the execute path existed. Flagged, not re-worked this run.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not start a second videos.insert after `RESUMABLE_COMPLETED_SESSION_GONE`. Do not invent a provider video id. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T09:15:00Z — Run 294

- **Objective:** Stop a finished resumable upload whose 200/201 body was dropped from looking like a missing video and inviting a second videos.insert.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/selftest.py`. OAuth secrets were not polled.
- **Action taken:** A completing PUT that returns 200 or 201 with an empty or id-less body queries the same session once and returns that video id. It does not open another videos.insert. A non-200/201 query stays `RESUMABLE_MISSING_VIDEO_ID`. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the empty-completion-body contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Runs 287-293 resume 308, 5xx, 401, and post-upload artifact failures, but a 201 with an empty body still raised `RESUMABLE_MISSING_VIDEO_ID` without asking the session. That is the case where the server already has the video and the next execute would spend another insert.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not start a second videos.insert when a completion body is empty. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T08:20:00Z — Run 293

- **Objective:** Stop a 401 on caption, thumbnail, or pin-comment upload from looking permanent after the video id already exists, without a second videos.insert.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/selftest.py`. OAuth secrets were not polled.
- **Action taken:** Post-upload calls refresh the access token on 401 and retry the same artifact request. An empty or unchanged token, or three refreshes, raise `POST_UPLOAD_TOKEN_REFRESH_EXHAUSTED`. A 400 stays permanent. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the post-upload 401 contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 292 refreshed a 401 only on the resumable master. Access tokens expire in about an hour, so a long upload could finish and then fail captions with the stale token. That is not a snippet gate.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not start a second videos.insert on a post-upload 401. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T07:20:00Z — Run 292

- **Objective:** Stop a 401 on the resumable master upload from aborting the session and inviting a second videos.insert.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/selftest.py`. OAuth secrets were not polled.
- **Action taken:** A chunk PUT 401, or a session-start 401 with no Location, refreshes the access token and continues the same upload. A Location already returned is not followed by another videos.insert. Three refreshes or an empty/unchanged token raise `RESUMABLE_TOKEN_REFRESH_EXHAUSTED`. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the 401 resume contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Runs 287-291 covered 308, 5xx, missing Range, session-start 503, and post-upload artifact retries. A 401 still raised `RESUMABLE_UNEXPECTED_STATUS` and dropped the Location.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not start a second videos.insert on 401. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T06:16:00Z — Run 291

- **Objective:** Stop a transient 503 on caption, thumbnail, or pin-comment upload from forcing another workflow dispatch after the video id already exists, without another snippet gate or a second videos.insert.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `tools/youtube_api.py`, `tools/selftest.py`.
- **Action taken:** Post-upload calls retry 408/429/5xx and network errors up to three times, then raise `POST_UPLOAD_RETRY_EXHAUSTED`. A 400 stays permanent. Extended the selftest. Did not dispatch. Did not poll secrets.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the artifact-retry contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Runs 287-290 made the master resumable, but captions and thumbnails still used one multipart POST. A 503 there is POST_UPLOAD_INCOMPLETE even though the video id exists. Snippet micro-gates remain deferred.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T05:20:00Z — Run 290

- **Objective:** Stop a session-start 503 with no Location from aborting the first upload, without starting a second videos.insert when Location is already present, and without restating the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/selftest.py`, `youtube-production.yml`.
- **Action taken:** Session POST now retries 408/429/5xx and network errors only when Location is missing. A Location on a non-200 is used and not followed by another POST. Chunk 408 and 429 join the existing resume set. A status query that advances the offset clears the retry count. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the session-start contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 288 resumed a chunk PUT 503, but the session POST itself still treated 503 as `RESUMABLE_SESSION_MISSING`. That is the call that spends the insert quota unit. A 503 with no Location has nothing to resume. A 503 with Location must not be retried as a new insert.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not scaffold Q2. Do not add another snippet micro-gate. Do not invent a baseline or decision.

## 2026-10-03T04:11:00Z — Run 289

- **Objective:** Stop a 308 with no Range header from skipping bytes the server did not store.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/selftest.py`, YouTube resumable upload guide (a 308 without Range means nothing has been uploaded).
- **Action taken:** `received_offset()` returns None when Range is omitted. The upload loop restarts at byte 0, honors Retry-After up to 30 seconds, and raises `RESUMABLE_STALLED` after three missing-Range responses. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the missing-Range contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 288 queried the session after a 5xx, but a chunk 308 without Range still used `end+1` as the resume point. That would send the next chunk past bytes YouTube says it does not have.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not treat a missing Range as received. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T03:12:00Z — Run 288

- **Objective:** Stop a transient 5xx on the resumable master upload from looking like a permanent failure and inviting a second `videos.insert`.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/selftest.py`, official resumable upload guide (500/502/503/504 are resumeable).
- **Action taken:** A chunk PUT that returns 500, 502, 503, or 504, or a network error, now queries the session with `Content-Range: bytes */size` and resumes from the Range. Three failures at the same stage raise `RESUMABLE_RETRY_EXHAUSTED`. A 404 on that query is `RESUMABLE_SESSION_EXPIRED`. Captions and thumbnails stay multipart. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the 5xx resume contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 287 resumed only on HTTP 308. A 503, which the official guide says to resume, still raised `RESUMABLE_UNEXPECTED_STATUS` and left no video id, so the next execute could open a second session.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not restore multipart for the master. Do not add another snippet micro-gate. Do not scaffold Q2.

## 2026-10-03T02:11:00Z — Run 287

- **Objective:** Stop the first authenticated `videos.insert` from depending on one multipart POST of the multi-minute master.
- **Inspected:** STATE, NEXT, RUNS, `tools/youtube_api.py`, `tools/youtube_upload.py`, workflow timeout, selftest.
- **Action taken:** `upload_video` now starts a resumable session and PUTs 8 MiB chunks, continuing after HTTP 308. Captions and thumbnails stay multipart. Selftest covers Range parsing, chunk alignment, and a fake 308 resume. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the resumable contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Runs 281-286 kept adding pre-insert snippet gates while the master still used multipart. That gate loop is diminishing and should stop unless a documented provider reject is still ungated. The transport hole was the remaining first-upload failure mode that local gates cannot catch.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not restore multipart for the master. Do not scaffold Q2.

## 2026-10-03T01:20:00Z — Run 286

- **Objective:** Stop a tag list that is under a raw 500-character sum from reaching `videos.insert` when quotes and commas push it over the provider limit.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, `tools/youtube_upload.py`, `tools/selftest.py`, Q1 `publish.md` tags.
- **Action taken:** `metadata_block_reason` now uses `tag_budget()`. A space adds two quote characters. Each comma between tags counts. Selftest covers a 12-tag fixture whose raw sum is under 500 and whose budget is over 500, plus the short Q1-style spaced tags. Q1 tags were checked and still pass (budget 152).
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the local gate and selftest. Actions was not re-run. No provider write.
- **Important discovery:** The previous total counted tag characters only. Official `videos.insert` accounting wraps spaced tags in quotes and counts separators, so the old gate could pass a list the API rejects as `invalidTags`.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not scaffold Q2. Do not regenerate Q1 tags.

## 2026-10-03T00:35:00Z — Run 285

- **Objective:** Stop overlapping captions or a truncated PNG from creating a private video that then loops on post-upload failure, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, `youtube_upload.py`, `youtube_api.py`, Q1 `captions.srt`, Q1 `thumbnail.png`, selftest.
- **Action taken:** `caption_timing_reason()` now refuses a cue that starts before the previous cue ends. `png_has_iend()` refuses a PNG whose last chunk is not IEND. Inspect stays HOLD_LOCAL. Execute raises ARTIFACT_REJECTED before the token refresh. `videos.insert` sets `defaultLanguage` and `defaultAudioLanguage` to `en`, and `captions.insert` uses the same language. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Q1 captions.srt (103 cues, no overlap) and thumbnail.png (IEND present) pass. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the overlap and IEND contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 284 checked cue start order only. A later cue could start inside the previous cue and still pass READY, then fail after `videos.insert`. A PNG with a valid IHDR and no IEND had the same hole for `thumbnails.set`.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it. The refresh token must include caption scope, not only upload scope.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), plus `yt-analytics.readonly` for later collect. Then dispatch `youtube-production.yml` with execute=true. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T23:20:00Z — Run 284

- **Objective:** Stop a caption draft with bad timing, or an empty or illegal title, from creating a private video that then loops on post-upload failure, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, `youtube_upload.py`, `youtube_api.py`, Q1 `captions.srt`, selftest.
- **Action taken:** Added `caption_timing_reason()`. Present captions must have parseable forward cues in order. If the master can be probed, the last cue cannot end more than one second past it. Empty titles and titles with angle brackets fail in `metadata_block_reason()`. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Q1 captions.srt (103 cues) passes with no local master. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the timing contract and local selftest. Actions was not re-run. No provider write. Q1 master was not in the checkout, so the past-video check was verified only by the unit case.
- **Important discovery:** Run 283 accepted any file containing `-->`. A backward cue or a cue past the master would still pass READY and fail only after `videos.insert`.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it. The refresh token must include caption scope, not only upload scope.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), plus `yt-analytics.readonly` for later collect. Then dispatch `youtube-production.yml` with execute=true. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T22:13:00Z — Run 283

- **Objective:** Stop a bad thumbnail or caption draft from creating a private video that then loops on post-upload failure, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, `youtube_upload.py`, `youtube_api.py`, Q1 `captions.srt`, selftest.
- **Action taken:** Added `artifact_block_reason()` and `png_dimensions()`. Inspect treats it as a hard local check. Execute raises `ARTIFACT_REJECTED` before the token refresh. Missing thumbnail or captions stay missing. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Q1 captions.srt passes with thumbnail absent. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the artifact contract and local selftest. Actions was not re-run. No provider write. Q1 thumbnail.png was not in the checkout, so its dimensions were not remeasured this run.
- **Important discovery:** Scope and snippet checks ran before insert, but a present thumbnail over 2MB, not a PNG, or under 640px, or a caption file with no cue, would still pass READY and fail only after `videos.insert`.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it. The refresh token must include caption scope, not only upload scope.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), plus `yt-analytics.readonly` for later collect. Then dispatch `youtube-production.yml` with execute=true. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T21:13:00Z — Run 282

- **Objective:** Stop an upload-only OAuth token from creating a private video that then loops on caption failure, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, FAILURES, `youtube_upload.py`, `youtube_api.py`, `youtube-production.yml`, `docs/youtube_integration.md`, selftest.
- **Action taken:** Added `missing_provider_scopes()` and a tokeninfo scope read after refresh. Execute raises `SCOPE_INSUFFICIENT` before `videos.insert` when captions need `youtube.force-ssl` or the full `youtube` scope and the grant lacks both. A scope refusal does not write `upload_state.json`. Documented the consent scopes. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the scope contract and local selftest. Actions was not re-run. No provider write. Tokeninfo was not called.
- **Important discovery:** The documented minimum scope was `youtube.upload`. That scope can insert the video and set a thumbnail, but `captions.insert` requires `youtube.force-ssl` or `youtube`. The first authenticated dispatch would have created a video and then stayed `POST_UPLOAD_INCOMPLETE`.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it. The refresh token must include caption scope, not only upload scope.
- **Recommended next action:** Add those three secrets from a token granted `youtube.upload` and `youtube.force-ssl` (or full `youtube`), plus `yt-analytics.readonly` for later collect. Then dispatch `youtube-production.yml` with execute=true. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T20:12:00Z — Run 281

- **Objective:** Fail closed on YouTube snippet limits before the first authenticated write, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, `youtube_upload.py`, selftest, Q1 `publish.md`.
- **Action taken:** Added `metadata_block_reason()`. Inspect treats it as a hard local check. Execute refuses `METADATA_REJECTED` and `PRIVACY_NOT_PRIVATE` before the token refresh. Stopped silent `tags[:12]` truncation. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Q1 title 42 chars, 9 tags, description under 5000, block reason None. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the metadata limit contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** `request_body` and `upload_video` sliced tags to 12, so a later packet could drop tags and still look READY.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Invalid snippet fields must fail before the token refresh. A post-upload failure can be retried with the same execute input; it must not create a second video. Dispatch collect_feedback=true only after uploaded_at is at least 7 days old and not in the same dispatch as execute. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T19:15:00Z — Run 280

- **Objective:** Stop a rematerialized master from uploading a second video, and let a failed caption or thumbnail resume on the existing video id, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, `youtube_upload.py`, `youtube-production.yml`, selftest.
- **Action taken:** Fingerprint now hashes export bytes instead of mtime. `existing_upload_action()` returns resume, finished, mismatch, or none. Inspect exposes `RESUME` / `RESUME_POST_UPLOAD` for an incomplete post-upload. Execute refuses `EXISTING_VIDEO_FINGERPRINT_MISMATCH` instead of inserting another video. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the resume/idempotency contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 279 persisted the video id, then the next execute hit `HOLD_IDEMPOTENT` and returned before resume. The fingerprint also included mtime, so a later materialize of the same r253 bytes would miss that id and upload a second copy.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. A post-upload failure can be retried with the same execute input; it must not create a second video. Dispatch collect_feedback=true only after uploaded_at is at least 7 days old and not in the same dispatch as execute. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T17:20:00Z — Run 279

- **Objective:** Stop a caption or thumbnail failure from looking like a finished upload, and stop that failure from dropping the provider video id, without retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `youtube_upload.py`, `youtube-production.yml`, selftest.
- **Action taken:** Added `incomplete_post_uploads()`. Execute writes state, then raises `POST_UPLOAD_INCOMPLETE` if caption, thumbnail, or requested comment status is failed. Persist step now runs with `always()` when execute was requested. Collect is skipped when execute is also true. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the incomplete-upload contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** A failed caption previously left the execute step green, and a raised execute step skipped the persist step. Either path could lose the video id or hide a missing caption.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Dispatch collect_feedback=true only after uploaded_at is at least 7 days old and not in the same dispatch as execute. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T16:20:00Z — Run 278

- **Objective:** Stop a resumed upload from erasing the observation clock, without retrying the OAuth stall or inventing a timestamp.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `youtube_upload.py`, `youtube_feedback.py`, selftest.
- **Action taken:** Added `preserved_upload_stamp()`. Resume copies `video_upload.uploaded_at` or top-level `uploaded_at` onto the new state. A fresh upload writes the same stamp in both places. Missing prior stamp stays missing. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the stamp contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 277's window reads `uploaded_at`, but a caption or thumbnail retry rebuilt `video_upload` as `already_uploaded` and dropped the stamp. The next collect would stay `OBSERVATION_WINDOW_UNKNOWN` forever.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall. Do not spend a run only restating it.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Dispatch collect_feedback=true only after uploaded_at is at least 7 days old. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T15:20:00Z — Run 277

- **Objective:** Stop an early feedback collect from becoming COLLECTED evidence, without retrying the OAuth stall or inventing metrics.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `youtube_feedback.py`, `youtube-production.yml`, selftest.
- **Action taken:** Collect now requires `video_upload.uploaded_at` or `uploaded_at` at least 7 days old. Missing time is `OBSERVATION_WINDOW_UNKNOWN`. An earlier time is `OBSERVATION_WINDOW_NOT_DUE` and exits 5 before any provider read. `execute_feedback` repeats the check. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the window contract and local selftest. Actions was not re-run. No provider write or read.
- **Important discovery:** Run 276 could dispatch collect as soon as a video id existed. That fetch would be committed as COLLECTED and could later be compared as if the 7-day window had elapsed.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Dispatch collect_feedback=true only after uploaded_at is at least 7 days old. Do not invent uploaded_at, a Q1 baseline, or a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T14:20:00Z — Run 276

- **Objective:** Remove the post-publish manual feedback CLI without retrying the OAuth stall or inventing metrics.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `youtube-production.yml`, `youtube_feedback.py`, `oauth_preflight.py`, selftest.
- **Action taken:** Added workflow input `collect_feedback` (default false). Authenticated execute or collect runs `oauth_preflight.py` first. Collect-only skips ffmpeg and materialize, then runs `youtube_feedback.py --execute` and `experiment_loop.py --write-state`. Persist commits feedback only when gate is COLLECTED and a provider video id exists. Extended the selftest. Did not dispatch.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute and collect were not dispatched. Videos published stay 0.
- **Verification status:** completed for the workflow contract and local selftest. Actions was not re-run. No provider write or read.
- **Important discovery:** The execute path persisted upload state and stopped. Every later video would still need a human to invoke the feedback CLI even after secrets exist.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish and collect gate. Not polled. Flagged as a recurring external stall.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. After a provider video id exists, dispatch collect_feedback=true. Do not invent a Q1 baseline or decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T13:30:00Z — Run 275

- **Objective:** Record an explicit keep/discard/retest without inferring it from the delta or retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `experiment_loop.py`, `complete.py`, selftest.
- **Action taken:** Added `load_decision()` for `experiment_decision.json`. The file is ignored until a numeric comparison exists. Valid keep/discard/retest with reason and a non-rejected source sets action `DECISION_RECORDED` and copies that decision into `result`. Missing, invented, or mismatched files stay pending. Extended the selftest. Did not write a Q1 decision.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the decision contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 274 could compute a delta but left `result` null forever. `complete.py` requires that field, and there was no file contract a later run could fill without editing code.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Flagged as a recurring external stall.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not invent a Q1 baseline or decision. Do not treat COMPARED as a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T12:25:00Z — Run 274

- **Objective:** Compute a post-publish primary-metric delta without inventing a baseline, a keep/discard, or retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `experiment_loop.py`, `complete.py`, selftest.
- **Action taken:** Added `compare_primary()`. A documented baseline plus one numeric collected value sets action `COMPARED` and fills `comparison` (observed, baseline, delta, direction). Decision stays `pending` and `result` stays null. Missing or conflicting metrics are `COMPARE_BLOCKED_METRIC`. `complete.py` now requires decision keep/discard/retest before COMPLETE.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0. No Q1 baseline was written.
- **Verification status:** completed for the comparison contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Run 273 stopped at COMPARE_READY even when the collected row already contained the primary metric. The next run would have had to hand-compute the delta.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Flagged as a recurring external stall.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not invent a Q1 baseline. Do not treat COMPARED as a decision. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T11:17:00Z — Run 273

- **Objective:** Unlock post-publish comparison without inventing a baseline or retrying the OAuth stall.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, PROGRESS, `experiment_loop.py`, `complete.py`, production workflow, selftest.
- **Action taken:** Added `load_baseline()` for `experiment_baseline.json`. Rejected missing fields, disallowed changes, and sources named invented/assumed/placeholder/guess. A valid file sets action `COMPARE_READY` and leaves decision `pending`. Extended the selftest. Did not write a Q1 baseline.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the baseline contract and local selftest. Actions was not re-run. No provider write.
- **Important discovery:** Runs 266-272 kept meeting the same secret boundary. Further restatement does not move publish. The next unblocked contract was the comparison schema, not another preflight.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` remain the publish gate. Not polled. Flagged as a recurring external stall.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not invent a Q1 baseline. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T10:15:00Z — Run 272

- **Objective:** Stop an execute dispatch from downloading Q1 media when the three OAuth secrets are still empty, without polling secrets or retrying upload.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `youtube-production.yml`, `youtube_upload.py`, `youtube_feedback.py`.
- **Action taken:** Added `tools/oauth_preflight.py` (names and presence only). Wired it as the first step after checkout when execute=true, before Python setup, ffmpeg, and materialize. Extended the selftest for empty, blank, and present values, and for step order.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Execute was not dispatched. Videos published stay 0.
- **Verification status:** completed for the preflight and selftest. Workflow order is unverified on Actions because execute was not dispatched. Dry-run path was not re-run.
- **Important discovery:** The previous execute step only failed after materialize. A mistaken execute=true dispatch would spend the release download before reporting missing secrets.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` are still unset. Not polled this run.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. The preflight should pass before materialize. Do not re-encode. Do not scaffold Q2.

## 2026-10-02T09:15:00Z — Run 271

- **Objective:** Stop the post-upload loop from treating a real feedback fetch as no evidence, without retrying the OAuth boundary.
- **Inspected:** STATE, NEXT, RUNS, BLOCKED, ROADMAP, `youtube_feedback.py`, `experiment_loop.py`, `complete.py`, production workflow.
- **Action taken:** Added `collected_metrics()` which accepts only `gate=COLLECTED`, `attempted_fetch=true`, a non-empty metric row list, and a video id matching `upload_state.json`. Experiment and complete gates now use that helper. Extended the selftest for mismatch and matching collected rows.
- **Result:** Local `python3 tools/selftest.py` printed SELFTEST PASS. Experiment with matching collected metrics is READY_TO_COMPARE and COMPARE_BLOCKED_NO_BASELINE. Result stays pending. Videos published stay 0.
- **Verification status:** completed. Local selftest passed, then Actions run 36988824728 succeeded on `613e8ee439ccf16e4ce8c5aaf4855fe30aa523dd`. No provider write.
- **Important discovery:** `inspect_feedback()` always sets metrics to None. Both learning gates used that field, so a later `feedback_state.json` would never advance the experiment or completion gates.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` are still unset. Secret list API returned 403 for this token. Do not poll.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not scaffold Q2. Do not invent a keep/discard from collected metrics.

## 2026-10-02T08:18:05Z — Run 270

- **Objective:** Prove the Run 269 production workflow instead of restating the OAuth hold.
- **Inspected:** STATE, NEXT, HANDOFF, RUNS, `youtube-production.yml`, `materialize_q1_release.py`.
- **Action taken:** Dispatched workflow_dispatch with execute=false. Run 36982959831 failed because materialize aborted when the expected truncated r249 master was present. Changed the guard to ignore that known sha, refuse an unexpected r249 master sha, and still refuse installing the banned sha as `export/master.mp4`. Pushed `9416aae2c482ca08fd55642e0fff94568482ee51` and redispatched.
- **Result:** Run 36983196381 succeeded. Materialize logged `ignored known-truncated r249 q1-master.mp4; installing r253 master only`, then 7 cards and `export/master.mp4`. Dry-run gate `YOUTUBE_AUTH_REQUIRED`, action `DRY_RUN`, export present, publish copy approved, captions 103 cues uploaded=false, thumbnail present uploaded=false. OAuth env vars were empty. Execute and state-persist steps skipped. Videos published stay 0.
- **Verification status:** Actions job 110762207440 conclusion success. Prior job 110761451601 conclusion failure, used as the regression evidence. No provider write claimed.
- **Important discovery:** The production path was blocked by a local guard, not by OAuth. Treating presence of the banned release asset as fatal prevented the r253 install.
- **Blocker:** GitHub Actions secrets `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` are unset.
- **Recommended next action:** Add those three secrets, then dispatch `youtube-production.yml` with execute=true. Do not re-encode. Do not scaffold Q2. Do not restore the presence-only abort.

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.
Earlier runs through Run 269 remain in git at `9416aae2c482ca08fd55642e0fff94568482ee51` (`RUNS.md` blob `243e47753b76bbd636a59dddb00e8c1c6f2e90c1`) and before that at `65cca063`.
