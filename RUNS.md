# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T02:05:00Z — Run 038

- **Objective:** Let clone-less agents see which reconstruct files are still absent, and resolve edited-tool names before which_contract is fetched.
- **Inspected:** STATE/NEXT/ROADMAP after Run 037. needed.py listed paths but did not check disk. Without which_contract, `needed.py new_packet.py` printed Unknown.
- **Action taken:** Added `--missing` (PRESENT/MISSING, READY/NOT READY, always exit 0). Added FALLBACK_ALIAS aligned to which_contract.MAP tool lists. Did not map needed.py. Did not edit which_contract or the five locks. Did not scaffold Q1. Did not change sample-001. Did not retry clone.
- **Result:** Local `/tmp/ca/tools` (no which_contract present):
  - `needed.py new_packet.py` prints scaffold_contract + tools/new_packet.py + queue_lib + docs/topic_queue.md
  - `needed.py doctor.py` and `needed.py needed.py` print Unknown, exit 0
  - `needed.py scaffold_contract.py --missing` prints four MISSING rows, NOT READY, exit 0
- **Verification status:** completed for the reconstruct presence printer. Other contract runtimes not re-run (no lock-body change). No media. No new packet folder. Queue rows remain queued.
- **Important discovery:** A reconstruct list that cannot resolve `new_packet.py` until the router file is fetched still forces agents to guess the first fetch set.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1. Agents: `python3 tools/needed.py EDITED_FILE --missing` after fetching listed paths. Do not auto-scaffold Q1. Do not add a sixth contract for needed.py. Do not make --missing exit 1.

## 2026-09-10T00:16:00Z — Run 037

- **Objective:** Stop clone-less agents from reconstructing the wrong file set from memory.
- **Result:** needed.py reconstruct list. Unmapped. Local PASS.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-09T23:15:00Z — Run 036

- **Objective:** Lock the which_contract map.
- **Result:** router_contract.py ROUTER CONTRACT PASS.

## Earlier runs 001–035
See prior commits for full detail.
