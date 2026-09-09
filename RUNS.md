# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-09T21:12:00Z — Run 034

- **Objective:** Lock the scaffold → mark_topic handoff so later agents cannot make new_packet auto-write the queue.
- **Inspected:** STATE/NEXT/ROADMAP after Run 033. Write-path and queue contracts exist. new_packet already prints dry-run mark_topic; NEXT forbids auto-scaffold and auto-mark.
- **Action taken:** Added read-only `tools/scaffold_contract.py`. Asserts new_packet source has mark_followup and no subprocess/uncommented mark_topic --write; mark_followup(Q1 title) prints dry-run `--id Q1` plus commented `--write`; unknown titles print generic mark_topic; titles_filled treats empty `1.` / empty Primary as untitled; next_id on a temp sample-001 tree is 002; no leak to videos/002-*. Did not scaffold Q1. Did not change sample-001. Did not rewrite new_packet, mark_topic, apply_script, or set_status. Did not retry clone.
- **Result:** `python3 /tmp/ca/tools/scaffold_contract.py` printed `SCAFFOLD CONTRACT PASS`, exit 0. File pushed via GitHub file API.
- **Verification status:** completed for the scaffold contract on a reconstructed tools + docs/topic_queue tree. Fixture selftest not re-run (no gated packet-tool body change). Queue contract not re-run (no queue-tool change). Write-path contract not re-run (no apply/set_status change). No media. No new packet folder in the real repo. Queue rows remain queued.
- **Important discovery:** Queue and write-path contracts did not assert the printed mark_followup strings. That handoff is the last place an agent could silently couple scaffold to queue writes.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1. Agents: do not auto-scaffold Q1; do not invent WORDS; do not pad the fixture. After new_packet/after_scaffold edits, run `scaffold_contract.py`.

## 2026-09-09T20:06:00Z — Run 033

- **Objective:** Lock the non-fixture write path so later agents cannot silently weaken apply_script or set_status gates.
- **Result:** `write_path_contract.py` WRITE PATH CONTRACT PASS. No new packet folder in the real repo.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-09T19:20:00Z — Run 032

- **Objective:** Lock the Run 031 queue-board contract so later agents cannot silently change classify codes or `--strict` exits.
- **Result:** `queue_contract.py` QUEUE CONTRACT PASS. No new packet folder in the real repo.
- **Recommended next action:** Human runs queue_status then human_session.

## Earlier runs 001–031
See prior commits for full detail.
