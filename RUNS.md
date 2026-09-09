# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-09T23:15:00Z — Run 036

- **Objective:** Lock the which_contract map so later agents cannot silently remap tools to the wrong lock or treat --run SKIP as FAIL.
- **Inspected:** STATE/NEXT/ROADMAP after Run 035. Router existed but had no contract of its own. `--after which_contract.py` printed no mapping.
- **Action taken:** Added `tools/router_contract.py`. Extended `which_contract.py` MAP with which_contract/router_contract → router_contract. Did not scaffold Q1. Did not change sample-001. Did not rewrite the four older locks. Did not retry clone.
- **Result:** Local run on `/tmp/ca/tools`:
  ```
  ROUTER CONTRACT PASS
  Map locked for 18 tools. Unknown tools exit 0. --run SKIP on missing deps.
  This command writes nothing under videos/ or docs/.
  EXIT:0
  ```
  `--after new_packet.py` → scaffold_contract; `--after which_contract.py` → router_contract; `doctor.py` stays unmapped.
- **Verification status:** completed for the router lock. Other contract runtimes not re-run (no lock-body change). No media. No new packet folder. Queue rows remain queued.
- **Important discovery:** A router without a lock is the same failure mode as four contracts without a router: the map lives only in markdown and drifts.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1. Agents: `python3 tools/which_contract.py --after EDITED_FILE` after any tool change. After editing the router, run `python3 tools/router_contract.py`. Do not auto-scaffold Q1.

## 2026-09-09T22:10:00Z — Run 035

- **Objective:** Stop later agents from guessing which contract to run after a tool edit.
- **Result:** `which_contract.py` map + --after checks. No new packet folder.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-09T21:12:00Z — Run 034

- **Objective:** Lock the scaffold → mark_topic handoff so later agents cannot make new_packet auto-write the queue.
- **Result:** `scaffold_contract.py` SCAFFOLD CONTRACT PASS. No new packet folder in the real repo.

## 2026-09-09T20:06:00Z — Run 033

- **Objective:** Lock the non-fixture write path so later agents cannot silently weaken apply_script or set_status gates.
- **Result:** `write_path_contract.py` WRITE PATH CONTRACT PASS.

## 2026-09-09T19:20:00Z — Run 032

- **Objective:** Lock the Run 031 queue-board contract so later agents cannot silently change classify codes or `--strict` exits.
- **Result:** `queue_contract.py` QUEUE CONTRACT PASS.

## Earlier runs 001–031
See prior commits for full detail.
