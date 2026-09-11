# STATE

Updated: 2026-09-11T08:10:00Z (Run 067)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + write_path_contract body restored + in-band set_status ready_for_vo lock** -> automated -> self-improving

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
- write_path_contract now has a real main() and locks missing --from, existing-draft dry-run, set_status blocked ready_for_vo, fixture apply --write, non-fixture apply --write/--refresh, and in-band set_status dry-run/--write

## What exists now (after Run 067)
- write_path_contract.py is executable again (was docstring-only after Run 066)
- Frozen doctor/hint/needed/which_contract/router/idea_brief/apply_script/set_status not edited
- No new packet folder; queue still queued
- idea_gate / operator_pin / idea_brief_contract stay unmapped

## Pipeline map
After scaffold: --block / paste / --check / expand off-repo / save draft.md / apply dry-run / --write --refresh / set_status ready_for_vo if WORDS in band.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 108 | 107 | in-band set_status cannot silently no-op or write on dry-run |
| Automated steps | 57 | 58 | contract body restored + in-band set_status lock |
| Videos produced | 0 | 0 | fixture only |
| Write-path contract | docstring 066 | body+lock 067 | do not treat STATE PASS as the file |

## Active constraints
- Do not auto-scaffold Q1
- Do not map needed.py / doctor.py / expand_prompt.py / idea_gate_contract.py / operator_pin_contract.py / idea_brief_contract.py
- Do not add WAVE 4 unless a new post-WAVE-3 guess is observed
- Do not retry HTTPS clone after one failure
- Do not write idea.md from new_packet or idea_brief
- Do not treat draft.md as script.md
- Do not weaken write_path_contract CLI locks including in-band set_status
- Do not replace write_path_contract.py with a docstring-only file
