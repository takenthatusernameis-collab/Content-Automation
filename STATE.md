# STATE

Updated: 2026-09-11T14:11:00Z (Run 073)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + write_path_contract body + contract_shape trio lock + verify_write_path order lock + words.py band + delta + hook delta** -> automated -> self-improving

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
- words.py is a read-only band printer. It prefers PATH/draft.md when present. It prints Delta (add/cut N), Hook Delta (20-35), and a Next line. It falls back to local counters if validate_packet.py is missing. --strict still keys off the total band only. It does not write and is not a lock. Do not map it in needed.py.

## What exists now (after Run 073)
- tools/words.py now prints Hook Delta for the 20-35 hook band
- write_path_contract.py / apply_script.py / set_status.py / contract_shape.py / verify_write_path.py not edited this run
- Frozen doctor/hint/needed/which_contract/router/idea_brief not edited
- No new packet folder; queue still queued
- idea_gate / operator_pin / idea_brief_contract stay unmapped

## Pipeline map
After scaffold: --block / paste / --check / expand off-repo / save draft.md / `words.py PATH` (read Result + Delta + Hook Delta) / apply dry-run / --write --refresh / set_status ready_for_vo if WORDS in band.
After reconstruct of write-path tools: `python3 tools/verify_write_path.py` (shape then contract).

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 102 | 101 | hook add/cut printed so expand pass has a number |
| Automated steps | 63 | 64 | words.py Hook Delta |
| Videos produced | 0 | 0 | fixture only |
| Write-path contract | body + trio + ordered verify 070 | unchanged 073 | run verify_write_path.py after reconstruct |

## Active constraints
- Do not auto-scaffold Q1
- Do not map needed.py / doctor.py / expand_prompt.py / idea_gate_contract.py / operator_pin_contract.py / idea_brief_contract.py / words.py
- Do not add WAVE 4 unless a new post-WAVE-3 guess is observed
- Do not retry HTTPS clone after one failure
- Do not write idea.md from new_packet or idea_brief
- Do not treat draft.md as script.md
- Do not weaken write_path_contract CLI locks including in-band set_status
- Do not replace write_path_contract.py with a docstring-only file
- Do not drop tools/contract_shape.py or shrink it back to a single-file witness
- Do not drop tools/verify_write_path.py or treat it as a replacement for the two files it runs
- Do not treat words.py IN BAND as apply --write
- Do not treat words.py Delta or Hook Delta as permission to pad filler
- Do not make words.py --strict fail on hook alone
