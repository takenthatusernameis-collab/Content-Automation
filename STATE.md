# STATE

Updated: 2026-09-10T12:20:00Z (Run 048)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + scaffold handoff + contract router + router lock + reconstruct list + reconstruct presence check + first-fetch bootstrap + fetch-wave plan + post-reconstruct operator command + operator reconstruct command + operator page with first-video expand/apply/status + Q1 title/path pin + idea.md pre-expand edit + scaffold idea reprint + expand_prompt blank-mechanism refuse + next_action fill-idea before expand + idea-gate contract** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured
- HTTPS clone from this agent sandbox still fails (private repo). Push via GitHub file API.
- Reconstruct + selftest path: `docs/agent_session.md`
- Operator path: `docs/human_session.md` pins Q1 title `Stop deciding what to work on every morning`, predicted folder `videos/002-stop-deciding-what-to-work-on-every-morning`, idea.md edit before expand_prompt, and notes that `new_packet` reprints topic + mechanism
- First fetch: `python3 tools/needed.py --bootstrap`
- Fetch waves: `python3 tools/needed.py --plan`
- Reconstruct file list: `python3 tools/needed.py CONTRACT`
- Reconstruct presence: `python3 tools/needed.py CONTRACT --missing` (exit 0 even if NOT READY)
- expand_prompt exits 2 when idea.md mechanism is blank / template-default / generic / tbd / todo. It does not write idea.md.
- next_action code `fill-idea` when that mechanism is blank. hint maps it to a paste comment + doctor, not expand_prompt.
- idea-gate lock: `python3 tools/idea_gate_contract.py` (tempfile; unmapped in which_contract; not a sixth reconstruct wave)

## What exists now (after Run 048)
- Operating memory files and frozen original master prompt
- Video packet standard + scaffold CLI + packet QA
- Sample packet fixture `videos/sample-001-why-systems-beat-motivation/`
- Topic queue + queue_lib + next_topic + queue_status + mark_topic
- Contracts: queue, write-path, scaffold, which_contract, router_contract, idea_gate_contract
- Reconstruct list `tools/needed.py` (read-only; unmapped like doctor)
- needed.py --missing / --bootstrap / --plan unchanged from Run 042
- Reconstruct-loop (Runs 037-042) flagged in FAILURES.md
- `new_packet.idea_followup` reprints topic + queue one_line mechanism; does not write idea.md
- `expand_prompt.py` refuses blank mechanism (exit 2)
- `scaffold_contract.py` locks idea_followup reprint + no idea.md write
- `next_action.py` returns `fill-idea` before write-script / expand-script when idea.md mechanism is blank
- `hint.py` maps `fill-idea` (no expand_prompt live command; first live command is doctor)
- `idea_gate_contract.py` locks the blank/filled mechanism cases + fill-idea hint map on tempfile
- No new packet folder this run; queue still queued
- No needed.py edit this run
- which_contract / router_contract not edited (idea_gate stays unmapped)

## Pipeline map
Unchanged from Run 037. Oversight now includes needed.py --plan WAVE 3 reconstruct + operator lines. Operator page no longer defers expand/apply/status and no longer leaves Q1 title/path as a guess. Scaffold reprint now includes idea.md fields. expand_prompt will not emit a pack until those fields are pasted. doctor/hint will not lead with expand_prompt while the mechanism is still blank. idea_gate_contract fails the run if that map regresses.

## Metrics snapshot
| Metric                      | Previous | Current    | Notes |
|-----------------------------|----------|------------|-------|
| Estimated human min / video | 127      | 126        | fill-idea map locked so later runs cannot silently restore expand-first |
| Automated steps             | 40       | 41         | idea_gate_contract added; no new reconstruct flag |
| Videos produced             | 0        | 0          | fixture only |
| Reconstruct list runtime    | PASS 042 | unchanged  | needed.py not edited |
| Scaffold contract           | PASS 046 | unchanged  | not re-run |
| Idea gate contract          | unit 047 | PASS 048   | tempfile + source locks |

## Active constraints
- Do not auto-scaffold Q1
- Do not map needed.py / doctor.py / expand_prompt.py / idea_gate_contract.py
- needed.py --missing, --bootstrap, and --plan must exit 0
- Do not treat --bootstrap or --plan as a sixth contract
- Do not grow BOOTSTRAP or WAVE 2/3 into a full-repo dump
- WAVE 3 stays commands only: reconstruct line + operator line; not a queue file list
- Do not add WAVE 4 unless a new post-WAVE-3 guess is observed
- FALLBACK_ALIAS must match which_contract.MAP tool lists
- Do not retry HTTPS clone after one failure
- No secrets, ffmpeg recipe, TTS, or YouTube API
- new_packet must not write idea.md or mark the queue
- expand_prompt must not write idea.md or script.md
- next_action/hint must not print expand_prompt as the first live command while idea.md mechanism is blank
- Do not treat idea_gate_contract as permission to auto-write idea.md
