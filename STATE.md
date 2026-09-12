# STATE

Updated: 2026-09-12T12:15:00Z (Run 093)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + write-path + words.py band + idea-lock INFO inside words.py** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- idea_brief reprints only; never writes idea.md
- PATH/draft.md is not script.md until apply --write
- Run 091: apply_script.py dry-run prints idea-lock INFO. INFO never blocks --write.
- Run 092: tools/idea_lock.py prints the same INFO. Exit 0. Unmapped.
- Run 093: words.py print_idea_lock_notes() imports apply_script.idea_lock_notes after Next. Fallback INFO if import fails. --strict still keys off the total band only.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 093)
- tools/idea_lock.py still available as an optional extra CLI
- apply_script.py still owns idea_lock_notes()
- words.py prints idea-lock INFO so the extra CLI is not required
- words_contract.py checks the print_idea_lock_notes marker and that INFO appears; --strict still exits 2 on BELOW/ABOVE
- No new packet folder; queue still queued

## Pipeline map
After scaffold: idea_brief --block / paste / --check / expand_prompt / save draft.md / `words.py PATH` / apply dry-run / `--write --refresh` / set_status ready_for_vo if WORDS in band.
`idea_lock.py PATH` is optional once words.py prints the notes.
After a high-risk GitHub write: `python3 tools/prove_locks.py`.
Start of session: `python3 tools/queue_status.py` then `python3 tools/next_topic.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 82 | 81 | idea-lock INFO now rides on the words.py pass |
| Automated steps | 73 | 74 | words.py folds apply_script.idea_lock_notes |
| Videos produced | 0 | 0 | fixture only |

## Active constraints
- Do not auto-scaffold Q1
- Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / needed.py
- Do not make idea-lock INFO a BLOCKED error or --strict FAIL
- Do not treat draft.md as script.md
- Do not write idea.md from idea_brief
- Do not retry HTTPS clone as the first action
- Do not spend a run aligning another page to name idea_brief
- Do not drop the words.py import fallback
