# STATE

Updated: 2026-09-10T14:20:00Z (Run 050)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + scaffold handoff + contract router + router lock + reconstruct list + reconstruct presence check + first-fetch bootstrap + fetch-wave plan + post-reconstruct operator command + operator reconstruct command + operator page with first-video expand/apply/status + Q1 title/path pin + idea.md pre-expand edit + scaffold idea reprint + expand_prompt blank-mechanism refuse + next_action fill-idea before expand + idea-gate contract + operator-pin contract + Q1 problem-line pin** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured
- HTTPS clone from this agent sandbox still fails (private repo). Push via GitHub file API.
- Reconstruct + selftest path: `docs/agent_session.md`
- Operator path: `docs/human_session.md` pins Q1 title `Stop deciding what to work on every morning`, predicted folder `videos/002-stop-deciding-what-to-work-on-every-morning`, idea.md problem/mechanism edit before expand_prompt, and notes that `new_packet` reprints topic + mechanism
- Operator pin lock: `python3 tools/operator_pin_contract.py` (unmapped; not a reconstruct wave). Also locks the Q1 problem line that is not a queue column.
- First fetch: `python3 tools/needed.py --bootstrap`
- Fetch waves: `python3 tools/needed.py --plan`
- Reconstruct file list: `python3 tools/needed.py CONTRACT`
- Reconstruct presence: `python3 tools/needed.py CONTRACT --missing` (exit 0 even if NOT READY)
- expand_prompt exits 2 when idea.md mechanism is blank / template-default / generic / tbd / todo. It does not write idea.md.
- next_action code `fill-idea` when that mechanism is blank. hint maps it to a paste comment + doctor, not expand_prompt.
- idea-gate lock: `python3 tools/idea_gate_contract.py` (tempfile; unmapped in which_contract; not a sixth reconstruct wave)

## What exists now (after Run 050)
- Same inventory as Run 049
- `operator_pin_contract.py` now also requires the Q1 problem sentence on `docs/human_session.md`
- `docs/agent_session.md` lists the two unmapped locks (`idea_gate_contract.py`, `operator_pin_contract.py`) so clone-less agents do not scan NEXT for them
- No new packet folder this run; queue still queued
- No needed.py edit this run
- which_contract / router_contract not edited (idea_gate and operator_pin stay unmapped)

## Pipeline map
Unchanged from Run 037. Operator pin now fails if the idea.md problem paste line disappears from human_session while Q1 is queued.

## Metrics snapshot
| Metric                      | Previous | Current    | Notes |
|-----------------------------|----------|------------|-------|
| Estimated human min / video | 125      | 124        | problem line no longer a free-floating paste string |
| Automated steps             | 42       | 42         | same contract, one more locked string; no new reconstruct flag |
| Videos produced             | 0        | 0          | fixture only |
| Reconstruct list runtime    | PASS 042 | unchanged  | needed.py not edited |
| Scaffold contract           | PASS 046 | unchanged  | not re-run |
| Idea gate contract          | PASS 048 | unchanged  | not re-run |
| Operator pin contract       | PASS 049 | PASS 050   | problem line added; local reconstruct PASS |

## Active constraints
- Do not auto-scaffold Q1
- Do not map needed.py / doctor.py / expand_prompt.py / idea_gate_contract.py / operator_pin_contract.py
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
- Do not treat idea_gate_contract or operator_pin_contract as permission to auto-write idea.md or scaffold Q1
- Do not add a problem column to topic_queue unless a human asks; lock the operator-page sentence instead
