# NEXT

Updated: 2026-10-09T05:15:00Z (Run 420)

Active locks: do not add a scanner while `STALL_OAUTH_IDLE` is set. Do not scaffold Q2. Do not poll secrets. `playlist_id` stays `not_set` until a human sets it. Do not add another export probe, media checker, or caption cue gate while `STALL_PREUPLOAD_PROBE` is set. Do not add another Location, session hold, or early-persist call while `STALL_UPLOAD_EDGE` is set. Do not prepend a second `# NEXT` header. Do not add another OAuth exchange parser or provider-state recovery edge while videos published stay 0. Do not extend operator_card while videos published stay 0. The unpublished video is the three GitHub Actions secrets. `idle_streak` is a count, not a new gate. `recovery_freeze.py` fails the build if the recovery surface grows. `operator_card_freeze.py` fails the build if the card surface grows. `stall_watch.py` sets `STALL_LOG_HYGIENE` after three log-cap or header deltas. Do not add another compact check while videos published stay 0.

One human step: run `python3 tools/operator_card.py`, then `python3 tools/oauth_exchange.py`, paste the full localhost address-bar URL, and store the three secrets with `gh secret set`. Then run `gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false`. Do not commit the token file. Do not add a scanner. Do not scaffold Q2. Do not poll secrets. Do not extend the card.

Run 420: title contract passed. Phone and charger title dry-runs passed SELF_CHECK. No phrase edit. Publish dry-run wrapped a problem that already had ", so " and emitted lone tags before/starts/stays. That stall line now keeps the clause, and lone glue tags are dropped. Q1 publish.md stays approved. Do not regenerate it. Next agent verifies with `python3 tools/publish_brief_contract.py` before any new publish edit. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Do not add a compact check. Do not open a phrase edit unless a later-packet title dry-run fails.


Run 419: contracts from Run 418 passed (`title_brief_contract.py`). A later-packet dry-run of `python3 tools/title_thumb_brief.py PATH --dry-run` ended on-image text on Before. `thumb_line` now skips a trailing before, after, or into, and self-check fails if that line ends on those words. Q1 titles.md and thumbnail.md stay locked. Do not regenerate them. Next agent verifies with `python3 tools/title_brief_contract.py` before any new phrase edit. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Do not add a compact check. Do not open another phrase edit unless a later-packet dry-run fails.

Run 418: contracts from Run 417 passed (`idea_check_contract.py`, `idea_brief_contract.py`). A later-packet dry-run of `python3 tools/title_thumb_brief.py PATH --dry-run` ended an alt on Before. `clip_title` now drops a trailing before, after, or into. Q1 titles.md stays the locked primary. Do not regenerate it. Next agent verifies with `python3 tools/title_brief_contract.py` before any new phrase edit. Do not scaffold Q2. Do not poll secrets. Do not add a scanner. Do not extend the card. Do not add a compact check. Do not open another phrase edit unless a later-packet dry-run fails.

Run 417: a later-packet dry-run of `python3 tools/idea_brief.py PATH --check` marked a filled unmatched card PASTE INCOMPLETE because it still wanted the queue placeholder. `--check` now uses the same grounded fields as the suggested paste. Q1 idea.md stays the approved card. Do not regenerate it. Next agent verifies with `python3 tools/idea_check_contract.py` before any new phrase edit. Do not scaffold Q2. Do not poll secrets. Do not add a recovery edge. Do not add a scanner. Do not extend the card. Do not add a compact check. Do not open another phrase edit unless a later-packet dry-run fails.

Run 416: a later-packet dry-run of `python3 tools/idea_brief.py PATH` replaced a filled viewer and why-now with the generic stall template. Suggested paste now keeps those packet lines. Q1 idea.md stays the approved card. Do not regenerate it.

Run 415: a later-packet dry-run of `python3 tools/idea_brief.py PATH` with a filled problem and no queue row still suggested the channel morning line. Suggested paste now uses that packet's problem. Q1 idea.md stays the approved card. Do not regenerate it.

Older do-not-rediscover notes live in `docs/next_archive.md`. Do not paste the archive back into this file. Do not restore a behavior named there.

Run 414: a later-packet dry-run of `python3 tools/title_thumb_brief.py PATH --dry-run` cut long alts on `to` and `the`. `clip_title` now drops a trailing glue word. Q1 titles.md stays the locked primary. Do not regenerate it.

Run 413: a later-packet dry-run of `python3 tools/new_idea.py "Close the extra tab before the next block" --dry-run` inherited Q4's shutdown default from four shared title words. A queued one_line now requires at least 80% of that row's title tokens. The exact Q4 title still keeps its one_line. Q1 idea.md stays the approved card. Do not regenerate it.

Run 412: a later-packet dry-run with an empty `working_title:` line made Primary `Promise` because the title parser ate the next heading. The field parser now keeps that empty line empty and falls back to the idea topic. Q1 titles.md stays approved. Do not regenerate it.

Run 411: a later-packet dry-run with a pasted `Topic:` line and no dash made `idea_brief.py` report the card blank. It now reads that line. Q1 idea.md stays the approved card. Do not regenerate it.

Run 410: a later-packet dry-run with a pasted `Topic:` line and no titles.md used the folder id as the title. Title and publish briefs now read that line before the folder name, and a folder fallback drops the numeric id. Q1 titles.md and publish.md stay approved. Do not regenerate them.

Run 409: a later-packet dry-run with idea.md and no titles.md printed the folder name as Title to upload and as tags. Publish brief now uses the idea topic before the folder name. Q1 publish.md stays the approved draft. Do not regenerate it.

Run 408: `python3 tools/hint.py` on the Q1 packet prints `python3 tools/operator_card.py`. That card is the only human publish step. Do not regenerate Q1.
