# RUNS

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

## Run 403 — 2026-10-08T10:13:00Z
- Objective: Stop later title briefs from padding a thin packet with step numbers or a copied Primary.
- Action: `title_thumb_brief.py` fills remaining titles from that packet's words. The step-N pad and the Primary-repeat loop stay off. An empty phrase is not renamed "the default" or "This Step". The contract checks a one-word Inbox fixture and still requires Q1 titles.md and thumbnail.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture titles stay distinct and do not say step N. Q1 title files unchanged.
- Verification: `python3 tools/title_brief_contract.py` printed TITLE BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The fill loop emitted "X step N", which never grounded, then the renderer copied Primary into every empty alt. A human would delete those repeats on every thin packet. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Packet-ground edits continue while videos published stay 0; this one removes a repeated delete, it does not add a freeze.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 titles.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 402 — 2026-10-08T09:13:00Z
- Objective: Stop later thumbnail briefs from renaming a one-word step to Name The Step.
- Action: `title_thumb_brief.py` keeps the packet token on the image line. The Name The Step pad stays off. The contract checks a one-word Inbox fixture and still requires Q1 titles.md and thumbnail.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture on-image text is Inbox. Q1 thumbnail file unchanged.
- Verification: `python3 tools/title_brief_contract.py` printed TITLE BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: A mechanism of one content word was discarded. A later thumbnail about an inbox would still say Name The Step unless a human rewrote it. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Packet-ground edits continue while videos published stay 0; this one removes a repeated rewrite, it does not add a freeze.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 thumbnail.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 401 — 2026-10-08T08:13:00Z
- Objective: Stop later thumbnail briefs from copying the first video's planning-clutter contrast.
- Action: `title_thumb_brief.py` builds Contrast from this packet's stall and step. The empty-panel line stays only when the packet already says it. The contract checks an inbox fixture and still requires Q1 titles.md and thumbnail.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture contrast names the mixed folders, not planning clutter. Q1 thumbnail file unchanged.
- Verification: `python3 tools/title_brief_contract.py` printed TITLE BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The contrast line was a fixed first-video visual. A later thumbnail about an inbox would still say leftover planning clutter unless a human rewrote it. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Packet-ground edits continue while videos published stay 0; this one removes a repeated rewrite, it does not add a freeze.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 thumbnail.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 400 — 2026-10-08T07:14:00Z
- Objective: Stop later publish stubs from failing the upload gate on a machine note.
- Action: `publish_brief.py` writes the lock sentence under Machine note, not Description. `viewer_description` drops "No upload happened" and the lock sentence before videos.insert. The contract refuses those lines in Description and still requires Q1 publish.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. A later stub description no longer contains the machine note. Q1 publish.md bytes unchanged.
- Verification: `python3 tools/publish_brief_contract.py` printed PUBLISH BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The stub sentence lived in Description, and the uploader refuses that marker even after the checklist is checked. A human would delete it on every later video. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Packet-ground edits continue while videos published stay 0; this one removes a repeated delete, it does not add a freeze.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 publish.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 399 — 2026-10-08T06:17:00Z
- Objective: Stop later publish descriptions from calling every mechanism a default to install.
- Action: `publish_brief.py` uses this packet's step. "that default" and "install" stay off unless the mechanism already says default. The contract checks a tab-closing fixture and still requires Q1 publish.md unchanged. Did not regenerate Q1. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check.
- Result: Videos published stay 0. Fixture description names the tab step. Q1 publish file unchanged.
- Verification: `python3 tools/publish_brief_contract.py` printed PUBLISH BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: The description template still said every later video walks a default and tells the viewer to install it. A tab-closing packet would have needed a human rewrite of that sentence. Suspicious: oauth_idle_without_publish still has no publish since before Run 270, and Runs 390-399 kept grounding packet copy instead of a publish.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1. Do not regenerate Q1 publish.md. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.
