# STATE

Updated: 2026-09-12T16:20:00Z (Run 097)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + write-path + words.py band + idea-lock INFO + words_contract IN BAND --strict 0 + idea_brief --queue + idea_brief_contract --queue lock + queue printers print --queue** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- idea_brief reprints only; never writes idea.md
- idea_brief --queue ID reprints the paste from topic_queue without a videos/ folder
- PATH/draft.md is not script.md until apply --write
- Run 097: queue_status.py and next_topic.py print `idea_brief.py --queue ID` for the first ok-queued row before scaffold. queue_contract locks that the tempfile board prints `--queue Q2` (first ok-queued) and not `--queue Q1` (mark-needed). Did not scaffold Q1. Did not map idea_brief.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 097)
- tools/idea_lock.py still available as an optional extra CLI
- apply_script.py still owns idea_lock_notes()
- words.py prints idea-lock INFO so the extra CLI is not required
- words_contract.py checks markers, BELOW/ABOVE exit 2, IN BAND --strict exit 0, and that INFO appears
- idea_brief.py --queue ID works before a packet folder exists
- idea_brief_contract.py locks that --queue path
- queue_status / next_topic surface --queue on the live board
- No new packet folder; queue still queued

## Pipeline map
Before scaffold: `python3 tools/queue_status.py` / `python3 tools/next_topic.py` print `python3 tools/idea_brief.py --queue Q1`. That reprints the idea.md paste.
After scaffold: idea_brief --block / paste / --check / expand_prompt / save draft.md / `words.py PATH` / apply dry-run / `--write --refresh` / set_status ready_for_vo if WORDS in band.
`idea_lock.py PATH` is optional once words.py prints the notes.
After a high-risk GitHub write: `python3 tools/prove_locks.py`.
Start of session: `python3 tools/queue_status.py` then `python3 tools/next_topic.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 78 | 77 | Operator no longer hunts docs for --queue |
| Automated steps | 77 | 78 | queue_contract locks pre-scaffold --queue print |
| Videos produced | 0 | 0 | fixture only |

## Active constraints
- Do not auto-scaffold Q1
- Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / needed.py / idea_brief.py / idea_brief_contract.py
- Do not make idea-lock INFO a BLOCKED error or --strict FAIL
- Do not treat draft.md as script.md
- Do not write idea.md from idea_brief (including --queue)
- Do not retry HTTPS clone as the first action
- Do not spend a run aligning another page to name idea_brief
- Do not drop the words.py import fallback
- Do not add another wrapper CLI around idea_lock_notes
- Do not add another idea_brief flag unless --queue regresses
- Do not print --queue for a mark-needed row (folder already exists; use --block/--check)
