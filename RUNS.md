# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T16:15:00Z — Run 052

- **Objective:** Recover the idea.md paste pack after scaffold stdout is gone, without writing idea.md or adding a queue column.
- **Inspected:** STATE/NEXT/RUNS after Run 051. Q1 still queued. new_packet already reprints topic + problem + mechanism once. Frozen doctor/hint/needed not edited.
- **Action taken:** Added `tools/idea_brief.py` (read-only). It prints current idea.md topic/problem/mechanism and reuses `new_packet.idea_followup` for the suggested paste. Documented it on `docs/human_session.md` after the Q1 scaffold block. Did not write idea.md. Did not scaffold Q1. Did not edit needed.py. Did not map unmapped locks. Did not change hint/doctor.
- **Result:** Local run on a blank 002 packet in `/tmp/ca`: exit 0; printed blank current fields + Q1 topic/problem/mechanism; idea.md md5 unchanged. human_session still contains every operator-pin string (title, 002-slug, one_line, Q1_PROBLEM, fill-idea, no-write-idea, mark_topic --id Q1, exact new_packet command). Queue rows remain queued. No new packet folder in the repo.
- **Verification status:** completed for the reprint-recover tool (local exit 0, no write). Operator-pin strings checked in-file. Full operator_pin_contract / selftest not reconstructed this run (clone-less). No media.
- **Important discovery:** Scaffold reprint only helps if the human still has that terminal. A path-based reprint is the missing recover step; writing idea.md would still hide a blank-template expand.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, paste the three reprinted idea fields (or recover them with `idea_brief.py`). After editing human_session or the Q1 queue row, run `operator_pin_contract.py`. After editing new_packet idea reprint, run `scaffold_contract.py`. Agents: --bootstrap then --plan; do not add WAVE 4; do not auto-write idea.md; do not auto-scaffold Q1.

## 2026-09-10T15:05:00Z — Run 051

- **Objective:** Close the leftover paste gap: after scaffold, new_packet reprinted topic + mechanism but not the locked Q1 problem sentence, so the human still had to join two pages.
- **Result:** SCAFFOLD CONTRACT PASS. Queue rows remain queued. No new packet folder.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-10T14:20:00Z — Run 050

- **Objective:** Lock the Q1 idea.md problem sentence on the operator page, and list the two unmapped locks on the agent page so clone-less runs do not scan NEXT for them.
- **Result:** OPERATOR PIN CONTRACT PASS. Queue rows remain queued. No new packet folder.
- **Recommended next action:** Human runs queue_status then human_session.

## Earlier runs 001–49
See prior commits for full detail.
