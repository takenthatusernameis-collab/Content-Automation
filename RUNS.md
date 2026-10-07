# RUNS

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.

## Run 380 — 2026-10-07T08:11:00Z
- Objective: Stop a green local selftest from shipping over-cap logs when the section is added afterward.
- Action: Added `tools/compact_all.py`. It runs the four existing compact tools and refuses a live log still over cap. Selftest calls `compact_all.py --check` and does not write. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add an exchange parser. Did not add a recovery edge. Did not dispatch the workflow.
- Result: Videos published stay 0. No live execute. Log caps stay a same-commit step, not a new upload path.
- Verification: `python3 tools/compact_all.py` then `python3 tools/selftest.py` on this commit. No provider write.
- Discovery: Run 378 passed selftest, then prepended a 13th STATE section and a 13th NEXT note. Actions run 37580716646 failed the contracts. Suspicious: oauth_idle_without_publish still stands (no publish since before Run 270), and recovery-edge stacking (Runs 368-378) did not publish. Do not add another edge for that stall.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Do not spend another run only restating that blocker.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. After a log prepend, run `python3 tools/compact_all.py` before push. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 379 — 2026-10-07T07:16:00Z
- Objective: Make Actions selftest green again after Run 378 overflowed the log caps.
- Action: Ran `state_compact.py`, `next_compact.py`, `runs_compact.py`, and `log_compact.py`. Archived the oldest sections. Did not change recovery, upload, or OAuth code. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add an exchange parser. Did not dispatch the workflow.
- Result: Live logs are back at the 12-section cap before this entry is compacted. Videos published stay 0. No live execute.
- Verification: Actions run 37580716646 failed with STATE.md 13 sections and NEXT.md 13 notes. Local compact tools printed COMPACT OK. Selftest is the verification for this commit.
- Discovery: A local SELFTEST PASS does not mean the commit stayed under the cap. Run 378 added a section and did not archive one. Suspicious: oauth_idle_without_publish still stands, and log_cap_overflow is a separate repeated risk if each run prepends without compacting.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Do not spend another run only restating that blocker. Do not add another recovery edge while this selftest was red.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. If push is rejected, run `python3 tools/persist_provider_state.py recover` and commit only the file that prints RECOVERED_RUN. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 378 — 2026-10-07T06:14:00Z
- Objective: Stop a rejected-push recovery from keeping a newer production artifact that has no provider video id.
- Action: `artifact_recovery_command` clears the download dir each run, skips a missing artifact, and skips `upload_state.json` unless `provider_video_id` is a non-empty string. Selftest refuses a break before that check. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute. Q1 media QA still PASS after materialize (verified this run, not committed).
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. `python3 tools/materialize_q1_release.py` then `python3 tools/media_qa.py` printed gate PASS. Actions not re-run. No provider write. The recover function does not call GitHub.
- Discovery: Run 377 stopped on the first production artifact. A later execute can upload state with a null video id. That file would hide an older insert and invite another videos.insert.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish (runs 366-378, no publish). Do not add another exchange parser. Do not spend another run only restating this blocker.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. If push is rejected, run `python3 tools/persist_provider_state.py recover` and commit only the file that prints RECOVERED_RUN. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 377 — 2026-10-07T05:11:00Z
- Objective: Stop a rejected-push recovery from downloading a later production run that has no video id.
- Action: `artifact_recovery_command` walks the last 20 `youtube-production.yml` runs, skips an empty run id, and downloads `provider-upload-state` into `/tmp/provider-upload-state` from the first run that has the artifact. Selftest refuses `--limit 1` and a missing empty-id guard. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write. The recover function does not call GitHub.
- Discovery: Run 376 pinned the newest production run. A later execute=false dispatch of the same workflow has no `provider-upload-state`. An empty `databaseId` also expanded to a bare download.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. If push is rejected, run `python3 tools/persist_provider_state.py recover` and commit that `upload_state.json` before another execute. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 376 — 2026-10-07T04:12:00Z
- Objective: Stop a rejected-push recovery from downloading the newest selftest run instead of the video id.
- Action: `artifact_recovery_command` now pins `youtube-production.yml` with `gh run list --workflow` before `gh run download --name provider-upload-state`. Selftest refuses a recovery command that omits that workflow. Did not poll secrets. Did not add a scanner. Did not scaffold Q2. Did not add a pre-upload checker. Did not add an exchange parser. Did not add an early-persist call. Did not dispatch the workflow.
- Result: Selftest passed. Videos published stay 0. No live execute.
- Verification: `python3 tools/selftest.py` printed SELFTEST PASS. Actions not re-run. No provider write. The recover function does not call GitHub.
- Discovery: Run 375 uploaded the artifact, then printed a bare `gh run download --name`. After the next agent commit, the newest run is selftest.yml, which has no `provider-upload-state`. That download misses the video id and invites another execute.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Suspicious: oauth_idle_without_publish. Do not add another exchange parser.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. If push is rejected, run `python3 tools/persist_provider_state.py recover` and commit that file before another execute. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

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
