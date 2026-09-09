# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

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
- **Inspected:** STATE/NEXT/ROADMAP after Run 022. Sample still short + draft. Board tools must stay read-only. NEXT forbids rewriting hint/set_status/apply_script unless wrong.
- **Action taken:** Added `tools/doctor.py` (read-only compose of inspect + recommend + commands_for + duration WARN). `--strict` exits 1 on FAIL gate or drift only. Duration WARN stays informational. Did not change sample-001. Did not rewrite hint.py or next_action.py.
- **Result:** Tool added and documented. Live import against the real fixture was not run in this sandbox (HTTPS clone requires credentials). GitHub push of tool + memory.
- **Verification status:** completed for file presence and composition design. Runtime against sample-001 unverified in this sandbox. No media created. Sample status unchanged.
- **Important discovery:** Four read-only oversight tools without a single entry point recreate lookup labor. The health block is the unit of session start.
- **Blocker:** None for this step. Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist.
- **Recommended next action:** Wait for a human to apply expanded WORDS to a new non-fixture packet with apply_script, then dry-run set_status `--to ready_for_vo`. Still no OAuth, TTS, stock, ffmpeg recipe, fixture pad, WORDS autofill, or board auto-bump.

## 2026-08-28T16:10:00+03:00 — Run 022

- **Objective:** After set_status exists, stop leaving humans to scan 21 tools for the next safe command. Still no WORDS invention, no fixture pad, no wav, no TTS, no ffmpeg, no OAuth.
- **Recommended next action:** Wait for a human to apply expanded WORDS to a new non-fixture packet with apply_script, then dry-run set_status `--to ready_for_vo`.

## Earlier runs 001–021
See prior commits for full detail.
