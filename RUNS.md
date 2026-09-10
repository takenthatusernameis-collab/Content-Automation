# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T04:10:00Z — Run 040

- **Objective:** Stop clone-less agents from guessing the command after the first-fetch set is READY.
- **Inspected:** STATE/NEXT/ROADMAP after Run 039. --bootstrap listed six files; session still required memory of what to reconstruct next.
- **Action taken:** Added `--plan` (WAVE 1 = bootstrap paths; WAVE 2 = `needed.py selftest.py --missing`, no selftest file dump). Did not map needed.py. Did not edit which_contract or the five locks. Did not scaffold Q1. Did not change sample-001. Did not retry clone.
- **Result:** Local `/tmp/ca/tools` (needed.py only):
  - `needed.py --plan` prints WAVE 1 six paths + WAVE 2 command; exit 0
  - `needed.py --plan --missing` PRESENT needed.py + five MISSING, NOT READY, exit 0
  - `needed.py --bootstrap` unchanged six paths, exit 0
  - `needed.py new_packet.py` still resolves to scaffold_contract
  - `needed.py doctor.py` still Unknown, exit 0
- **Verification status:** completed for the fetch-wave printer. Other contract runtimes not re-run (no lock-body change). No media. No new packet folder. Queue rows remain queued.
- **Important discovery:** First-fetch READY is not session-complete. The next reconstruct command must be printed, not remembered, and must not become a second file dump.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md` on Q1. Agents: `--bootstrap` then `--plan` then fetch WAVE 1, then the WAVE 2 command. Do not auto-scaffold Q1. Do not add a sixth contract. Do not make --plan exit 1. Do not list selftest files inside --plan.

## 2026-09-10T03:10:00Z — Run 039

- **Objective:** Stop clone-less agents from guessing the first files to fetch before needed.py can resolve names.
- **Result:** `--bootstrap`. Local PASS.
- **Recommended next action:** Human runs queue_status then human_session.

## 2026-09-10T02:05:00Z — Run 038

- **Objective:** Let clone-less agents see which reconstruct files are still absent, and resolve edited-tool names before which_contract is fetched.
- **Result:** `--missing` + FALLBACK_ALIAS. Local PASS.

## 2026-09-10T00:16:00Z — Run 037

- **Objective:** Stop clone-less agents from reconstructing the wrong file set from memory.
- **Result:** needed.py reconstruct list. Unmapped. Local PASS.

## Earlier runs 001–036
See prior commits for full detail.
