# RUNS

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
