# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-11T00:20:00Z — Run 059

- **Objective:** After PASTE READY prints expand_prompt, stop the human from hunting the apply_script dry-run. Also lock the Run 058 check_command / exact default --check claims that were not fully in idea_brief_contract. No new flag, no reconstruct wave, no idea.md write.
- **Inspected:** STATE/NEXT/RUNS after Run 058. idea_brief already printed exact --block on INCOMPLETE and exact expand_prompt on PASTE READY. Default reprint printed exact --check. Contract source_locks did not require check_command or exact default folder commands. Q1 still queued.
- **Action taken:** Added `apply_command` and printed that dry-run (`apply_script PATH --from FILE`) on PASTE READY. Did not print `--write`. Extended idea_brief_contract for check_command, apply_command, exact default --block/--check with folder, and PASTE READY apply dry-run without `--write`. Noted the printed apply line on human_session. Did not write idea.md. Did not scaffold Q1. Did not edit needed.py / which_contract / new_packet / doctor.
- **Result:** Local `/tmp/ca-repo` run: IDEA BRIEF CONTRACT PASS, exit 0. PASTE READY stdout includes expand_prompt then apply_script --from FILE. Blank --check still exit 2. idea.md hash unchanged under default, --block, and --check. Queue rows remain queued. No new packet folder in the repo.
- **Verification status:** completed for PASTE READY apply dry-run + contract lock (local PASS, no write). Full selftest / operator_pin_contract not reconstructed this run (clone-less). No media.
- **Important discovery:** After printed expand_prompt, leftover labor was hunting apply_script on human_session. Printing the dry-run is cheaper than another flag. Do not include the string `--write` on that stdout or the contract fails on purpose.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, run printed `--block`, paste, run printed `--check`, then run the printed expand_prompt off-repo, then the printed apply_script dry-run. After editing idea_brief PASTE READY lines, run `idea_brief_contract.py`. Do not add another idea_brief flag unless new leftover labor appears after the printed apply dry-run. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1.

## 2026-09-10T23:10:00Z — Run 058

- **Objective:** After default idea_brief reprint, stop the human from substituting PATH in the --check command. No new flag, no reconstruct wave, no idea.md write.
- **Result:** IDEA BRIEF CONTRACT PASS. Default reprint includes exact --check and --block. Queue rows remain queued.
- **Recommended next action:** Human runs queue_status then human_session.

## Earlier runs 001–57
See prior commits for full detail.
