# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-09T15:21:00Z — Run 028

- **Objective:** Close queue drift after the first non-fixture scaffold and stop humans guessing `NNN-slug`.
- **Inspected:** STATE/NEXT/ROADMAP/PROGRESS/RUNS after Run 027. Queue printer existed but printed `videos/NNN-slug`. `new_packet.py` next_id ignored `sample-001-*` because the name does not start with digits, so the next id would have been `001`.
- **Action taken:** Added `tools/mark_topic.py` (dry-run default; `--write` required; refuses missing folder and sample-001). `next_topic.py` now prints predicted path and commented mark_topic follow-up. `new_packet.py` / `next_topic.py` next_id treat `sample-001-*` as 001 so the next packet is `002-...`. Did not scaffold Q1. Did not change sample-001 WORDS. Did not rewrite gated oversight tools. Did not retry clone.
- **Result:** Local dry run: no folder → skip used; folder `002-stop-deciding-...` → plan used; `--write` rewrote only that row; next_topic then printed Q2. Files pushed via GitHub file API.
- **Verification status:** completed for local printer/closer runtime on a temp tree. Selftest not re-run (no gated-tool change). No media. No new packet folder in the real repo. Queue rows remain queued.
- **Important discovery:** `sample-001-*` was invisible to `^(\d+)` next_id. Without the `(?:sample-)?` prefix, the first real packet would collide conceptually with the fixture number.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/next_topic.py` then follows `docs/human_session.md` on that title, including mark_topic after the folder exists. Agents: do not auto-scaffold Q1; do not invent WORDS; do not pad the fixture.

## 2026-09-09T13:04:00Z — Run 027

- **Objective:** Remove the blank-title stall before the first non-fixture packet without inventing WORDS, padding the fixture, wrapping doctor, or retrying clone.
- **Result:** Topic queue + read-only next_topic.py. No new packet folder.
- **Recommended next action:** Human runs next_topic then human_session.

## 2026-09-09T12:22:00Z — Run 026

- **Objective:** Close the three-run "runtime unverified" loop. Prove `tools/selftest.py` against sample-001 without padding WORDS or wrapping doctor.
- **Result:** SELFTEST PASS, exit 0, 153 words on reconstructed tree.
- **Recommended next action:** Human follows `docs/human_session.md` on a new packet.

## Earlier runs 001–025
See prior commits for full detail.
