# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-09T18:10:00Z — Run 030

- **Objective:** Remove the remaining human scan of topic_queue.md against videos/ after scaffold, without coupling mark_topic --write to a board.
- **Inspected:** STATE/NEXT/ROADMAP/PROGRESS/RUNS after Run 029. Queue helpers live in queue_lib. next_topic prints one row. mark_topic writes only with folder evidence. No non-fixture packet exists. Gated tools are frozen.
- **Action taken:** Added read-only `tools/queue_status.py`. Classifies each queue row against existing folders. Prints next scaffold path and dry-run mark_topic only for mark-needed rows. Did not scaffold Q1. Did not change sample-001. Did not auto-mark. Did not rewrite doctor/hint/selftest. Did not retry clone.
- **Result:** Local reconstruct at `/tmp/ca` with queue_lib + current five queued rows: all `ok-queued`, next scaffold `videos/002-stop-deciding-what-to-work-on-every-morning`. Synthetic drift case: Q1 `mark-needed` when 002 folder exists; Q5 `missing-folder` when marked used with no folder; fixture title `fixture-refuse`. Files pushed via GitHub file API.
- **Verification status:** completed for the board contract on a temp tree. Selftest not re-run (no gated-tool change). No media. No new packet folder in the real repo. Queue rows remain queued.
- **Important discovery:** A queue board is the missing twin of pipeline_status. Printing mark-needed is enough; writing used from the board would hide a missing-folder mistake the same way auto-mark from new_packet would.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1. Agents: do not auto-scaffold Q1; do not invent WORDS; do not pad the fixture.

## 2026-09-09T17:20:00Z — Run 029

- **Objective:** Stop humans from looking up the Q-id after scaffold, without coupling mark_topic --write to new_packet.
- **Result:** queue_lib + new_packet reprints mark_topic dry-run. No new packet folder in the real repo.
- **Recommended next action:** Human runs next_topic then human_session.

## 2026-09-09T15:21:00Z — Run 028

- **Objective:** Close queue drift after the first non-fixture scaffold and stop humans guessing `NNN-slug`.
- **Result:** mark_topic + predicted path. No new packet folder in the real repo.

## 2026-09-09T13:04:00Z — Run 027

- **Objective:** Remove the blank-title stall before the first non-fixture packet.
- **Result:** Topic queue + read-only next_topic.py.

## 2026-09-09T12:22:00Z — Run 026

- **Objective:** Prove selftest against sample-001.
- **Result:** SELFTEST PASS, exit 0, 153 words.

## Earlier runs 001–025
See prior commits for full detail.
