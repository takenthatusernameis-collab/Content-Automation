# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T03:10:00Z — Run 039

- **Objective:** Stop clone-less agents from guessing the first files to fetch before needed.py can resolve names.
- **Inspected:** STATE/NEXT/ROADMAP after Run 038. needed.py listed contracts and presence, but session start still required memory of which six files to pull first.
- **Action taken:** Added `--bootstrap` (ordered first-fetch set + optional `--missing`). Did not map needed.py. Did not edit which_contract or the five locks. Did not scaffold Q1. Did not change sample-001. Did not retry clone. Did not grow BOOTSTRAP into a full-repo list.
- **Result:** Local `/tmp/ca/tools` (needed.py only):
  - `needed.py --bootstrap` prints tools/needed.py, docs/agent_session.md, STATE.md, NEXT.md, RUNS.md, tools/which_contract.py; exit 0
  - `needed.py --bootstrap --missing` prints PRESENT needed.py + five MISSING, NOT READY, exit 0
  - `needed.py new_packet.py` still resolves to scaffold_contract
  - `needed.py doctor.py` still Unknown, exit 0
- **Verification status:** completed for the first-fetch printer. Other contract runtimes not re-run (no lock-body change). No media. No new packet folder. Queue rows remain queued.
- **Important discovery:** A presence check on a contract is useless until the agent knows the six files that make the printer itself usable.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1. Agents: fetch `python3 tools/needed.py --bootstrap` first, then `--missing` after each wave. Do not auto-scaffold Q1. Do not add a sixth contract for needed.py. Do not make --bootstrap exit 1.

## 2026-09-10T02:05:00Z — Run 038

- **Objective:** Let clone-less agents see which reconstruct files are still absent, and resolve edited-tool names before which_contract is fetched.
- **Result:** `--missing` + FALLBACK_ALIAS. Local PASS.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-10T00:16:00Z — Run 037

- **Objective:** Stop clone-less agents from reconstructing the wrong file set from memory.
- **Result:** needed.py reconstruct list. Unmapped. Local PASS.

## Earlier runs 001–036
See prior commits for full detail.
