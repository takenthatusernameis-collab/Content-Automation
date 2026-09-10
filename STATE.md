# STATE

Updated: 2026-09-10T09:05:00Z (Run 045)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + scaffold handoff + contract router + router lock + reconstruct list + reconstruct presence check + first-fetch bootstrap + fetch-wave plan + post-reconstruct operator command + operator reconstruct command + operator page with first-video expand/apply/status + Q1 title/path pin + idea.md pre-expand edit + scaffold idea reprint** -> automated -> self-improving

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

## What exists now (after Run 045)
- Operating memory files and frozen original master prompt
- Video packet standard + scaffold CLI + packet QA
- Sample packet fixture `videos/sample-001-why-systems-beat-motivation/`
- Topic queue + queue_lib + next_topic + queue_status + mark_topic
- Contracts: queue, write-path, scaffold, which_contract, router_contract
- Reconstruct list `tools/needed.py` (read-only; unmapped like doctor)
- needed.py --missing / --bootstrap / --plan unchanged from Run 042
- Reconstruct-loop (Runs 037-042) flagged in FAILURES.md
- `new_packet.idea_followup` reprints topic + queue one_line mechanism; does not write idea.md
- No new packet folder this run; queue still queued
- No needed.py edit this run
- Operator page no longer uses a placeholder title or `videos/002-slug`

## Pipeline map
Unchanged from Run 037. Oversight now includes needed.py --plan WAVE 3 reconstruct + operator lines. Operator page no longer defers expand/apply/status and no longer leaves Q1 title/path as a guess. Scaffold reprint now includes idea.md fields so later packets do not require opening topic_queue.md for the mechanism.

## Metrics snapshot
| Metric                      | Previous | Current    | Notes |
|-----------------------------|----------|------------|-------|
| Estimated human min / video | 130      | 129        | scaffold reprints idea topic + mechanism |
| Automated steps             | 40       | 40         | reprint only; no new flag |
| Videos produced             | 0        | 0          | fixture only |
| Reconstruct list runtime    | PASS 042 | unchanged  | needed.py not edited |
| Scaffold contract           | PASS 034 | PASS 045   | local /tmp/ca tree; no videos/ write |

## Active constraints
- Do not auto-scaffold Q1
- Do not map needed.py / doctor.py / expand_prompt.py
- needed.py --missing, --bootstrap, and --plan must exit 0
- Do not treat --bootstrap or --plan as a sixth contract
- Do not grow BOOTSTRAP or WAVE 2/3 into a full-repo dump
- WAVE 3 stays commands only: reconstruct line + operator line; not a queue file list
- Do not add WAVE 4 unless a new post-WAVE-3 guess is observed
- FALLBACK_ALIAS must match which_contract.MAP tool lists
- Do not retry HTTPS clone after one failure
- No secrets, ffmpeg recipe, TTS, or YouTube API
- new_packet must not write idea.md or mark the queue
