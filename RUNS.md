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
