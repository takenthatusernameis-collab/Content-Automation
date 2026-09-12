# STATE

Updated: 2026-09-12T00:21:00Z (Run 081)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + write_path_contract body + contract_shape trio lock + verify_write_path order lock + words.py band + delta + hook delta + beats/thin + grow + cut + words_contract + placeholder_guard (includes prove_locks.py) + prove_locks order wrapper + NEXT_RUN_PROMPT names prove_locks first** -> automated -> self-improving

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
- placeholder_guard.py is an unmapped lock for emptied or placeholder bodies across the high-risk tool set (words, words_contract, write-path trio, contract_shape, verify_write_path, prove_locks). Size floor + markers + empty-body check. Writes nothing. Do not map it in needed.py.
- prove_locks.py is an unmapped order wrapper. It subprocess-runs placeholder_guard.py, then words_contract.py, then verify_write_path.py. Stops on first non-zero. Writes nothing. Do not map it in needed.py.
- NEXT_RUN_PROMPT.md names prove_locks.py as the first post-write command (Run 080). The three inner commands stay valid only as fallback.

## What exists now (after Run 081)
- tools/placeholder_guard.py now also witnesses prove_locks.py (800-byte floor + PROVE LOCKS PASS + inner three names)
- Isolated sandbox: missing or 8-byte prove_locks.py FAIL exit 1
- Frozen doctor/hint/needed/which_contract/router/idea_brief/words/prove_locks not edited
- No new packet folder; queue still queued
- idea_gate / operator_pin / idea_brief_contract / words_contract / placeholder_guard / prove_locks stay unmapped

## Pipeline map
After scaffold: --block / paste / --check / expand off-repo / save draft.md / `words.py PATH` / apply dry-run / --write --refresh / set_status ready_for_vo if WORDS in band.
After a GitHub write of any high-risk tool: `python3 tools/prove_locks.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 94 | 93 | emptied prove_locks.py now fails in the first inner lock |
| Automated steps | 70 | 71 | placeholder_guard gained one sibling check; no new file |
| Videos produced | 0 | 0 | fixture only |
| Write-path contract | body + trio + ordered verify 070 | unchanged 081 | run prove_locks.py after a high-risk GitHub write |

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
