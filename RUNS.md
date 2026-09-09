# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-09T19:20:00Z — Run 032

- **Objective:** Lock the Run 031 queue-board contract so later agents cannot silently change classify codes or `--strict` exits.
- **Inspected:** STATE/NEXT/ROADMAP after Run 031. Queue board exists; no non-fixture packet; gated packet tools frozen; NEXT forbids auto-scaffold.
- **Action taken:** Added read-only `tools/queue_contract.py`. It builds a tempfile tree only, asserts classify codes (ok-queued, mark-needed, missing-folder, ok-used, parked, fixture-refuse, unknown-status), PACKET column reads, next_id after sample-001+002, mark_topic rewrite_status, default exit 0, `--strict` 2/1, and commented `--write` lines. Did not scaffold Q1. Did not change sample-001. Did not rewrite doctor/hint/selftest/queue_status. Did not retry clone.
- **Result:** `python3 /tmp/ca/tools/queue_contract.py` printed `QUEUE CONTRACT PASS`, exit 0. Files pushed via GitHub file API.
- **Verification status:** completed for the queue contract on a temp tree. Fixture selftest not re-run (no gated packet-tool change). No media. No new packet folder in the real repo. Queue rows remain queued.
- **Important discovery:** `packet_status` returns `no-packet` when the folder has no `packet.md`, and `no-status` only when `packet.md` exists but has no `- status:` line. Those are different misses.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1. Agents: do not auto-scaffold Q1; do not invent WORDS; do not pad the fixture. After queue-tool edits, run `queue_contract.py`.

## 2026-09-09T19:05:00Z — Run 031

- **Objective:** Turn the queue board into a monitor without coupling writes or changing the default human glance.
- **Result:** queue_status PACKET column + `--strict`. No new packet folder in the real repo.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-09T18:10:00Z — Run 030

- **Objective:** Remove the remaining human scan of topic_queue.md against videos/ after scaffold, without coupling mark_topic --write to a board.
- **Result:** Read-only queue_status.py. No new packet folder in the real repo.

## Earlier runs 001–029
See prior commits for full detail.
