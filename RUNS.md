# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-09T17:20:00Z — Run 029

- **Objective:** Stop humans from looking up the Q-id after scaffold, without coupling mark_topic --write to new_packet.
- **Inspected:** STATE/NEXT/ROADMAP/PROGRESS/RUNS after Run 028. next_id/slugify/parse_queue were copied in three files. new_packet printed only the folder path. DECISIONS forbids auto-mark from scaffold.
- **Action taken:** Added `tools/queue_lib.py`. Pointed `next_topic.py`, `mark_topic.py`, and `new_packet.py` at it. After a successful scaffold, `new_packet.py` prints the matching `mark_topic --id QN` dry-run line and a commented `--write`. Did not scaffold Q1. Did not change sample-001. Did not auto-mark. Did not rewrite gated oversight tools. Did not retry clone.
- **Result:** Local `queue_lib` checks PASS (next_id treats sample-001 as 001; match_folder ignores fixture; matching_queue_row finds Q1). Files pushed via GitHub file API.
- **Verification status:** completed for helper contract on a temp tree. Selftest not re-run (no gated-tool change). No media. No new packet folder in the real repo. Queue rows remain queued.
- **Important discovery:** Printing the Q-id from scaffold is enough to close lookup labor. Auto-writing the queue from new_packet would hide a missing-folder mistake.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/next_topic.py` then follows `docs/human_session.md` on that title, including the mark_topic line printed by new_packet. Agents: do not auto-scaffold Q1; do not invent WORDS; do not pad the fixture.

## 2026-09-09T15:21:00Z — Run 028

- **Objective:** Close queue drift after the first non-fixture scaffold and stop humans guessing `NNN-slug`.
- **Result:** mark_topic + predicted path. No new packet folder in the real repo.
- **Recommended next action:** Human runs next_topic then human_session.

## 2026-09-09T13:04:00Z — Run 027

- **Objective:** Remove the blank-title stall before the first non-fixture packet.
- **Result:** Topic queue + read-only next_topic.py.

## 2026-09-09T12:22:00Z — Run 026

- **Objective:** Prove selftest against sample-001.
- **Result:** SELFTEST PASS, exit 0, 153 words.

## Earlier runs 001–025
See prior commits for full detail.
