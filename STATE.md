# STATE

Updated: 2026-09-12T14:25:00Z (Run 095)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + write-path + words.py band + idea-lock INFO + words_contract IN BAND --strict 0 + idea_brief --queue** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- idea_brief reprints only; never writes idea.md
- idea_brief --queue ID reprints the paste from topic_queue without a videos/ folder
- PATH/draft.md is not script.md until apply --write
- Run 093: words.py print_idea_lock_notes() imports apply_script.idea_lock_notes after Next. Fallback INFO if import fails. --strict still keys off the total band only.
- Run 094: words_contract.py proves an IN BAND tempfile draft exits 0 under --strict while INFO still prints. Did not map words_contract.py.
- Run 095: idea_brief.py --queue Q1 prints the same six-field paste as --block without requiring scaffold. --check still needs a folder. Did not map idea_brief. Did not scaffold Q1.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 095)
- tools/idea_lock.py still available as an optional extra CLI
- apply_script.py still owns idea_lock_notes()
- words.py prints idea-lock INFO so the extra CLI is not required
- words_contract.py checks markers, BELOW/ABOVE exit 2, IN BAND --strict exit 0, and that INFO appears
- idea_brief.py --queue ID works before a packet folder exists
- No new packet folder; queue still queued

## Pipeline map
Before scaffold: `python3 tools/idea_brief.py --queue Q1` reprints the idea.md paste.
After scaffold: idea_brief --block / paste / --check / expand_prompt / save draft.md / `words.py PATH` / apply dry-run / `--write --refresh` / set_status ready_for_vo if WORDS in band.
`idea_lock.py PATH` is optional once words.py prints the notes.
After a high-risk GitHub write: `python3 tools/prove_locks.py`.
Start of session: `python3 tools/queue_status.py` then `python3 tools/next_topic.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 80 | 79 | paste is available before scaffold; folder still human-owned |
| Automated steps | 75 | 76 | idea_brief --queue reprint |
| Videos produced | 0 | 0 | fixture only |

## Active constraints
- Do not auto-scaffold Q1
- Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / needed.py
- Do not make idea-lock INFO a BLOCKED error or --strict FAIL
- Do not treat draft.md as script.md
- Do not write idea.md from idea_brief (including --queue)
- Do not retry HTTPS clone as the first action
- Do not spend a run aligning another page to name idea_brief
- Do not drop the words.py import fallback
- Do not add another wrapper CLI around idea_lock_notes
