# STATE

Updated: 2026-09-12T09:16:00Z (Run 090)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + write_path_contract body + contract_shape trio lock + verify_write_path order lock + words.py band + delta + hook delta + beats/thin + grow + cut + words_contract + placeholder_guard (includes prove_locks.py) + prove_locks order wrapper + NEXT_RUN_PROMPT names prove_locks first + hint.py prints idea_brief and words.py + next_action/doctor Why names idea_brief --block/--check + queue_status/next_topic print idea_brief after folder exists + human_session / agent_session / README / production_rules name those lines + idea_brief --block fills the whole idea.md template + expand_prompt prints Idea locks from idea.md** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured
- HTTPS clone from this agent sandbox still fails (private repo). Push via GitHub file API.
- Reconstruct + selftest path: `docs/agent_session.md`
- Operator path: `docs/human_session.md` pins Q1 title `Stop deciding what to work on every morning`, predicted folder `videos/002-stop-deciding-what-to-work-on-every-morning`
- idea_brief reprints only; never writes idea.md
- Run 089: `--block` pastes topic, viewer, problem, mechanism, why now, and related. `--check` still gates only topic / problem / mechanism. Extra blanks print INFO, not FAIL.
- Run 090: expand_prompt.py prints parsed Idea locks and refuses with idea_brief --block/--check. Still does not write script.md. prompts/script_expander.md follows draft.md + words.py.
- Off-repo expand draft convention: PATH/draft.md is not script.md until apply --write
- write_path_contract has a real main() (restored Run 067)
- contract_shape.py witnesses write_path_contract.py, apply_script.py, and set_status.py
- verify_write_path.py subprocess-runs contract_shape.py then write_path_contract.py
- words.py is a read-only band printer. Do not map it in needed.py.
- words_contract.py / placeholder_guard.py / prove_locks.py stay unmapped. Do not map them in needed.py.
- NEXT_RUN_PROMPT.md names prove_locks.py as the first post-write command (Run 080).
- hint.py / next_action.py / queue_status.py / next_topic.py / human_session / agent_session / README / production_rules already name idea_brief after a folder exists (Runs 082–088). Do not spend the next run aligning another page to the same three lines.

## What exists now (after Run 090)
- expand_prompt.py committed at 8111 bytes with idea_locks() and refuse text that names idea_brief
- idea_brief --block still prints a complete idea.md body
- Isolated check: committed expand_prompt.py contains "Idea locks", "idea_brief.py", and PATH/draft.md apply lines
- Frozen doctor/needed/which_contract/router/idea_brief_contract/words/prove_locks/placeholder_guard/hint/next_action/queue_status/next_topic command lists not edited this run
- No new packet folder; queue still queued
- idea_gate / operator_pin / idea_brief_contract / words_contract / placeholder_guard / prove_locks stay unmapped

## Pipeline map
After scaffold: idea_brief --block / paste / --check / expand_prompt (now carries Idea locks) / save draft.md / `words.py PATH` / apply dry-run / `--write --refresh` / set_status ready_for_vo if WORDS in band.
After a GitHub write of any high-risk tool: `python3 tools/prove_locks.py`.
Start of session: `python3 tools/queue_status.py` then `python3 tools/next_topic.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 85 | 84 | expand writer is given parsed idea locks instead of a raw blob |
| Automated steps | 71 | 71 | no new lock file; assembler grew |
| Videos produced | 0 | 0 | fixture only |
| Write-path contract | body + trio + ordered verify 070 | unchanged 090 | run prove_locks.py after a high-risk GitHub write |

## Active constraints
- Do not auto-scaffold Q1
- Do not map needed.py / doctor.py / expand_prompt.py / idea_gate_contract.py / operator_pin_contract.py / idea_brief_contract.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py
- Do not add WAVE 4 unless a new post-WAVE-3 guess is observed
- Do not retry HTTPS clone after one failure
- Do not write idea.md from new_packet or idea_brief
- Do not treat draft.md as script.md
- Do not make --check FAIL on blank viewer / why now / related
- Do not spend the next run aligning another markdown page to name idea_brief --block/--check
- Do not drop the Idea locks section from expand_prompt.py
- Do not revert expand_prompt refuse text to "Paste the new_packet reprint"
- Do not weaken write_path_contract CLI locks including in-band set_status
- Do not replace write_path_contract.py with a docstring-only file
- Do not drop tools/contract_shape.py or shrink it back to a single-file witness
- Do not drop tools/verify_write_path.py or treat it as a replacement for those two files
- Do not treat words.py IN BAND as apply --write
- Do not treat words.py Delta, Hook Delta, Beats, Thin, Grow, or Cut as permission to pad filler
- Do not make words.py --strict fail on hook, thin headings, Grow, or Cut alone
- Do not treat words_contract PASS, PLACEHOLDER GUARD PASS, or PROVE LOCKS PASS as apply --write or as a Q1 scaffold
- Do not drop tools/placeholder_guard.py or drop the prove_locks.py check from it
- Do not drop tools/prove_locks.py or treat it as a replacement for the three files it runs
- Do not add another order wrapper around prove_locks.py
- Do not strip idea_brief or words.py lines from hint.py fill-idea / write-script / expand-script
- Do not revert next_action fill-idea Why to "paste the new_packet reprint"
- Do not strip idea_brief --block/--check from queue_status, next_topic, human_session, agent_session, README, or production_rules handoff
