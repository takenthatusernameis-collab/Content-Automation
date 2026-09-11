# STATE

Updated: 2026-09-11T02:10:00Z (Run 061)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + scaffold handoff + contract router + router lock + reconstruct list + reconstruct presence check + first-fetch bootstrap + fetch-wave plan + post-reconstruct operator command + operator reconstruct command + operator page with first-video expand/apply/status + Q1 title/path pin + idea.md pre-expand edit + scaffold idea reprint (topic + problem + mechanism) + expand_prompt blank-mechanism refuse + next_action fill-idea before expand + idea-gate contract + operator-pin contract + Q1 problem-line pin + idea_brief reprint recover + idea-brief contract + idea_brief --block paste body + idea_brief --check paste confirm + --check PASTE READY prints expand_prompt + apply_script dry-run --from PATH/draft.md + --check PASTE INCOMPLETE prints --block + default idea_brief reprint prints exact --check + apply_script missing --from exits 2 with draft.md hint** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured
- HTTPS clone from this agent sandbox still fails (private repo). Push via GitHub file API.
- Reconstruct + selftest path: `docs/agent_session.md`
- Operator path: `docs/human_session.md` pins Q1 title `Stop deciding what to work on every morning`, predicted folder `videos/002-stop-deciding-what-to-work-on-every-morning`
- After scaffold stdout is gone: `python3 tools/idea_brief.py PATH` reprints current vs suggested idea fields and prints the exact `--block` and `--check` commands for that folder. `--block` prints only the paste-ready idea.md body. `--check` compares current idea.md to that body (exit 2 incomplete and prints `python3 tools/idea_brief.py PATH --block`, exit 0 PASTE READY and prints `python3 tools/expand_prompt.py PATH` then dry-run `python3 tools/apply_script.py PATH --from PATH/draft.md`). None of those flags write idea.md.
- After editing idea_brief: `python3 tools/idea_brief_contract.py` (unmapped; tempfile).
- Operator pin lock: `python3 tools/operator_pin_contract.py` (unmapped).
- First fetch: `python3 tools/needed.py --bootstrap`
- Fetch waves: `python3 tools/needed.py --plan`
- Reconstruct file list: `python3 tools/needed.py CONTRACT`
- Reconstruct presence: `python3 tools/needed.py CONTRACT --missing` (exit 0 even if NOT READY)
- expand_prompt exits 2 when idea.md mechanism is blank / template-default. It does not write idea.md.
- next_action code `fill-idea` when that mechanism is blank.
- idea-gate lock: `python3 tools/idea_gate_contract.py` (unmapped)
- new_packet idea_followup reprints Q1 problem from `operator_pin_contract.Q1_PROBLEM` and still does not write idea.md
- Off-repo expand draft convention: save to `PATH/draft.md`, then dry-run apply_script `--from PATH/draft.md`. That file is not script.md until `--write`.
- If that `--from` path is missing, apply_script exits 2 and prints a draft.md hint instead of a traceback. It still does not write script.md.

## What exists now (after Run 061)
- Same inventory as Run 060 plus apply_script missing-source guard
- write_path_contract locks missing --from messaging and load_source exit 2
- Frozen doctor/hint/needed/which_contract/router/idea_brief not edited
- No new packet folder; queue still queued
- idea_gate / operator_pin / idea_brief_contract stay unmapped

## Pipeline map
Unchanged from Run 037. After scaffold, paste from `--block`, confirm with `--check`, then run the printed expand_prompt off-repo, save to PATH/draft.md, then the printed apply_script dry-run. If draft.md is not there yet, apply_script exits 2 with the save hint.

## Metrics snapshot
| Metric                      | Previous | Current    | Notes |
|-----------------------------|----------|------------|-------|
| Estimated human min / video | 114      | 113        | missing --from no longer a traceback |
| Automated steps             | 51       | 52         | apply_script missing-source exit 2 |
| Videos produced             | 0        | 0          | fixture only |
| Write-path contract         | PASS 060 | partial 061 | helper locked; full contract not reconstructed this run |

## Active constraints
- Do not auto-scaffold Q1
- Do not map needed.py / doctor.py / expand_prompt.py / idea_gate_contract.py / operator_pin_contract.py / idea_brief_contract.py
- Do not add WAVE 4 unless a new post-WAVE-3 guess is observed
- Do not retry HTTPS clone after one failure
- new_packet must not write idea.md or mark the queue
- idea_brief must not write idea.md (including --block and --check)
- expand_prompt must not write idea.md or script.md
- Do not add a problem column to topic_queue unless a human asks
- Do not print --write from idea_brief --check
- Do not treat draft.md as script.md
- Do not add another idea_brief flag unless leftover labor remains after the printed draft.md apply dry-run
