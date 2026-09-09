# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-09T19:05:00Z — Run 031

- **Objective:** Turn the queue board into a monitor without coupling writes or changing the default human glance.
- **Inspected:** STATE/NEXT/ROADMAP after Run 030. queue_status classified rows but always exited 0 and did not show packet status. Gated tools frozen. No non-fixture packet.
- **Action taken:** Extended `tools/queue_status.py` with a PACKET column (reads `- status:` only) and `--strict` exit codes (2 missing-folder, 1 mark-needed/unknown-status, 0 clean). Default exit remains 0. Did not scaffold Q1. Did not change sample-001. Did not rewrite doctor/hint/selftest. Did not retry clone.
- **Result:** Temp tree `/tmp/ca`: five queued rows + fixture only -> default 0, `--strict` 0, next scaffold `videos/002-stop-deciding-what-to-work-on-every-morning`. Synthetic 002 folder -> Q1 `mark-needed` PACKET `draft`, `--strict` 1. Q5 marked used with no folder -> `missing-folder`, `--strict` 2. Files pushed via GitHub file API.
- **Verification status:** completed for the monitor contract on a temp tree. Selftest not re-run (no gated-tool change). No media. No new packet folder in the real repo. Queue rows remain queued.
- **Important discovery:** Opt-in `--strict` is the same pattern as doctor/pipeline_status. Making default exit non-zero would turn every clean human start into a failure.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1. Agents: do not auto-scaffold Q1; do not invent WORDS; do not pad the fixture.

## 2026-09-09T18:10:00Z — Run 030

- **Objective:** Remove the remaining human scan of topic_queue.md against videos/ after scaffold, without coupling mark_topic --write to a board.
- **Result:** Read-only queue_status.py. No new packet folder in the real repo.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-09T17:20:00Z — Run 029

- **Objective:** Stop humans from looking up the Q-id after scaffold, without coupling mark_topic --write to new_packet.
- **Result:** queue_lib + new_packet reprints mark_topic dry-run. No new packet folder in the real repo.
- **Recommended next action:** Human runs next_topic then human_session.

## Earlier runs 001–028
See prior commits for full detail.
