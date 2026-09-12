# STATE

Updated: 2026-09-12T20:05:00Z (Run 101)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + write-path + words.py band + idea-lock INFO + words_contract IN BAND --strict 0 + idea_brief --queue + idea_brief_contract --queue lock + queue printers print --queue + doctor all-packet Queue next footer + needed --plan WAVE 3 start sequence + WAVE 3 doctor reconstruct + doctor reconstruct lists imports** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- idea_brief reprints only; never writes idea.md
- idea_brief --queue ID reprints the paste from topic_queue without a videos/ folder
- PATH/draft.md is not script.md until apply --write
- Run 101: `needed.py doctor.py` lists doctor.py plus the seven files it imports or reads. `--missing` is READY only when those eight paths exist. Exit stays 0. which_contract.MAP unchanged. --plan WAVE 3 still prints only the reconstruct command, not the file dump. Did not scaffold Q1. Did not add WAVE 4.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 101)
- tools/idea_lock.py still available as an optional extra CLI
- apply_script.py still owns idea_lock_notes()
- words.py prints idea-lock INFO so the extra CLI is not required
- words_contract.py checks markers, BELOW/ABOVE exit 2, IN BAND --strict exit 0, and that INFO appears
- idea_brief.py --queue ID works before a packet folder exists
- idea_brief_contract.py locks that --queue path
- queue_status / next_topic surface --queue on the live board
- doctor all-packet run surfaces the same first ok-queued --queue line
- needed.py --plan WAVE 3 reconstructs the board and unmapped doctor before the start commands
- needed.py doctor.py reconstruct lists hint, next_action, pipeline_status, queue_lib, queue_status, validate_packet, topic_queue
- No new packet folder; queue still queued

## Pipeline map
Before scaffold: `python3 tools/doctor.py` (no path) prints fixture health then `Queue next` with `idea_brief.py --queue Q1`. `python3 tools/queue_status.py` / `python3 tools/next_topic.py` print the same `--queue` line.
Clone-less reconstruct: `python3 tools/needed.py --plan` WAVE 3 reconstructs queue_status then doctor.py, then runs doctor / queue_status / next_topic. `needed.py doctor.py --missing` is READY only after doctor imports are on disk.
After scaffold: idea_brief --block / paste / --check / expand_prompt / save draft.md / `words.py PATH` / apply dry-run / `--write --refresh` / set_status ready_for_vo if WORDS in band.
`idea_lock.py PATH` is optional once words.py prints the notes.
After a high-risk GitHub write: `python3 tools/prove_locks.py`.
Start of session: `python3 tools/doctor.py` then `python3 tools/queue_status.py` then `python3 tools/next_topic.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 74 | 73 | Clone-less doctor READY now means doctor can import |
| Automated steps | 81 | 82 | needed.py doctor reconstruct lists imports |
| Videos produced | 0 | 0 | fixture only |

## Active constraints
- Do not auto-scaffold Q1
- Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / needed.py / idea_brief.py / idea_brief_contract.py / doctor.py
- Do not make idea-lock INFO a BLOCKED error or --strict FAIL
- Do not treat draft.md as script.md
- Do not write idea.md from idea_brief (including --queue)
- Do not retry HTTPS clone as the first action
- Do not spend a run aligning another page to name idea_brief
- Do not drop the words.py import fallback
- Do not add another wrapper CLI around idea_lock_notes
- Do not add another idea_brief flag unless --queue regresses
- Do not print --queue for a mark-needed row (folder already exists; use --block/--check)
- Do not print Queue next when doctor is given a single packet path
- Do not wrap doctor in start.py
- Do not add WAVE 4
- Do not list doctor internals inside --plan WAVE 3
