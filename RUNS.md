# RUNS

## Run 425 — 2026-10-09T10:20:00Z
- Objective: Verify Run 424 publish contract, stop the publish-stub loop if the dry-run is clean, and fix one other later-packet leak.
- Action: `publish_brief_contract.py` passed. Keys, mug, and window publish dry-runs did not emit a machine stall sentence or a lone tag the title/mechanism rule missed. Did not edit publish_brief. Caption dry-run on a plain beat counted words and printed an empty cue. `spoken_text` now uses the same body as the word count. Visual notes stay out. Added `tools/caption_brief_contract.py`. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Plain-beat cues now carry the spoken line. Q1 captions.md and publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS. `python3 tools/caption_brief_contract.py` PASS. Sample caption dry-run still prints WORDS lines. `python3 tools/selftest.py` PASS. No provider write.
- Discovery: Run 424 closed the tag-source leak. The next human rewrite was caption stubs that counted a plain sentence and left the dash empty. Suspicious: oauth_idle_without_publish is unchanged since before Run 270. Publish-stub microfixes 420-424 had no new failure this run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/caption_brief_contract.py` before any new caption edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief again unless a dry-run still emits a machine sentence or a lone tag the title/mechanism rule does not drop.

## Run 424 — 2026-10-09T09:12:00Z
- Objective: Verify Run 423 publish contract, then fix only a real later-packet publish dry-run failure.
- Action: `publish_brief_contract.py` passed. Later-packet dry-runs still emitted lone tags from problem prose and title imperatives (`under`, `while`, `already`, `hang`, `set`, `down`). Tag source is now title and mechanism only. Command-first words and short mechanism-only words are skipped. Contract covers the keys packet and the mug packet. Did not grow TAG_GLUE. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Those leaks are gone on the later-packet dry-run. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS after the edit. `python3 tools/selftest.py` PASS. No provider write.
- Discovery: Run 423 skipped listed function words and still tokenized the problem sentence. A source rule beats another skip-list append. Suspicious: publish-stub microfixes now span runs 420-424 while oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not grow STOP or TAG_GLUE. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief again unless a dry-run still emits a machine sentence or a lone tag the title/mechanism rule does not drop.


## Run 423 — 2026-10-09T08:14:00Z
- Objective: Verify Run 422 publish contract, then fix only a real later-packet publish dry-run failure.
- Action: `publish_brief_contract.py` passed. Later-packet dry-runs still printed `If the stall named in this packet` with no problem, and lone tags don't/until/ends/onto/has/where/does. Description now omits that machine sentence. Those function words are skipped. Contract covers the empty-problem packet, inbox tags, bag tags, and phone tags. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Those leaks are gone on the later-packet dry-run. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS after the edit. No provider write.
- Discovery: Run 422 fixed period, imperative, and bare so-clause only. Incomplete packets still needed a human delete of the stall sentence, and function words still became tags. Suspicious: publish-stub microfixes now span runs 420-423 while oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not open a phrase edit unless a later-packet title dry-run fails. Do not edit publish_brief again unless a dry-run still emits a machine sentence or a lone tag a human would delete.

## Run 422 — 2026-10-09T07:14:00Z
- Objective: Verify Run 421 publish contract, then fix only a real later-packet publish dry-run failure.
- Action: `publish_brief_contract.py` passed. Later-packet dry-runs still printed `Shut the lid..`, `If don't reopen the inbox until the block ends`, and `If the notebook stays in the bag so the block has no page`. Description now keeps a finished period, keeps an imperative problem, and keeps a bare so-clause. Contract covers lid, inbox, and notebook packets. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Did not open a title phrase edit.
- Result: Videos published stay 0. Those three description leaks are gone on the later-packet dry-run. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS after the edit. No provider write.
- Discovery: Run 421 skipped lone verbs only. The description still needed a human rewrite on punctuated titles, imperative problems, and so-clauses without a comma. Suspicious: publish-stub microfixes now span runs 420-422 while oauth_idle_without_publish is unchanged since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not open a phrase edit unless a later-packet title dry-run fails. Do not add another lone-verb skip unless a dry-run still emits one.

## Run 421 — 2026-10-09T06:20:00Z
- Objective: Verify Run 420 publish contract, then fix only a real later-packet dry-run failure.
- Action: `publish_brief_contract.py` and `title_brief_contract.py` passed. Phone and charger title dry-runs passed SELF_CHECK. No phrase edit. Publish dry-run still tagged leave/put/walk and fill as lone tags. TAG_GLUE now skips those verbs. Contract covers the desk and glass packets. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Charger tags are charger/desk/block/kitchen, not leave/put/walk. Q1 publish.md unchanged.
- Verification: `python3 tools/publish_brief_contract.py` PASS. `python3 tools/title_brief_contract.py` PASS. `python3 tools/selftest.py` PASS. Charger publish dry-run dropped leave/put/walk and kept the existing problem clause. No provider write.
- Discovery: Run 420 dropped before/starts/stays only. Leave/put/walk/fill were still content tokens, so every later stub still needed a tag trim. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not open a phrase edit unless a later-packet title dry-run fails.

## Run 420 — 2026-10-09T05:15:00Z
- Objective: Verify Run 419 title contract, then fix only a real later-packet dry-run failure.
- Action: `title_brief_contract.py` passed. Phone and charger title dry-runs passed SELF_CHECK (on-image `Leave Charger Kitchen Block`). Idea check stayed PASTE READY. No phrase edit. Publish dry-run still printed `If the charger stays in the kitchen, so the block starts with a walk` and lone tags before/starts/stays. Stall line now keeps a problem that already has ", so ". Lone glue tags are skipped. Contract covers that packet. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Later-packet description no longer double-wraps the stall. Tags keep charger/kitchen/block and drop before/starts/stays. Q1 publish.md unchanged.
- Verification: `python3 tools/title_brief_contract.py` PASS. `python3 tools/publish_brief_contract.py` PASS. `python3 tools/selftest.py` PASS. Charger publish dry-run printed the problem clause without a second If. No provider write.
- Discovery: Run 419 fixed thumbnail endings only. Publish still prefixed If onto a full problem and tokenized before/starts/stays into tags. Suspicious: oauth_idle_without_publish still has no publish since before Run 270.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/publish_brief_contract.py` before any new publish edit. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not open a phrase edit unless a later-packet title dry-run fails.


## Run 419 — 2026-10-09T04:20:00Z
- Objective: Verify Run 418 title contract, then fix only a real later-packet dry-run failure.
- Action: `title_brief_contract.py` passed. Phone, charger, and tab dry-runs did not borrow the morning reopen. `title_thumb_brief.py --dry-run` still ended on-image text on Before (`Leave Charger Kitchen Before`). `thumb_line` now skips trailing before/after/into, and self-check rejects that ending. Title contract covers the charger thumb. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Charger on-image text is `Leave Charger Kitchen Block`, not `... Before`. Q1 titles.md and thumbnail.md unchanged.
- Verification: `python3 tools/title_brief_contract.py` PASS. `python3 tools/selftest.py` PASS. Charger dry-run printed SELF_CHECK PASS. No provider write.
- Discovery: Run 418 stripped trailing glue from titles only. Thumbnail text took the first four content tokens, and before is not a stop word. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs 395-419 stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/title_brief_contract.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 418 — 2026-10-09T03:16:00Z
- Objective: Verify Run 417 contracts, then fix only a real later-packet dry-run failure.
- Action: `idea_check_contract.py` and `idea_brief_contract.py` passed. Idea, publish, expand, caption, asset, and research dry-runs on an unmatched phone packet did not borrow the morning reopen. `title_thumb_brief.py --dry-run` still ended an alt on Before. `clip_title` now drops trailing before/after/into. Title contract covers that packet. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. Phone alt is `Face Phone Down Another Room`, not `... Before`. Q1 titles.md unchanged.
- Verification: `python3 tools/idea_check_contract.py` PASS. `python3 tools/idea_brief_contract.py` PASS. `python3 tools/title_brief_contract.py` PASS. `python3 tools/selftest.py` PASS. No provider write.
- Discovery: Run 414 stripped to/the/so/from/of/a. Before was still a content word, so a short noun phrase could end on it. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs 395-418 stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/title_brief_contract.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 417 — 2026-10-09T02:11:00Z
- Objective: Run the later-packet dry-run and fix only a real failure.
- Action: Suggested paste already kept a filled unmatched viewer, problem, and why-now. `idea_brief.py --check` still compared those fields to the queue placeholder and printed PASTE INCOMPLETE. `--check` now uses `grounded_fields`. Added `tools/idea_check_contract.py`. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1.
- Result: Videos published stay 0. A filled later packet should now check as PASTE READY. Q1 idea.md unchanged.
- Verification: partial. The contract file was committed. This session could not execute Python (workspace shell unavailable). No provider write.
- Discovery: Run 416 fixed the reprint and left the gate a human runs next. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs 395-417 stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Next agent should run `python3 tools/idea_check_contract.py` and `python3 tools/idea_brief_contract.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

## Run 416 — 2026-10-09T01:20:00Z
- Objective: Run the later-packet dry-run and fix only a real failure.
- Action: Title, publish, expand, caption, asset, research, and render dry-runs on a tab packet did not leak the morning reopen. `idea_brief.py` still replaced a filled viewer and why-now with the generic stall template. Suggested paste now keeps those packet lines. The idea brief contract covers the fixture. Did not scaffold Q2. Did not poll secrets. Did not dispatch the workflow. Did not add a scanner, recovery edge, card extension, or compact check. Did not rewrite Q1. Compacted logs that were already over the section cap.
- Result: Videos published stay 0. Unmatched paste keeps the packet viewer and why-now. Q1 idea.md unchanged.
- Verification: `python3 tools/idea_brief_contract.py` printed IDEA BRIEF CONTRACT PASS. `python3 tools/selftest.py` printed SELFTEST PASS. No provider write.
- Discovery: Queue-matched and blank-problem paths were already grounded. The leak was a filled viewer treated as missing. Suspicious: oauth_idle_without_publish still has no publish since before Run 270. Phrase-edit runs 395-416 stay gated on a failed dry-run.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: A human follows issue 1 via `python3 tools/operator_card.py`. Do not regenerate Q1. Do not scaffold Q2. Do not poll secrets. Do not add a scanner.

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.
