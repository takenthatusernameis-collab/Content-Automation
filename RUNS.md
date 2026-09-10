# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T00:16:00Z — Run 037

- **Objective:** Stop clone-less agents from reconstructing the wrong file set from memory.
- **Inspected:** STATE/NEXT/ROADMAP after Run 036. Router lock exists. Reconstruct lists lived only in agent_session markdown.
- **Action taken:** Added `tools/needed.py`. Pointed `docs/agent_session.md` reconstruct sections at it. Did not map needed.py in which_contract. Did not scaffold Q1. Did not change sample-001. Did not rewrite the five locks. Did not retry clone.
- **Result:** Local run on `/tmp/ca/tools`:
  ```
  # scaffold_contract.py
  python3 tools/scaffold_contract.py
  tools/scaffold_contract.py
  tools/new_packet.py
  tools/queue_lib.py
  docs/topic_queue.md

  This command writes nothing.
  ```
  `needed.py selftest.py` lists the nine tools plus seven sample-001 files. `needed.py doctor.py` prints Unknown, exit 0.
- **Verification status:** completed for the reconstruct list printer. Other contract runtimes not re-run (no lock-body change). No media. No new packet folder. Queue rows remain queued.
- **Important discovery:** A router that names the lock is still not enough if the agent has to guess which files to fetch before that lock can run.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1. Agents: `python3 tools/needed.py EDITED_FILE` then fetch those paths; `python3 tools/which_contract.py --after EDITED_FILE` after any tool change. Do not auto-scaffold Q1. Do not add a sixth contract for needed.py.

## 2026-09-09T23:15:00Z — Run 036

- **Objective:** Lock the which_contract map so later agents cannot silently remap tools to the wrong lock or treat --run SKIP as FAIL.
- **Result:** `router_contract.py` ROUTER CONTRACT PASS. No new packet folder.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-09T22:10:00Z — Run 035

- **Objective:** Stop later agents from guessing which contract to run after a tool edit.
- **Result:** `which_contract.py` map + --after checks. No new packet folder.
- **Recommended next action:** Human runs queue_status then human_session.

## Earlier runs 001–034
See prior commits for full detail.
