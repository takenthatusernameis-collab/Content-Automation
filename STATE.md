# STATE

Updated: 2026-09-10T04:10:00Z (Run 040)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + monitored queue + write-path + scaffold handoff + contract router + router lock + reconstruct list + reconstruct presence check + first-fetch bootstrap + fetch-wave plan** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured
- HTTPS clone from this agent sandbox still fails (private repo). Push via GitHub file API.
- Reconstruct + selftest path: `docs/agent_session.md`
- First fetch: `python3 tools/needed.py --bootstrap`
- Fetch waves: `python3 tools/needed.py --plan`
- Reconstruct file list: `python3 tools/needed.py CONTRACT`
- Reconstruct presence: `python3 tools/needed.py CONTRACT --missing` (exit 0 even if NOT READY)

## What exists now (after Run 040)
- Operating memory files and frozen original master prompt
- Video packet standard + scaffold CLI + packet QA
- Sample packet fixture `videos/sample-001-why-systems-beat-motivation/`
- Topic queue + queue_lib + next_topic + queue_status + mark_topic
- Contracts: queue, write-path, scaffold, which_contract, router_contract
- Reconstruct list `tools/needed.py` (read-only; unmapped like doctor)
- `needed.py --missing` reports PRESENT/MISSING/READY/NOT READY; always exit 0
- `needed.py --bootstrap` prints the first-fetch set; `--bootstrap --missing` same flags; always exit 0
- `needed.py --plan` prints WAVE 1 (bootstrap paths) then WAVE 2 command (`needed.py selftest.py --missing`); does not dump selftest files; always exit 0
- FALLBACK_ALIAS so `needed.py new_packet.py` works before which_contract is fetched
- Operator path `docs/human_session.md`; agent path `docs/agent_session.md`
- Spoken-duration band: 900-1500 words for explainer-6-10min at 150 wpm
- No new packet folder this run; queue still queued

## Pipeline map
Unchanged from Run 037. Oversight now includes needed.py --plan.

## Metrics snapshot
| Metric                      | Previous | Current    | Notes |
|-----------------------------|----------|------------|-------|
| Estimated human min / video | 135      | 134        | plan stops second-wave guesswork |
| Automated steps             | 37       | 38         | --plan fetch-wave printer |
| Videos produced             | 0        | 0          | fixture only |
| Reconstruct list runtime    | PASS 039 | PASS 040   | local /tmp/ca/tools |

## Active constraints
- Do not auto-scaffold Q1
- Do not map needed.py / doctor.py / expand_prompt.py
- needed.py --missing, --bootstrap, and --plan must exit 0
- Do not treat --bootstrap or --plan as a sixth contract
- Do not grow BOOTSTRAP or WAVE 2 into a full-repo dump
- FALLBACK_ALIAS must match which_contract.MAP tool lists
- Do not retry HTTPS clone after one failure
- No secrets, ffmpeg recipe, TTS, or YouTube API
