# STATE

Updated: 2026-09-12T07:10:00Z (Run 088)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + write_path_contract body + contract_shape trio lock + verify_write_path order lock + words.py band + delta + hook delta + beats/thin + grow + cut + words_contract + placeholder_guard (includes prove_locks.py) + prove_locks order wrapper + NEXT_RUN_PROMPT names prove_locks first + hint.py prints idea_brief and words.py + next_action/doctor Why names idea_brief --block/--check + queue_status/next_topic print idea_brief after folder exists + human_session start names those idea_brief lines + agent_session WAVE 3 board names those idea_brief lines + README start path names those idea_brief lines and prove_locks + production_rules handoff names those idea_brief lines, words.py, and prove_locks** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured
- HTTPS clone from this agent sandbox still fails (private repo). Push via GitHub file API.
- Reconstruct + selftest path: `docs/agent_session.md`
- Operator path: `docs/human_session.md` pins Q1 title `Stop deciding what to work on every morning`, predicted folder `videos/002-stop-deciding-what-to-work-on-every-morning`
- idea_brief reprints only; never writes idea.md
- Off-repo expand draft convention: PATH/draft.md is not script.md until apply --write
- write_path_contract has a real main() (restored Run 067)
- contract_shape.py witnesses write_path_contract.py, apply_script.py, and set_status.py (size + markers). It does not import them and writes nothing.
- verify_write_path.py subprocess-runs contract_shape.py then write_path_contract.py. It writes nothing. It is not a substitute for those two files.
- words.py is a read-only band printer. It prefers PATH/draft.md when present. It prints Delta, Hook Delta, Beats, Thin, Grow, Cut, and a Next line. --strict keys off the total band only. Do not map it in needed.py.
- words_contract.py is an unmapped lock for words.py. Writes nothing under videos/. Do not map it in needed.py.
- placeholder_guard.py is an unmapped lock for emptied or placeholder bodies across the high-risk tool set. Size floor + markers + empty-body check. Writes nothing. Do not map it in needed.py.
- prove_locks.py is an unmapped order wrapper. It subprocess-runs placeholder_guard.py, then words_contract.py, then verify_write_path.py. Stops on first non-zero. Writes nothing. Do not map it in needed.py.
- NEXT_RUN_PROMPT.md names prove_locks.py as the first post-write command (Run 080). The three inner commands stay valid only as fallback.
- hint.py is a read-only command printer. Run 082 made fill-idea print idea_brief reprint/--block/--check and write-script/expand-script print words.py plus PATH/draft.md apply lines. It writes nothing. It is not a lock.
- next_action.py Why for fill-idea names idea_brief --block / paste / --check. doctor.py and hint.py reprint that Why. It writes nothing.
- queue_status.py is a read-only board. Run 084 prints idea_brief --block / paste / --check under mark-needed folders. It still writes nothing. It is not a lock.
- next_topic.py is a read-only next-row printer. Run 084 prints idea_brief --block / paste / --check after the predicted folder. It still writes nothing. It is not a lock.
- docs/human_session.md start-of-session section names those same idea_brief lines (Run 085). It is the human page, not a lock.
- docs/agent_session.md WAVE 3 board paragraph names those same idea_brief lines (Run 086). It is the clone-less agent page, not a lock.
- README.md Human session and Local tools now name idea_brief --block / paste / --check after a mark-needed folder and prove_locks after a high-risk write (Run 087). It is the GitHub front door, not a lock.
- docs/production_rules.md Packet + Script + Human handoff now name idea_brief --block / paste / --check, words.py on PATH/draft.md, and prove_locks after a high-risk write (Run 088). It is the packet contract page, not a lock.

## What exists now (after Run 088)
- production_rules Packet, Script, and Human handoff name idea_brief.py --block / --check, words.py, and prove_locks.py
- Isolated check: production_rules contains idea_brief.py, --block, --check, words.py, draft.md, and prove_locks.py in Human handoff, not only buried in later tool lists
- Frozen doctor/needed/which_contract/router/idea_brief/words/prove_locks/placeholder_guard/hint/next_action/queue_status/next_topic/human_session/agent_session/README command lists not edited this run
- No new packet folder; queue still queued
- idea_gate / operator_pin / idea_brief_contract / words_contract / placeholder_guard / prove_locks stay unmapped

## Pipeline map
After scaffold: idea_brief --block / paste / --check / expand off-repo / save draft.md / `words.py PATH` / apply dry-run / --write --refresh / set_status ready_for_vo if WORDS in band.
After a GitHub write of any high-risk tool: `python3 tools/prove_locks.py`.
Start of session: `python3 tools/queue_status.py` then `python3 tools/next_topic.py`. After a mark-needed folder exists, those printers name idea_brief --block/--check. `docs/human_session.md` start section says the same. `docs/agent_session.md` WAVE 3 board paragraph says the same. README Human session now says the same. `docs/production_rules.md` Human handoff now says the same. After scaffold on a live packet, `python3 tools/hint.py PATH` still prints idea_brief and words.py lines; `python3 tools/next_action.py PATH` Why still names idea_brief --block/--check.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 87 | 86 | production_rules no longer omits idea_brief after a folder exists |
| Automated steps | 71 | 71 | no new lock; packet contract now matches the printers |
| Videos produced | 0 | 0 | fixture only |
| Write-path contract | body + trio + ordered verify 070 | unchanged 088 | run prove_locks.py after a high-risk GitHub write |

## Active constraints
- Do not auto-scaffold Q1
- Do not map needed.py / doctor.py / expand_prompt.py / idea_gate_contract.py / operator_pin_contract.py / idea_brief_contract.py / words.py / words_contract.py / placeholder_guard.py / prove_locks.py
- Do not add WAVE 4 unless a new post-WAVE-3 guess is observed
- Do not retry HTTPS clone after one failure
- Do not write idea.md from new_packet or idea_brief
- Do not treat draft.md as script.md
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
- Do not strip idea_brief --block/--check from queue_status mark-needed follow-up or next_topic after-folder lines
- Do not strip idea_brief --block/--check from docs/human_session.md start-of-session text
- Do not strip idea_brief --block/--check from docs/agent_session.md WAVE 3 board paragraph
- Do not strip idea_brief --block/--check or prove_locks.py from README Human session text
- Do not strip idea_brief --block/--check, words.py, or prove_locks.py from docs/production_rules.md Packet / Script / Human handoff text
