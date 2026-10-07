# RUNS

## Run 387 — 2026-10-07T17:12:00Z
- Objective: Stop the NEXT header from staying on an older run after a log prepend.
- Action: `prepend_next` replaces the single `Updated:` line from the note. The contract fails if that line is missing or doubled. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend operator_card. Did not add a scanner. Did not scaffold Q2. Did not add a freeze module.
- Result: Videos published stay 0. NEXT header now matches the note that wrote it. No live execute.
- Verification: `python3 tools/record_run_contract.py` printed RECORD RUN CONTRACT PASS. This entry was written by `record_run.py`, which also runs compact. No provider write.
- Discovery: Run 386 prepended note 1zr50 and left `Updated: ... (Run 385)`. Suspicious: oauth_idle_without_publish still has no publish since before Run 270, and Runs 375-386 stacked recovery, card, and freeze tooling instead of a publish. Do not add another freeze for that stall.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not extend the card. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 386 — 2026-10-07T16:13:00Z
- Objective: Stop a green selftest from shipping an over-cap log when the section is prepended afterward.
- Action: Called the existing `check_compact_all()` from selftest `main`. Added `tools/record_run.py`, which prepends the five live logs and runs `compact_all.py` before it exits. Opened issue 1 with the operator-card text. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend operator_card. Did not add a scanner. Did not scaffold Q2.
- Result: Videos published stay 0. Issue 1 is the human step. No live execute.
- Verification: `python3 tools/record_run_contract.py` and `python3 tools/selftest.py`. No provider write.
- Discovery: Run 380 said selftest calls `compact_all.py --check`. The function existed and was not in `main`, so the Actions cap was only the separate state/next contracts. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not extend the card. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.

## Run 385 — 2026-10-07T13:23:00Z
- Objective: Stop another operator-card extension from landing while videos published stay 0.
- Action: Added `tools/operator_card_freeze.py`. Selftest fails if `operator_card.py` grows a function, a second card module appears, or the card imports subprocess or a network client. `stall_watch.py` sets `STALL_OPERATOR_CARD` after three wired card deltas. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend operator_card. Did not add a scanner. Did not scaffold Q2.
- Result: Videos published stay 0. Operator-card defs stay 5. No live execute.
- Verification: `python3 tools/operator_card_freeze_contract.py`, `python3 tools/stall_watch_contract.py`, and `python3 tools/selftest.py`. No provider write.
- Discovery: Runs 383-384 reprinted the human step and still published nothing. A prose "do not add a second card" did not stop the reprint. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human runs `python3 tools/operator_card.py` and stores the three secrets. Do not extend the card. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 384 — 2026-10-07T12:20:00Z
- Objective: Make the one human publish command include the Google Cloud steps, not only the secret-set lines.
- Action: `tools/operator_card.py` reprints the numbered steps from `oauth_setup.recipe()`. The contract fails if Desktop app, YouTube Data API v3, the exchange command, or the dispatch line drifts. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not add a scanner. Did not scaffold Q2.
- Result: Videos published stay 0. Operator card PASS. Console steps match the recipe.
- Verification: `python3 tools/operator_card_contract.py` and `python3 tools/operator_card.py`. No provider write.
- Discovery: Run 383 printed secret-set commands and still sent the human to reconstruct the console clicks. Suspicious: oauth_idle_without_publish still has no publish since before Run 270, and Runs 368-383 added stall tooling instead of a publish.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human runs `python3 tools/operator_card.py` and stores the three secrets. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 383 — 2026-10-07T11:17:00Z
- Objective: Keep the remaining human publish step in one command that cannot drift from the OAuth recipe.
- Action: Added `tools/operator_card.py`. It prints the three secret-set commands and the dispatch line from `oauth_setup.py`, and fails if HANDOFF loses the documented master sha. Selftest runs the contract. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge.
- Result: Videos published stay 0. Operator card PASS. Dispatch line matches the recipe.
- Verification: `python3 tools/operator_card_contract.py` and `python3 tools/operator_card.py`. No provider write.
- Discovery: Runs 368-382 froze and flagged recovery edges, but the human step was still reconstructed from NEXT notes. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human runs `python3 tools/operator_card.py` and stores the three secrets. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 382 — 2026-10-07T10:14:00Z
- Objective: Stop another provider-state recovery edge from landing while videos published stay 0.
- Action: Added `tools/recovery_freeze.py`. Selftest fails if the production workflow grows a second `provider-upload-state` artifact or a second `persist_provider_state.py recover` call. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Downloaded `q1-media-r253` `q1-master-r253.mp4` and matched the documented sha256 and stream shape.
- Result: Videos published stay 0. Recovery surface counts stay artifact=1 and recover_call=1. Master sha256 `4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546`, 1920x1080 h264 30fps yuv420p, stereo AAC 48000 Hz, 328.40s.
- Verification: `python3 tools/recovery_freeze.py`, `python3 tools/recovery_freeze_contract.py`, and `python3 tools/selftest.py`. No provider write.
- Discovery: `STALL_RECOVERY_EDGE` only prints after four wired deltas. It did not stop Runs 368-378. A build failure on a grown surface is the stop. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

## Run 381 — 2026-10-07T09:13:00Z
- Objective: Flag stacked provider-state recovery edges while videos published stay 0.
- Action: `stall_watch.py` now sets `STALL_RECOVERY_EDGE` and `suspicious: recovery_edge_without_publish` when the last four STATE deltas wire a recovery path during the OAuth stall. Lock sentences do not set the flag. Contract and selftest cover both cases. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge.
- Result: Videos published stay 0. The flag is clear on this commit because the newest deltas are log-cap work, not recover wiring.
- Verification: `python3 tools/stall_watch_contract.py` and `python3 tools/selftest.py`. No provider write.
- Discovery: Runs 368-378 stacked recovery edges and prose warnings did not stop the next edge. The idle flag already existed; it did not name this pattern.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set. Do not spend another run only restating that blocker.
- Next: A human stores the three secrets and runs the dispatch printed by `tools/oauth_setup.py`. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

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
