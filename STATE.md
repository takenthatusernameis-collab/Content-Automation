# STATE

Updated: 2026-09-13T00:25:00Z (Run 105)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + write-path + words.py band + idea-lock INFO + writer band-landing + template draft.md save target** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- idea_brief reprints only; never writes idea.md
- idea_brief --queue ID reprints the paste from topic_queue without a videos/ folder
- PATH/draft.md is not script.md until apply --write
- Run 105: added `videos/_template/draft.md` so `new_packet` copies a save target with the spoken_words comment and empty beat skeleton. Did **not** touch needed.py, WAVE 3, doctor mapping, which_contract.MAP, writer prompts, or idea_brief.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 105)
- videos/_template/draft.md (empty WORDS + spoken_words comment; not script.md)
- prompts/script_writer.md Band landing table still in force (untouched this run)
- prompts/script_expander.md still points at that allocation (untouched this run)
- tools/idea_lock.py still available as an optional extra CLI
- apply_script.py still owns idea_lock_notes()
- words.py still prints idea-lock INFO and still owns the official count
- No new packet folder; queue still queued
- Reconstruct-loop watch from Runs 099–103 remains in force

## Pipeline map
Before scaffold: `python3 tools/doctor.py` (no path) prints fixture health then `Queue next` with `idea_brief.py --queue Q1`. `python3 tools/queue_status.py` / `python3 tools/next_topic.py` print the same `--queue` line.
Clone-less reconstruct: `python3 tools/needed.py --plan` WAVE 3 reconstructs queue_status then doctor.py, then runs doctor / queue_status / next_topic.
After scaffold: idea_brief --block / paste / --check / expand_prompt / overwrite PATH/draft.md (template copy is empty) / `words.py PATH` / apply dry-run / `--write --refresh` / set_status ready_for_vo if WORDS in band.
Off-repo writer must follow `prompts/script_writer.md` Band landing before the human runs words.py.
`idea_lock.py PATH` is optional once words.py prints the notes.
After a high-risk GitHub write: `python3 tools/prove_locks.py`.
Start of session: `python3 tools/doctor.py` then `python3 tools/queue_status.py` then `python3 tools/next_topic.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 70 | 69 | scaffold now copies the draft save target |
| Automated steps | 84 | 84 | no new CLI |
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
- Do not print --queue for a mark-needed row
- Do not print Queue next when doctor is given a single packet path
- Do not wrap doctor in start.py
- Do not add WAVE 4
- Do not list doctor internals inside --plan WAVE 3
- Do not add next_topic.py to which_contract.MAP need list
- Reconstruct-loop watch: Runs 099–103 touched needed.py reconstruct. Runs 104–105 did not. Next run must not add another reconstruct path unless a READY lie is proven.
- Do not rewrite writer prompts again unless the first real draft misses the 900–1500 band.
- Do not add a second draft template or a CLI that reprints Band landing.
