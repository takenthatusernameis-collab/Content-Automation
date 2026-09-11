# STATE

Updated: 2026-09-11T09:15:00Z (Run 068)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + write_path_contract body + contract_shape lock** -> automated -> self-improving

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
- contract_shape.py is a separate file that fails if write_path_contract.py is missing, under 8000 bytes, or lacks def main / subprocess / PASS printer / in-band markers

## What exists now (after Run 068)
- tools/contract_shape.py added
- write_path_contract.py not edited this run (body already restored)
- Frozen doctor/hint/needed/which_contract/router/idea_brief/apply_script/set_status not edited
- No new packet folder; queue still queued
- idea_gate / operator_pin / idea_brief_contract stay unmapped

## Pipeline map
After scaffold: --block / paste / --check / expand off-repo / save draft.md / apply dry-run / --write --refresh / set_status ready_for_vo if WORDS in band.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 107 | 106 | empty lock file can no longer hide behind its own PASS printer |
| Automated steps | 58 | 59 | contract_shape.py |
| Videos produced | 0 | 0 | fixture only |
| Write-path contract | body+lock 067 | body + separate shape lock 068 | run contract_shape.py before trusting write_path_contract.py |

## Active constraints
- Do not auto-scaffold Q1
- Do not map needed.py / doctor.py / expand_prompt.py / idea_gate_contract.py / operator_pin_contract.py / idea_brief_contract.py
- Do not add WAVE 4 unless a new post-WAVE-3 guess is observed
- Do not retry HTTPS clone after one failure
- Do not write idea.md from new_packet or idea_brief
- Do not treat draft.md as script.md
- Do not weaken write_path_contract CLI locks including in-band set_status
- Do not replace write_path_contract.py with a docstring-only file
- Do not drop tools/contract_shape.py
