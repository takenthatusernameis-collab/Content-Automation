# RUNS

## Run 416 — 2026-10-09T01:20:00Z
- Objective: Run the later-packet dry-run and fix only a real failure.
- Action: Title, publish, expand, caption, asset, research, and render dry-runs on a tab packet did not leak the morning reopen. `idea_brief.py` still replaced a filled viewer and why-now with the generic stall template. Suggested paste now keeps those packet lines. The idea brief contract covers the fixture. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Compacted logs that were already over the section cap.
- Result: Videos published stay 0. Unmatched paste keeps the packet viewer and why-now. Q1 idea.md unchanged.
- Verification: `python3 tools/idea_brief_contract.py` printed IDEA BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Queue-matched and blank-problem paths were already grounded. The leak was a filled viewer treated as missing. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs 395-416 stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 415 — 2026-10-09T00:20:00Z
- Objective: Run the later-packet dry-run and fix only a real failure.
- Action: Title, publish, expand, caption, asset, and new-idea dry-runs on a tab packet did not leak the morning reopen. `idea_brief.py` still suggested the channel morning line when the packet had a problem but no queue row. Suggested paste now uses that packet's problem and mechanism. The idea brief contract covers the fixture. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Unmatched paste names the extra tab. Q1 idea.md unchanged.
- Verification: `python3 tools/idea_brief_contract.py` printed IDEA BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Queue-matched rows were already grounded. The leak was the no-row placeholder, which still counted as a blank problem. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs should stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 414 — 2026-10-08T23:20:00Z
- Objective: Run the later-packet dry-run and fix only a real failure.
- Action: A Q5-shaped packet dry-run named the checklist stall, not the morning reopen. Title alts still ended on `to` and `the` after the 70-character cut. `clip_title` now drops a trailing glue word. The title contract covers that fixture. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Long alts end on a content word. Q1 titles.md unchanged.
- Verification: `python3 tools/title_brief_contract.py` printed TITLE BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The length cut was already on a word boundary, but the last kept word was glue. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs should stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 413 — 2026-10-08T22:20:00Z
- Objective: Run the later-packet dry-run and fix only a real failure.
- Action: `new_idea.py` treated four shared title words as the Q4 row, so a near tab topic inherited "shutdown default" and "just checking one more thing". A queued one_line now requires at least 80% of that row's title tokens. The exact Q4 title still uses its one_line. The ground contract covers both. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Near tab topic names its own step. Exact Q4 title keeps the queued one_line. Q1 idea.md unchanged.
- Verification: `python3 tools/idea_ground_contract.py` printed IDEA GROUND CONTRACT PASS. `python3 tools/selftest.py` after log compact. No provider write.
- Discovery: Token overlap of 3 was matching a neighbor row, not this topic. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs should stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 412 — 2026-10-08T21:15:00Z
- Objective: Run the later-packet dry-run and fix only a real failure.
- Action: A packet with a filled `Topic:` line and an empty `working_title:` followed by `## Promise` made the title brief Primary `Promise`. `title_thumb_brief.py` field parse no longer consumes the newline after the colon. The title contract covers that fixture. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Empty working_title falls back to the idea topic. Q1 titles.md unchanged.
- Verification: `python3 tools/title_brief_contract.py` printed TITLE BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The pasted Topic path from Run 410 was fine. The leak was an empty field plus a markdown heading, not another first-video phrase. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs should stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 411 — 2026-10-08T20:20:00Z
- Objective: Run the later-packet dry-run and fix only a real failure.
- Action: Title, publish, expand, caption, asset, research, and render dry-runs on a tab packet did not leak the morning reopen. `idea_brief.py` still treated a pasted `Topic:` line as blank. It now reads that line, and the contract covers the fixture. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Plain Topic reprint shows the idea topic. Q1 idea.md unchanged.
- Verification: `python3 tools/idea_brief_contract.py` printed IDEA BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Run 410 fixed the same pasted line for titles and upload title. The idea reprint still ignored it, so a human would refill a card that was already filled. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 410 — 2026-10-08T18:16:00Z
- Objective: Run the later-packet dry-run and fix only a real failure.
- Action: Canonical tab packet briefs passed. A pasted `Topic:` line with no dash made the title brief and the upload title use the folder id. `title_thumb_brief.py` and `publish_brief.py` now read that line, and a folder fallback drops the numeric id. `research_brief.py` also reads a short mechanism label. Contracts cover the plain Topic fixture. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Plain Topic upload title is the idea topic. Folder id is not a tag. Q1 files unchanged.
- Verification: `python3 tools/title_brief_contract.py` and `python3 tools/publish_brief_contract.py` passed. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The dash-bullet path was already grounded. The remaining leak was a pasted field line, not another first-video phrase. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 409 — 2026-10-08T17:20:00Z
- Objective: Run the later-packet dry-run Run 408 closed the phrase streak on, and fix only a real failure.
- Action: Dry-ran idea, title, publish, expand, caption, asset, research, and render on a temp Q4 packet. Publish used the folder name as the upload title when titles.md was absent. `primary_title` now uses the idea topic before the folder name. Contract covers that fixture. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Bare later-packet title is the idea topic. Folder tokens are not tags. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` printed PUBLISH BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Grounded briefs otherwise named the extra tab, not the morning reopen. The remaining publish leak was the folder slug, not another first-video phrase. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.


- Objective: Stop the Q1 hint from leaving the human publish step unnamed.
- Action: `hint.py` prints `python3 tools/operator_card.py` for this packet. `next_action.py` names that same command. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Hint command list includes the operator card. Q1 files unchanged.
- Verification: `python3 tools/hint.py` and `python3 tools/next_action.py` on the Q1 packet. Selftest after compact. No provider write.
- Discovery: Runs 395-407 each grounded one phrase while videos published stayed 0. That streak is now the suspicious loop. Do not open another phrase edit unless a later-packet dry-run fails. oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 407 — 2026-10-08T14:15:00Z
- Objective: Stop later idea cards from using the channel niche line as why now.
- Action: `new_idea.py` names why now from that topic. A morning reopen or an install line stays only when the topic already says morning, reopen, install, or default. The contract checks a tab-closing fixture and still requires Q1 idea.md unchanged. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Dry-run why-now names the extra tab. Q1 idea file unchanged.
- Verification: `python3 tools/idea_ground_contract.py` printed IDEA GROUND CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Run 406 grounded the suggested paste, but `new_idea.py` still wrote "working niche" on every card. A tab topic would still need a human rewrite of why now. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Packet-ground edits continue while videos published stay 0; this one removes a repeated rewrite, it does not add a freeze.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 idea.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 406 — 2026-10-08T13:22:00Z
- Objective: Stop later idea pastes from inheriting the planning-stall viewer and an install line.
- Action: `idea_brief.py` names the viewer and why-now from that row. Planning-stall audience and "stall to install" stay only when the row already says planning, every morning, install, or default. The contract checks Q3 and the Q2 reprint and still does not write idea.md. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Q3 paste names competing lists and does not say install. Q1 idea file unchanged.
- Verification: `python3 tools/idea_brief_contract.py` printed IDEA BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Run 405 grounded `new_idea.py`, but the suggested paste still stamped the channel planning viewer and told every row to install its stall. A human pasting Q3 would rewrite both lines. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Packet-ground edits continue while videos published stay 0; this one removes a repeated rewrite, it does not add a freeze.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 idea.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 405 — 2026-10-08T12:21:00Z
- Objective: Stop later idea cards from inheriting the first video's planning-stall viewer.
- Action: `new_idea.py` builds the viewer line from the topic. "stalls after planning" stays off unless the topic already says planning. The contract checks a tab-closing fixture and still requires Q1 idea.md unchanged. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Dry-run viewer names the tab. Q1 idea file unchanged.
- Verification: `python3 tools/idea_ground_contract.py` printed IDEA GROUND CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Run 396 grounded the mechanism and beat titles, but every later card still opened with the planning-stall viewer. A tab topic would still need a human rewrite of that line. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Packet-ground edits continue while videos published stay 0; this one removes a repeated rewrite, it does not add a freeze.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 idea.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 404 — 2026-10-08T11:17:00Z
- Objective: Stop later expand briefs from telling a short draft to grow without this packet's stall.
- Action: `expand_brief.py` adds a growth line from idea.md problem or mechanism when the brief is short or empty. A morning reopen stays forbidden unless the idea card already says it. The contract checks a tab fixture and still requires Q1 expand.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture growth line names the extra tab. Q1 expand file unchanged.
- Verification: `python3 tools/expand_brief_contract.py` printed EXPAND BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The budget said only how many words to add. A later short script about a tab would still be grown as the first video's morning reopen unless a human rewrote the beat. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Packet-ground edits continue while videos published stay 0; this one removes a repeated rewrite, it does not add a freeze.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 expand.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.
