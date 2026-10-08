# RUNS

## Run 398 — 2026-10-08T04:11:00Z
- Objective: Stop the default idea reprint from suggesting the first video's morning why-now line for later packets.
- Action: `idea_brief.py` suggested paste now calls `why_now_line(problem)`, matching `--block` and `--queue`. The contract runs a Q2 tempfile reprint and still does not write idea.md. Selftest calls the existing contract. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Q2 suggested paste names the start-cue stall. Q1 idea file unchanged.
- Verification: `python3 tools/idea_brief_contract.py` printed IDEA BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: `--block` was fixed in Run 390, but the default suggested section still printed the shared morning sentence. A human following that section would rewrite why now on every later card. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 idea.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 397 — 2026-10-08T03:11:00Z
- Objective: Stop later scripts from being told to grow the first video's morning scene.
- Action: `script_writer.md` and `script_expander.md` grow a short beat from this packet's stall. A morning reopen stays allowed only when the idea card is about the morning. `expand_prompt.py` repeats that rule in the assembled prompt. The contract checks a tab-closing fixture and still requires Q1 script.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Assembled prompt names the extra tab. Q1 script file unchanged.
- Verification: `python3 tools/script_prompt_contract.py` printed SCRIPT PROMPT CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The writer contract aliased every short draft to a morning scene. A later script about a tab would still be padded with the first video's reopen unless a human rewrote the beat. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 script.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 396 — 2026-10-08T02:11:00Z
- Objective: Stop later idea cards from inheriting the first video's mechanism and beat titles.
- Action: `new_idea.py` builds the mechanism from the topic, or from a queued one_line only when the topic already matches that row. Beat titles use the topic instead of "The default that replaces the decision". `--dry-run` prints the card and does not create a folder. The contract checks a tab topic and still requires Q1 idea.md unchanged. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Dry-run names the topic. Q1 idea file unchanged.
- Verification: `python3 tools/idea_ground_contract.py` printed IDEA GROUND CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The idea scaffolder aliased every new topic to the first video's written default. A later topic about a tab would still open with that mechanism unless a human rewrote the card. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 idea.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 395 — 2026-10-08T01:15:00Z
- Objective: Stop later publish stubs from inheriting the first video's tags.
- Action: `publish_brief.py` keeps focused work, productivity systems, and deep work, then adds words from that packet. "start cue", "decision fatigue", and "work defaults" stay off unless those words are already in the packet. A missing mechanism no longer becomes "a written default" or a mood-dependent start. The contract checks a tab-closing fixture and still requires Q1 publish.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture tags name the tab, not the start cue. Q1 publish file unchanged.
- Verification: `python3 tools/publish_brief_contract.py` printed PUBLISH BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The tag list was a fixed six, including the next queued mechanism. A later video about closing a tab would still upload "start cue" and "decision fatigue" unless a human trimmed the stub. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 publish.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

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
