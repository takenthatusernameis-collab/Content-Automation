# STATE

Updated: 2026-09-11T07:25:00Z (Run 066)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + scaffold handoff + contract router + router lock + reconstruct list + reconstruct presence check + first-fetch bootstrap + fetch-wave plan + post-reconstruct operator command + operator reconstruct command + operator page with first-video expand/apply/status + Q1 title/path pin + idea.md pre-expand edit + scaffold idea reprint (topic + problem + mechanism) + expand_prompt blank-mechanism refuse + next_action fill-idea before expand + idea-gate contract + operator-pin contract + Q1 problem-line pin + idea_brief reprint recover + idea-brief contract + idea_brief --block paste body + idea_brief --check paste confirm + --check PASTE READY prints expand_prompt + apply_script dry-run --from PATH/draft.md + --check PASTE INCOMPLETE prints --block + default idea_brief reprint prints exact --check + apply_script missing --from exits 2 with draft.md hint + write_path_contract locks missing --from CLI exit 2 + write_path_contract locks dry-run --from existing draft.md (no script.md write) + write_path_contract locks set_status CLI ready_for_vo duration/fixture block (no packet.md write, including blocked --write) + write_path_contract locks apply_script CLI --write fixture refuse (no script.md write) + write_path_contract locks advertised non-fixture apply CLI (--refresh without --write is a no-op; --write replaces script.md only; --write --refresh replaces script.md and refreshes expand/vo_session/captions; packet.md stays draft)** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured
- HTTPS clone from this agent sandbox still fails (private repo). Push via GitHub file API.
- Reconstruct + selftest path: `docs/agent_session.md`
- Operator path: `docs/human_session.md` pins Q1 title `Stop deciding what to work on every morning`, predicted folder `videos/002-stop-deciding-what-to-work-on-every-morning`
- After scaffold stdout is gone: `python3 tools/idea_brief.py PATH` reprints current vs suggested idea fields and prints the exact `--block` and `--check` commands for that folder. `--block` prints only the paste-ready idea.md body. `--check` compares current idea.md to that body (exit 2 incomplete and prints `python3 tools/idea_brief.py PATH --block`, exit 0 PASTE READY and prints `python3 tools/expand_prompt.py PATH` then dry-run `python3 tools/apply_script.py PATH --from PATH/draft.md`). None of those flags write idea.md.
- Off-repo expand draft convention: save to `PATH/draft.md`, then dry-run apply_script `--from PATH/draft.md`. That file is not script.md until `--write`.
- write_path_contract subprocess-runs missing `--from` (exit 2), existing `PATH/draft.md` dry-run (exit 0, script.md unchanged), set_status ready_for_vo blocked CLI (exit 1, packet.md unchanged), apply_script `--write --from` against the fixture (exit 1, script.md unchanged), `--refresh` without `--write` (exit 0, no writes), non-fixture `--write` (script.md replaced, derived files untouched), and non-fixture `--write --refresh` (script.md + expand/vo_session/captions refreshed, packet.md still draft).

## What exists now (after Run 066)
- Same inventory as Run 065 plus write_path_contract CLI lock on advertised non-fixture apply --write / --refresh
- WRITE PATH CONTRACT PASS on a reconstructed tools tree (tempfile + subprocess; no videos/ leak)
- Frozen doctor/hint/needed/which_contract/router/idea_brief/apply_script/set_status not edited
- No new packet folder; queue still queued
- idea_gate / operator_pin / idea_brief_contract stay unmapped

## Pipeline map
Unchanged from Run 037. After scaffold, paste from `--block`, confirm with `--check`, then run the printed expand_prompt off-repo, save to PATH/draft.md, then the printed apply_script dry-run. If draft.md is not there yet, apply_script exits 2 with the save hint. If draft.md is there, dry-run prints OK / Dry-run only and does not write script.md. `--refresh` without `--write` also stays dry-run. `--write` on sample-001 exits 1 and leaves script.md unchanged. After apply dry-run OK on a non-fixture packet, `python3 tools/apply_script.py PATH --from PATH/draft.md --write --refresh` writes script.md and refreshes expand/vo_session/captions without bumping status. Only then, if WORDS sit in band, `python3 tools/set_status.py PATH --to ready_for_vo` (dry-run first). If WORDS are short, that CLI exits 1 and leaves packet.md draft even with `--write`.

## Metrics snapshot
| Metric                      | Previous | Current    | Notes |
|-----------------------------|----------|------------|-------|
| Estimated human min / video | 109      | 108        | advertised --write --refresh cannot silently no-op or refresh without write |
| Automated steps             | 56       | 57         | write_path_contract non-fixture apply --write / --refresh CLI lock |
| Videos produced             | 0        | 0          | fixture only |
| Write-path contract         | PASS 065 | PASS 066   | apply dry-run + set_status blocked + apply fixture --write + live --write/--refresh |

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
- Do not turn a missing --from path into a Python traceback; exit 2 with the draft.md hint
- Do not weaken the write_path_contract CLI missing --from lock
- Do not weaken the write_path_contract CLI dry-run existing draft.md lock (exit 0, no script.md write)
- Do not weaken the write_path_contract CLI set_status ready_for_vo duration/fixture lock (exit 1, no packet.md write)
- Do not weaken the write_path_contract CLI apply_script --write fixture lock (exit 1, no script.md write)
- Do not weaken the write_path_contract CLI --refresh-without-write no-op lock
- Do not weaken the write_path_contract CLI non-fixture --write script-only lock
- Do not weaken the write_path_contract CLI non-fixture --write --refresh derived lock
