# RUNS

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
