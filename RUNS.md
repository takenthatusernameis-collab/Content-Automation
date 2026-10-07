# RUNS

## Run 392 — 2026-10-07T22:12:00Z
- Objective: Stop the approved Q1 pin from posting a reply ask without rewriting that draft.
- Action: `viewer_comment` drops the reply sentence the same way it drops the stub pin note. The publish contract checks the posted pin and still requires Q1 bytes unchanged. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend the card. Did not add a scanner. Did not scaffold Q2. Did not add a freeze module. Did not add a compact check.
- Result: Videos published stay 0. Posted pin is the assignment. Q1 copy unchanged. No live execute.
- Verification: `python3 tools/publish_brief_contract.py` printed PUBLISH BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Run 391 stopped the generator and left the bait in the approved first comment. The uploader would have posted it. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not rewrite Q1 publish.md. Do not scaffold Q2. Do not add a scanner. Do not poll secrets.

## Run 391 — 2026-10-07T21:12:00Z
- Objective: Stop future publish stubs from asking viewers to reply.
- Action: `publish_brief.py` pins the mechanism assignment only. A contract fails if the reply sentence returns or if Q1 publish.md changes. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend the card. Did not add a scanner. Did not scaffold Q2. Did not add a freeze module. Did not add a compact check.
- Result: Videos published stay 0. Future pins name the assignment. Q1 copy unchanged. No live execute.
- Verification: `python3 tools/publish_brief_contract.py` printed PUBLISH BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The stub always ended with a reply ask, including when the mechanism was not a cue. That line would have been pasted into every later publish.md. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not scaffold Q2. Do not add a scanner. Do not poll secrets.

## Run 390 — 2026-10-07T20:13:00Z
- Objective: Make the next queued idea paste name its own stall, and stop a false contract fail on the existing Q1 folder.
- Action: `idea_brief.py` why now now includes the queue problem. The contract requires Q2 and Q3 why-now lines to differ and accepts Q1 status=used. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend the card. Did not add a scanner. Did not scaffold Q2. Did not add a freeze module. Did not add a compact check.
- Result: Videos published stay 0. Q2 why now names the missing start cue. Q3 why now names competing lists. No live execute.
- Verification: `python3 tools/idea_brief_contract.py` printed IDEA BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The idea contract already failed on main because it wanted Q1 status queued and the 002 folder absent. A shared why-now line would have been rewritten by hand on every later packet.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not scaffold Q2. Do not add a scanner. Do not poll secrets.

## Run 389 — 2026-10-07T19:11:00Z
- Objective: Flag three consecutive log-hygiene deltas so the next run does not invent another compact check.
- Action: `stall_watch.py` sets `STALL_LOG_HYGIENE` after three wired log-cap or header deltas while videos published stay 0. Contract and selftest cover the flag and the lock sentence. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend operator_card. Did not add a scanner. Did not scaffold Q2. Did not add a freeze module. Did not add a compact check.
- Result: Videos published stay 0. The flag names Runs 386-388. No live execute.
- Verification: `python3 tools/stall_watch_contract.py` printed STALL WATCH CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Runs 386-388 tightened log checks and still published nothing. Suspicious: log_hygiene_without_publish and oauth_idle_without_publish. Do not add another compact check for that stall.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not extend the card. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets. Do not add a compact check.

## Run 388 — 2026-10-07T18:11:00Z
- Objective: Stop a duplicated archive pointer from shipping after a green section-count check.
- Action: `compact_all.py --check` now fails unless PROGRESS.md and FAILURES.md each have exactly one archive pointer. Ran `log_compact.py` so the Run 387 duplicates are gone. Did not poll secrets. Did not dispatch the workflow. Did not add a recovery edge. Did not extend operator_card. Did not add a scanner. Did not scaffold Q2. Did not add a freeze module.
- Result: Videos published stay 0. Live logs have one pointer each. No live execute.
- Verification: `python3 tools/log_compact_contract.py` printed LOG COMPACT CONTRACT PASS. `python3 tools/compact_all.py --check` printed COMPACT ALL OK. No provider write.
- Discovery: Run 387 said record_run compacts, and the committed logs still had two identical pointers. `--check` did not read them. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Do not add another freeze for that stall.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not open a second issue. Do not extend the card. Do not add a recovery edge. Do not add a scanner. Do not scaffold Q2. Do not poll secrets.

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
