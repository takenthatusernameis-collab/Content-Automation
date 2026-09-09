# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-09T20:06:00Z — Run 033

- **Objective:** Lock the non-fixture write path so later agents cannot silently weaken apply_script or set_status gates.
- **Inspected:** STATE/NEXT/ROADMAP after Run 032. Queue contract exists; selftest only covers fixture refuse; no non-fixture packet; NEXT forbids auto-scaffold and rewriting apply/set_status unless wrong.
- **Action taken:** Added read-only `tools/write_path_contract.py`. Temp tree only. Asserts expand-prompt detection, fence unwrap, fixture vs live detect, apply refuse (fixture / prompt / short hook), apply allow on a well-formed non-fixture body, set_status refuse (duration WARN -> ready_for_vo, skip draft->ready_for_edit, already draft, invalid status, fixture promote), and no leak into repo `videos/002-write-path-contract`. Did not scaffold Q1. Did not change sample-001. Did not rewrite apply_script, set_status, doctor, hint, selftest, or queue tools. Did not retry clone.
- **Result:** `python3 /tmp/ca/tools/write_path_contract.py` printed `WRITE PATH CONTRACT PASS`, exit 0. Files pushed via GitHub file API.
- **Verification status:** completed for the write-path contract on a temp tree. Fixture selftest not re-run (no gated packet-tool body change). Queue contract not re-run (no queue-tool change). No media. No new packet folder in the real repo. Queue rows remain queued.
- **Important discovery:** Selftest only proves fixture refuse. The allow path for apply_script and the duration-block for set_status were previously unasserted except by reading source.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1. Agents: do not auto-scaffold Q1; do not invent WORDS; do not pad the fixture. After apply_script/set_status edits, run `write_path_contract.py`.

## 2026-09-09T19:20:00Z — Run 032

- **Objective:** Lock the Run 031 queue-board contract so later agents cannot silently change classify codes or `--strict` exits.
- **Result:** `queue_contract.py` QUEUE CONTRACT PASS. No new packet folder in the real repo.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-09T19:05:00Z — Run 031

- **Objective:** Turn the queue board into a monitor without coupling writes or changing the default human glance.
- **Result:** queue_status PACKET column + `--strict`. No new packet folder in the real repo.

## Earlier runs 001–030
See prior commits for full detail.
