# STATE

Updated: 2026-09-13T05:05:00Z (Run 110)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + write-path + words.py band + idea-lock INFO + writer band-landing + template draft.md + new_packet draft overwrite reprint + empty-heading expand budget + live expand_prompt budget on stub expand.md + human_session empty-script Target column + hint expand-script Target comment** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- idea_brief reprints only; never writes idea.md
- PATH/draft.md is not script.md until apply --write
- Run 110: `tools/hint.py` write-script/expand-script Command now includes the empty-draft Target comment (hook 28 / payoff 60 / beats 220x4 / CTA 50 / land ~1010). Doctor prints those same commands; doctor.py itself was not mapped or edited. Did **not** scaffold Q1. Did **not** touch needed.py, WAVE 3, which_contract.MAP, writer prompts, idea_brief, new_packet, expand_prompt, expand_brief, or human_session.
- words.py / words_contract / placeholder_guard / prove_locks stay unmapped.

## What exists now (after Run 110)
- hint/doctor Command for expand-script names the same Target numbers human_session already names
- Human expand step names hook 28 / payoff 60 / beats 220x4 / CTA 50 / land ~1010
- videos/_template/expand.md includes those targets while Status stays placeholder
- expand_prompt uses a live budget when expand_is_filled is false
- videos/_template/draft.md (empty WORDS + spoken_words comment; not script.md)
- new_packet prints draft overwrite path; does not write WORDS
- prompts/script_writer.md Band landing table still in force (untouched this run)
- No new packet folder; queue still queued
- Reconstruct-loop watch from Runs 099-103 remains in force

## Pipeline map
Before scaffold: `python3 tools/doctor.py` then `python3 tools/queue_status.py` then `python3 tools/next_topic.py`.
After scaffold: idea_brief --block / paste / --check / expand_prompt / overwrite PATH/draft.md / `words.py PATH` / apply dry-run / `--write --refresh` / set_status ready_for_vo if WORDS in band.
Off-repo writer must follow `prompts/script_writer.md` Band landing. expand.md, expand_prompt, human_session, and hint Command now show the same per-heading targets on an empty script.
After a high-risk GitHub write: `python3 tools/prove_locks.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 65 | 64 | doctor/hint Command names Target; no extra page |
| Automated steps | 84 | 84 | no new CLI |
| Videos produced | 0 | 0 | fixture only |

## Active constraints
- Do not auto-scaffold Q1
- Do not map idea_lock.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py / needed.py / idea_brief.py / idea_brief_contract.py / doctor.py
- Do not make idea-lock INFO a BLOCKED error or --strict FAIL
- Do not treat draft.md as script.md
- Do not write idea.md from idea_brief
- Do not retry HTTPS clone as the first action
- Do not add another wrapper CLI around idea_lock_notes
- Do not add another idea_brief flag unless --queue regresses
- Do not add WAVE 4
- Reconstruct-loop watch: Runs 099-103 touched needed.py reconstruct. Runs 104-110 did not. Next run must not add another reconstruct path unless a READY lie is proven.
- Do not rewrite writer prompts again unless the first real draft misses the 900-1500 band.
- Do not add a second draft template or a CLI that reprints Band landing.
- Do not add a fourth new_packet followup unless the draft overwrite reprint regresses.
- Do not hide the empty-WORDS expand budget table again.
- Do not make expand_prompt write expand.md.
- Do not strip the Target column from docs/human_session.md step 3.
- Do not strip the Target comment from hint.py write-script/expand-script commands.
