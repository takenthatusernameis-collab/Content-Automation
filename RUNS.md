# RUNS

## Run 394 — 2026-10-08T00:20:00Z
- Objective: Stop later title briefs from copying the first video's slogans.
- Action: `title_thumb_brief.py` keeps a title only when its content words are in that packet. The on-image line uses the mechanism tokens, not "One Written Default". The contract refuses those Q1 slogans on an inbox fixture and still requires Q1 titles.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture titles name the inbox. Q1 title file unchanged.
- Verification: `python3 tools/title_brief_contract.py` printed TITLE BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The title pads were aliases for packet 002. A later script about a different stall would still offer "Stop Deciding Every Morning" unless a human rewrote the list. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 titles. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 393 — 2026-10-07T23:12:00Z
- Objective: Stop later chapter drafts from copying the first video's chapter titles.
- Action: `chapter_draft.py` builds a short title from the beat's spoken words. Generic Hook, payoff, and CTA headings no longer become "The reopen", "Written default", or "Tomorrow's sentence". The existing selftest refuses those Q1 labels on a fixture and still requires Q1 chapters.md to keep "0:00 The reopen". Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture chapter titles come from the fixture script. Q1 chapter file unchanged.
- Verification: `check_chapter_draft_fail_closed` returned no failures. No provider write.
- Discovery: The label helpers were aliases for packet 002. A later script about a different stall would still publish "The reopen" unless a human retyped the lines. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 chapters. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

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
