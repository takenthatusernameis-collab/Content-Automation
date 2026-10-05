# RUNS

Older runs live in `docs/runs_archive.md`. Do not paste the archive back. `tools/runs_compact.py` moves extras. It does not delete history.

## Run 346 — 2026-10-05T20:15:00Z
- Objective: Stop a committed dead-session hold from bricking the first upload after Studio shows no video.
- Action: Added a local release that clears `session_expired_hold` only with studio token `no_video_in_studio`, no provider video id, and no remaining Location. Persist commits that release. The production workflow does not pass the flag. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a YouTubeAPIError reason.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 345 fail-closed on 404/410, but nothing could clear the hold, so the first expired session would block every later execute even after a human checked Studio.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Eight-plus runs of upload-edge fixes have not published; that idle is the known credential stall, not a missing scanner.
- Next: Do not pass the release flag from Actions. Do not release without the Studio token. Do not start a second videos.insert when Location exists or when session_expired_hold is set. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 345 — 2026-10-05T19:20:00Z
- Objective: Stop a dead resumable Location from being reused forever or turning into a second videos.insert.
- Action: Probe a saved session URI before any chunk. A 404 or 410 drops the URI, sets session_expired_hold, and commits that hold. The next execute raises RESUMABLE_SESSION_EXPIRED and does not POST videos.insert. Did not add a reason. Did not poll secrets. Did not add a scanner. Did not scaffold Q2.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 344 committed the Location, but an expired session was skip_transient, so the dead URI stayed the next execute target.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not start a second videos.insert when Location exists or when session_expired_hold is set. Do not print the URI. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 344 — 2026-10-05T18:20:00Z
- Objective: Stop a killed execute from starting a second videos.insert after Location exists.
- Action: Saved the resumable session URI into upload_state.json and committed that row. The next execute resumes that URI and does not POST videos.insert. Fingerprint mismatch reuses the existing mismatch reason. Did not poll secrets. Did not add a scanner. Did not scaffold Q2.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Runs 340-343 only compacted fetch files. The open Location was still not durable, so the first real upload could duplicate if the runner died after the session POST.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not print the session URI. Do not start a second videos.insert when Location exists. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 343 — 2026-10-05T17:25:00Z
- Objective: Stop PROGRESS.md and FAILURES.md from truncating before the newest lesson on the next agent fetch.
- Action: Moved sections older than the newest 12 to docs/progress_archive.md and docs/failures_archive.md. Added tools/log_compact.py and a contract. Selftest runs the contract. Did not poll secrets. Did not add a scanner. Did not scaffold Q2.
- Result: Both live files are 12 sections. Archives hold the older notes. Videos published stay 0.
- Verification: log_compact_contract printed LOG COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: PROGRESS.md was 27269 bytes and FAILURES.md was 30708 bytes. NEXT.md truncated near 28KB, so both were already past the known fetch cut.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not paste the archives back. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 342 — 2026-10-05T17:15:00Z
- Objective: Stop RUNS.md from truncating before the newest run log on the next agent fetch.
- Action: Moved entries older than the newest 12 from RUNS.md to docs/runs_archive.md. Added tools/runs_compact.py and a contract. Selftest runs the contract. Did not poll secrets. Did not add a scanner. Did not scaffold Q2.
- Result: RUNS.md keeps 12 entries plus the permanent footer. Archive holds the older entries, including Run 270. Videos published stay 0.
- Verification: runs_compact_contract printed RUNS COMPACT CONTRACT PASS. python3 tools/selftest.py printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: RUNS.md was 108696 bytes and 71 entries. The agent fetch cut the newest section before the recommended next action.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not paste the archive back into RUNS.md. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 341 — 2026-10-05T16:20:00Z
- Objective: Stop NEXT.md from truncating before the older do-not-rediscover locks on the next agent fetch.
- Action: Moved notes older than the newest 12 from NEXT.md to docs/next_archive.md. Added tools/next_compact.py and a contract. Selftest runs the contract. Left an active-lock line for the OAuth stall, Q2, materialize, and resumable upload.
- Result: NEXT.md is 12 notes. Archive holds the older notes, including the materialize abort and multipart refusal. Videos published stay 0.
- Verification: next_compact_contract printed NEXT COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: NEXT.md was 28596 bytes. The agent fetch kept the newest notes and cut the upload locks that still prevent a second videos.insert.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not paste the archive back into NEXT.md. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 340 — 2026-10-05T15:20:00Z
- Objective: Stop STATE.md from truncating before the current gate on the next agent fetch.
- Action: Moved deltas older than the newest 12 from STATE.md to docs/state_archive.md. Added tools/state_compact.py and a contract. Selftest runs the contract.
- Result: STATE.md is 12 run sections. Archive holds the older sections. stall_watch still prints STALL_OAUTH_IDLE. Videos published stay 0.
- Verification: state_compact_contract printed STATE COMPACT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: STATE.md was 52418 bytes and 67 run sections. The agent fetch truncated it before the publish-gate section.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Do not paste the archive back into STATE.md. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 339 — 2026-10-05T14:20:00Z
- Objective: Stop the production stall printer from treating `No new scanner` as another local-gate run.
- Action: Removed the bare `scanner` token from `tools/stall_watch.py` and scrub negation phrases before the local-gate match. Contract covers three boilerplate deltas. Real scan tokens still set `STALL_LOCAL_GATE`.
- Result: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. Current STATE prints `STALL_OAUTH_IDLE` only. `python3 tools/selftest.py` printed SELFTEST PASS. Videos published stay 0.
- Verification: completed locally. Actions not re-run. No provider write.
- Discovery: Runs 336-338 said `No new scanner` and that sentence kept `STALL_LOCAL_GATE` set, so later runs were told not to add a scanner they were not adding.
- Blocker: YouTube OAuth secrets still absent. Playlist id still `not_set`.
- Next: Do not restore the bare scanner token. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

## Run 338 — 2026-10-05T12:30:00Z
- Objective: Stop the production persist step from committing a COLLECTED analytics file that is not the first-calendar-days stamp.
- Action: `feedback_commit_decision` returns `skip_unstamped_window` when kind is missing or `sliding_now`, days are not 7, or start/end dates are absent. A stamped file still returns `commit_collected`. Selftest locks both. Workflow summary states the commit rule. Date match against `uploaded_at` stays in `collected_metrics`.
- Result: `python3 tools/selftest.py` printed SELFTEST PASS. No Analytics call. Videos published stay 0.
- Verification: completed locally. Actions not re-run. No provider write.
- Discovery: Run 337 closed the comparison path only. The workflow still committed any COLLECTED file with a video id, so a sliding or unstamped file could become the durable evidence.
- Blocker: YouTube OAuth secrets still absent. Playlist id still `not_set`.
- Next: Do not commit an unstamped collected file. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

## Run 337 — 2026-10-05T11:20:00Z
- Objective: Stop a collected analytics file from counting as the first 7 days unless its window is that video's calendar range.
- Action: `collected_window_ok` refuses a missing kind, `sliding_now`, or dates that do not match `analytics_range`. `execute_feedback` stamps `kind: first_calendar_days` and queries `DEFAULT_WINDOW_DAYS` from `uploaded_at`. Selftest covers a sliding file and a matching file. Experiment fixture now includes the matching window.
- Result: `python3 tools/selftest.py` printed SELFTEST PASS. No Analytics call. Videos published stay 0.
- Verification: completed locally. Actions not re-run. No provider write.
- Discovery: Run 336 aligned the dry-run plan, but a COLLECTED file without kind still passed into experiment comparison.
- Blocker: YouTube OAuth secrets still absent. Playlist id still `not_set`.
- Next: Do not treat an unstamped collected file as the 7-day observation. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

## Run 336 — 2026-10-05T10:20:00Z
- Objective: Make the dry-run analytics plan use the same first-7-day dates the live fetch already uses.
- Action: `video_window()` fills `inspect_feedback` window from `analytics_range` when `uploaded_at` exists. Missing upload time leaves query dates empty. `request_plan` reads those dates. Selftest fails if a ready plan is not the upload date through upload plus 6 days.
- Result: `python3 tools/selftest.py` printed SELFTEST PASS. No Analytics call. Videos published stay 0.
- Verification: completed locally. Actions not re-run. No provider write.
- Discovery: Run 335 fixed the due gate and the execute query, but the plan an operator would copy still showed a sliding now window.
- Blocker: YouTube OAuth secrets still absent. Playlist id still `not_set`.
- Next: Do not restore the sliding query range. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

## Run 335 — 2026-10-05T09:11:00Z
- Objective: Stop the first analytics collect from treating a short, lag-cut window as the 7-day observation.
- Action: `window_status` due time is upload plus 7 days plus `DATA_LAG_DAYS` (3). `analytics_range` is the first 7 calendar days of that video. Selftest expects day 8 to stay not due and day 11 to be READY offline. Workflow summary and `docs/feedback_loop.md` say the same.
- Result: Local `check_feedback_fail_closed` returned no failures. No Analytics call. Videos published stay 0.
- Verification: completed for the window math and the existing feedback selftest helper. Full `selftest.py` not re-run. Actions not re-run.
- Discovery: The old due gate and the query end date disagreed, so the first experiment could be collected before the claimed window existed.
- Blocker: YouTube OAuth secrets still absent. Playlist id still `not_set`.
- Next: Do not rediscover this lag. Do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets.

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.
Earlier runs through Run 269 remain in git at `9416aae2c482ca08fd55642e0fff94568482ee51` (`RUNS.md` blob `243e47753b76bbd636a59dddb00e8c1c6f2e90c1`) and before that at `65cca063`.
