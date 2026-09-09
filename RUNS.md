# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-09T11:20:00Z — Run 025

- **Objective:** Runs 022–024 left doctor/hint/validate runtime unverified because the sandbox cannot clone the private repo. Encode the fixture contract as an executable selftest so the next clone or local session can prove gates without rereading STATE.
- **Inspected:** STATE/NEXT/ROADMAP/README/doctor/hint/next_action/pipeline_status/validate/set_status/apply_script after Run 024. Sample still the only packet. NEXT forbids wrapping doctor in start.py and forbids padding WORDS.
- **Action taken:** Added `tools/selftest.py` (read-only; sample-001 only). Asserts publish PASS, duration WARN + `--duration` FAIL, draft status, no drift, next-action `expand-script`, first live hint command has no `--write`, fixture lock present, set_status and apply_script refuse the fixture. Did not change sample-001. Did not rewrite gated tools. Did not add start.py.
- **Result:** Selftest file present. Memory files updated. No media. No status bump. Live import against the fixture still cannot run in this sandbox (no checkout of videos/ + render_brief.py together).
- **Verification status:** completed for file presence and encoded contracts. Runtime of selftest against sample-001 remains unverified until a machine with a full checkout runs `python3 tools/selftest.py`.
- **Important discovery:** Repeating “runtime unverified” without a check file is itself the labor. A selftest is cheaper than another prose restatement. Flag: three consecutive runs could not execute Python against the fixture from this agent path.
- **Blocker:** Private-repo clone still unavailable from this sandbox. Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist.
- **Recommended next action:** On a full checkout, run `python3 tools/selftest.py`. Human follows `docs/human_session.md` on a new packet. Agents: do not invent WORDS, do not pad the fixture, do not wrap doctor in start.py.

## 2026-09-09T10:20:00Z — Run 024

- **Objective:** After doctor exists, stop leaving humans to reconstruct the expand → apply → set_status path from NEXT.md and 21 tool files. Still no WORDS invention, no fixture pad, no wav, no TTS, no ffmpeg, no OAuth.
- **Inspected:** STATE/NEXT/ROADMAP/README after Run 023. Sample still the only packet. NEXT forbids rewriting doctor/hint/set_status/apply_script unless wrong. HTTPS clone failed once (private repo); did not retry.
- **Action taken:** Added `docs/human_session.md` (doctor-first operator path, fixture freeze, dry-run-then-write). Pointed README start list and Local tools closer at that page. Marked roadmap item 28 done. Did not change sample-001. Did not add start.py. Did not rewrite gated tools.
- **Result:** Playbook present. Memory files updated. No media. No status bump.
- **Verification status:** completed for file presence and scope. Runtime of doctor against sample-001 unverified in this sandbox (no checkout). GitHub push to be verified by ref update.
- **Important discovery:** Runs 021–023 already encoded the path in tools; the remaining labor was finding the path. A second wrapper tool would not have reduced that. One page does.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. Private-repo clone remains unavailable from this sandbox.
- **Recommended next action:** Human follows `docs/human_session.md` on a new packet. Agents: do not invent WORDS, do not pad the fixture, do not wrap doctor in start.py.

## 2026-09-08T21:26:00Z — Run 023

- **Objective:** After hint exists, stop leaving humans to run board + next_action + hint + validate as four commands. Still no WORDS invention, no fixture pad, no wav, no TTS, no ffmpeg, no OAuth.
- **Recommended next action:** Wait for a human to apply expanded WORDS to a new non-fixture packet with apply_script, then dry-run set_status `--to ready_for_vo`.

## Earlier runs 001–022
See prior commits for full detail.
