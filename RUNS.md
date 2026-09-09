# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-09T22:10:00Z — Run 035

- **Objective:** Stop later agents from guessing which contract to run after a tool edit.
- **Inspected:** STATE/NEXT/ROADMAP after Run 034. Four locks exist (selftest, queue_contract, write_path_contract, scaffold_contract). NEXT item 1 listed them by hand. Agent session repeated the same map.
- **Action taken:** Added read-only `tools/which_contract.py`. Default prints the tool→contract table. `--after new_packet.py` prints `python3 tools/scaffold_contract.py`. `--after apply_script.py` prints write_path_contract. Unknown tools print the map and exit 0. `--run` subprocesses a contract only when required files exist; otherwise SKIP (not FAIL). Did not scaffold Q1. Did not change sample-001. Did not rewrite the four locks. Did not retry clone.
- **Result:** Local run of the new file: map exit 0; `--after new_packet.py` printed scaffold_contract; `--after apply_script.py` printed write_path_contract. File pushed via GitHub file API.
- **Verification status:** completed for the router itself (map + --after). Existing contract runtimes not re-run (no lock-body change). No media. No new packet folder. Queue rows remain queued.
- **Important discovery:** Four contracts without a router means NEXT and agent_session become the only map, and those pages already drift when a fifth lock appears.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1. Agents: `python3 tools/which_contract.py --after EDITED_FILE` after any tool change. Do not auto-scaffold Q1.

## 2026-09-09T21:12:00Z — Run 034

- **Objective:** Lock the scaffold → mark_topic handoff so later agents cannot make new_packet auto-write the queue.
- **Result:** `scaffold_contract.py` SCAFFOLD CONTRACT PASS. No new packet folder in the real repo.
- **Recommended next action:** Human runs queue_status then human_session.

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
