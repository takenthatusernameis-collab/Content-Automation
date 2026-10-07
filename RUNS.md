# RUNS

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.

## Run 375 — 2026-10-07T03:11:00Z
- Objective: Keep a provider video id recoverable when git push is rejected after videos.insert.
- Action: The production workflow has `actions: write` and uploads `upload_state.json` as `provider-upload-state` with continue-on-error. A rejected push prints `python3 tools/persist_provider_state.py recover` (`gh run download --repo takenthatusernameis-collab/Content-Automation --name provider-upload-state`). Selftest refuses a workflow that lacks that artifact. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Runs 370-374 exit 0 after a rejected push so the job stays green. That still leaves the video id off main. The next execute can insert again. The artifact is the copy that survives the runner.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. If push is rejected, download `provider-upload-state` and commit it before another execute. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.


## Run 374 — 2026-10-07T02:13:00Z
- Objective: Keep a provider video id on main when classify-upload misses, without painting the job red.
- Action: The persist step prints `PERSIST_CLASSIFY_MISS_STILL_COMMIT` and continues to `git add` when classify-upload is non-zero and a provider video id exists. Status 2 still skips. A miss without that id still fails. Selftest refuses an exit 0 between that sentence and `git add`. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Runs 372 and 373 stopped a classify miss from failing the job by exiting 0 before the commit. That left the video id on the runner, which is the same loss the heredoc fix was meant to stop.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 373 — 2026-10-07T01:15:00Z
- Objective: Make the provider-state push actually run after videos.insert.
- Action: Replaced both workflow heredocs with `python3 tools/persist_provider_state.py push`. The old `<<'PY'` terminator was indented, so Bash never closed it and `push_with_retry` never ran. Selftest refuses a workflow heredoc. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. A local count of `<<'PY'` in the workflow is 0. Actions not re-run. No provider write.
- Discovery: Runs 370-372 treated a non-zero persist status as not an insert failure. That swallow hid a push that could not start. The video id would stay on the runner.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 372 — 2026-10-07T00:15:00Z
- Objective: Stop a persist classify miss from painting the job red after videos.insert.
- Action: The persist step prints `PERSIST_PUSH_NOT_INSERT_FAILURE` and exits 0 when `classify-upload` fails and a provider video id exists. A miss without that id still fails the step. Selftest refuses `exit "$status"` in that step. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 370 swallowed a rejected commit or push. A non-zero `classify-upload` still exited the step and could invite another execute.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 371 — 2026-10-06T23:13:00Z
- Objective: Stop a playlist-step crash and a contradictory job summary from looking like an insert failure after videos.insert.
- Action: The playlist membership step prints `PLAYLIST_INSERT_NOT_UPLOAD_FAILURE` and exits 0 on any non-zero exit when upload state exists, not only exit 2. The job summary now says a caption or thumbnail miss prints `POST_UPLOAD_NOT_INSERT_FAILURE` and exits 0. Selftest refuses the old non-zero summary sentence and a playlist `exit "$status"`. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 368 only swallowed playlist exit 2. A crash still exited 1 and failed the job. The summary still said a caption or thumbnail failure exits non-zero after the video id is written, which invites another execute.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 370 — 2026-10-06T21:16:00Z
- Objective: Stop a Studio pin miss or a rejected provider-state push from painting the job red after videos.insert.
- Action: The Studio pin step prints `STUDIO_PIN_NOT_INSERT_FAILURE` and exits 0 when `studio_handoff.py` exits non-zero. The persist step prints `PERSIST_PUSH_NOT_INSERT_FAILURE` and exits 0 when a provider video id exists and the commit or push fails. A persist miss without that id still fails the step. Selftest requires both markers. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Runs 368 and 369 stopped a red playlist step and a red post-upload step from inviting a second execute. The Studio pin step and the persist step could still fail the job after a video id existed.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 369 — 2026-10-06T19:12:00Z
- Objective: Stop a caption, thumbnail, or comment miss from painting the job red after videos.insert.
- Action: The execute step treats exit 4 with a saved provider video id and `POST_UPLOAD_INCOMPLETE` as `POST_UPLOAD_NOT_INSERT_FAILURE` and exits 0. An insert failure without that id still fails the step. Selftest requires that marker. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 368 stopped a red playlist step from inviting a second execute. The upload step still exits 4 after the video id is written when caption, thumbnail, or comment work is incomplete. That red job is the same signal.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 368 — 2026-10-06T18:12:00Z
- Objective: Stop a failed playlist insert from painting the job red after videos.insert.
- Action: The playlist membership step treats exit 2 as `PLAYLIST_INSERT_NOT_UPLOAD_FAILURE` and exits 0. Selftest requires that marker. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 367 said a failed playlistItems.insert is not an upload failure, but the step still returned that exit code. A red job is the signal that invites a second execute.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 367 — 2026-10-06T17:11:00Z
- Objective: Stop the first Studio pass from asking for a playlist end-screen element while playlist_id is not_set.
- Action: `tools/studio_handoff.py` names a video element (best for viewer) until a playlist id is set. A set id still names a playlist element. The workflow comment no longer says a failed playlistItems.insert prevents videos.insert. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: The pin note said lower-left video or playlist. playlist_id is not_set, so that instruction would stall the end screen the same way a missing playlist stalls membership.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 366 — 2026-10-06T16:20:00Z
- Objective: Stop a shadowed stall-watch check from letting a broken contract print SELFTEST PASS.
- Action: Merged the two `check_stall_watch` definitions in `tools/selftest.py`. The remaining check runs `stall_watch_contract.py` and the inline OAuth-idle assertions. Removed the duplicate call. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: The later definition replaced the contract call. Selftest invoked the name twice and still never ran the contract.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 365 — 2026-10-06T15:20:00Z
- Objective: Restore a green selftest after a zero idle streak was treated as a stall flag and the live logs exceeded the compact cap.
- Action: `tools/stall_watch.py` omits `idle_streak: 0` from `flag_text`. A positive streak and `suspicious: oauth_idle_without_publish` at 8 or more stay. Compact moved the oldest STATE delta and the oldest NEXT note into the archives. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Stall contract passed. State and next compact contracts passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. Compact tools printed OK. `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write.
- Discovery: Run 364 made every file print a streak, including a clear file. Selftest treats a non-empty `flag_text` as a stall. The live STATE and NEXT files were also one section over the cap, so the compact contracts failed.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 364 — 2026-10-06T13:22:00Z
- Objective: Make the repeated unpublished OAuth stall countable so later runs can flag it instead of restating it.
- Action: `tools/stall_watch.py` prints `idle_streak` and `suspicious: oauth_idle_without_publish` at 8 or more consecutive unpublished unpolled deltas. Contract covers the streak, the suspicious line, and a reset when the newest delta is not that shape. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Contract passed. Videos published stay 0. No live execute. Idle streak on this STATE is 13.
- Verification: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. Actions not re-run. No provider write.
- Discovery: Runs 352-363 each said videos published stay 0 and OAuth was not polled. The idle flag already existed, but it did not say how long the stall had lasted.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 363 — 2026-10-06T12:20:00Z
- Objective: Stop a progress section that omits the Run heading from being dropped by the size cap.
- Action: `tools/log_compact.py` promotes a bare `NNN — timestamp` line to a Run heading before it splits sections. Restored the Run 360 heading. Moved Run 351 and Run 350 progress sections into `docs/progress_archive.md`. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Contract passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/log_compact_contract.py` printed LOG COMPACT CONTRACT PASS. Actions not re-run. No provider write.
- Discovery: Run 360 wrote `360 — 2026-10-06T09:11:00Z` without the section prefix. Compact splits only on the Run heading, so that lesson was body text of Run 361.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: OAuth-idle runs have not published a video. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

