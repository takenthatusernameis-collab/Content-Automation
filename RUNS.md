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
