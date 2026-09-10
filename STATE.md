# STATE

Updated: 2026-09-10T19:10:00Z (Run 054)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + scaffold handoff + contract router + router lock + reconstruct list + reconstruct presence check + first-fetch bootstrap + fetch-wave plan + post-reconstruct operator command + operator reconstruct command + operator page with first-video expand/apply/status + Q1 title/path pin + idea.md pre-expand edit + scaffold idea reprint (topic + problem + mechanism) + expand_prompt blank-mechanism refuse + next_action fill-idea before expand + idea-gate contract + operator-pin contract + Q1 problem-line pin + idea_brief reprint recover + idea-brief contract + idea_brief --block paste body** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured
- HTTPS clone from this agent sandbox still fails (private repo). Push via GitHub file API.
- Reconstruct + selftest path: `docs/agent_session.md`
- Operator path: `docs/human_session.md` pins Q1 title `Stop deciding what to work on every morning`, predicted folder `videos/002-stop-deciding-what-to-work-on-every-morning`, idea.md problem/mechanism edit before expand_prompt, and notes that `new_packet` reprints topic + problem + mechanism
- After scaffold stdout is gone: `python3 tools/idea_brief.py PATH` reprints current vs suggested idea fields. `--block` prints only the paste-ready idea.md body. Neither writes idea.md.
- After editing idea_brief or its operator mention: `python3 tools/idea_brief_contract.py` (unmapped; tempfile; not a reconstruct wave).
- Operator pin lock: `python3 tools/operator_pin_contract.py` (unmapped; not a reconstruct wave). Also locks the Q1 problem line that is not a queue column.
- First fetch: `python3 tools/needed.py --bootstrap`
- Fetch waves: `python3 tools/needed.py --plan`
- Reconstruct file list: `python3 tools/needed.py CONTRACT`
- Reconstruct presence: `python3 tools/needed.py CONTRACT --missing` (exit 0 even if NOT READY)
- expand_prompt exits 2 when idea.md mechanism is blank / template-default / generic / tbd / todo. It does not write idea.md.
- next_action code `fill-idea` when that mechanism is blank. hint maps it to a paste comment + doctor, not expand_prompt.
- idea-gate lock: `python3 tools/idea_gate_contract.py` (tempfile; unmapped in which_contract; not a sixth reconstruct wave)
- new_packet idea_followup reprints Q1 problem from `operator_pin_contract.Q1_PROBLEM` and still does not write idea.md

## What exists now (after Run 054)
- Same inventory as Run 053 plus `idea_brief.py --block`
- Frozen doctor/hint/needed/which_contract/router not edited
- No new packet folder; queue still queued
- idea_gate / operator_pin / idea_brief_contract stay unmapped

## Pipeline map
Unchanged from Run 037. After scaffold, the human can paste topic + problem + mechanism from new_packet stdout, recover with idea_brief, or copy the `--block` body.

## Metrics snapshot
| Metric                      | Previous | Current    | Notes |
|-----------------------------|----------|------------|-------|
| Estimated human min / video | 121      | 120        | --block removes assembling three fields into idea.md shape |
| Automated steps             | 44       | 45         | idea_brief --block + contract lock |
| Videos produced             | 0        | 0          | fixture only |
| Reconstruct list runtime    | PASS 042 | unchanged  | needed.py not edited |
| Scaffold contract           | PASS 051 | unchanged  | new_packet not edited |
| Idea gate contract          | PASS 048 | unchanged  | not re-run |
| Operator pin contract       | PASS 050 | strings kept | human_session gained --block only |
| Idea brief contract         | PASS 053 | PASS 054   | /tmp/ca tempfile; idea.md hash unchanged including --block |

## Active constraints
- Do not auto-scaffold Q1
- Do not map needed.py / doctor.py / expand_prompt.py / idea_gate_contract.py / operator_pin_contract.py / idea_brief_contract.py
- needed.py --missing, --bootstrap, and --plan must exit 0
- Do not treat --bootstrap or --plan as a sixth contract
- Do not grow BOOTSTRAP or WAVE 2/3 into a full-repo dump
- WAVE 3 stays commands only: reconstruct line + operator line; not a queue file list
- Do not add WAVE 4 unless a new post-WAVE-3 guess is observed
- FALLBACK_ALIAS must match which_contract.MAP tool lists
- Do not retry HTTPS clone after one failure
- No secrets, ffmpeg recipe, TTS, or YouTube API
- new_packet must not write idea.md or mark the queue
- idea_brief must not write idea.md (including --block)
- expand_prompt must not write idea.md or script.md
- next_action/hint must not print expand_prompt as the first live command while idea.md mechanism is blank
- Do not treat idea_gate_contract, operator_pin_contract, or idea_brief_contract as permission to auto-write idea.md or scaffold Q1
- Do not add a problem column to topic_queue unless a human asks; lock the operator-page sentence instead; reprint it from Q1_PROBLEM
