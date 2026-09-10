# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-10T23:10:00Z — Run 058

- **Objective:** After default idea_brief reprint, stop the human from substituting PATH in the --check command. No new flag, no reconstruct wave, no idea.md write.
- **Inspected:** STATE/NEXT/RUNS after Run 057. idea_brief already printed exact --block on PASTE INCOMPLETE and exact expand_prompt on PASTE READY. Default reprint still said `python3 tools/idea_brief.py PATH --check`. Q1 still queued. FAILURES flags another needed.py/WAVE/contract loop.
- **Action taken:** Added `check_command` and printed that exact line on the default reprint. Also printed the exact `--block` command on default reprint. Extended idea_brief_contract to require `check_command` in source and those lines on the blank tempfile default run. Noted the printed commands on human_session. Did not write idea.md in the repo. Did not scaffold Q1. Did not edit needed.py / which_contract / new_packet / doctor.
- **Result:** Local `/tmp/ca-repo` run: IDEA BRIEF CONTRACT PASS, exit 0. Default reprint includes `idea_brief.py` `--check` and the 002 folder, plus `--block`. Blank --check still exit 2. Pasted --check still exit 0. idea.md hash unchanged under default, --block, and --check. Queue rows remain queued. No new packet folder in the repo.
- **Verification status:** completed for the default-reprint --check command line (local PASS, no write). Full selftest / operator_pin_contract not reconstructed this run (clone-less). No media.
- **Important discovery:** After default reprint, leftover labor was replacing the PATH placeholder. Printing the exact command is cheaper than another flag.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, run printed `--block`, paste, run printed `--check`, then run the printed expand_prompt off-repo. After editing idea_brief default reprint, run `idea_brief_contract.py`. Do not add another idea_brief flag unless new leftover labor appears after PASTE READY. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1.

## 2026-09-10T22:13:00Z — Run 057

- **Objective:** After --check exit 2, stop the human from hunting the --block command. No new flag, no reconstruct wave, no idea.md write.
- **Result:** IDEA BRIEF CONTRACT PASS. Queue rows remain queued. No new packet folder.
- **Recommended next action:** Human runs queue_status then human_session. After scaffold, if --check exits 2, run the printed --block command, paste, re-check, then run the printed expand_prompt.

## 2026-09-10T21:05:00Z — Run 056

- **Objective:** After paste confirm, stop the human from hunting the expand command. No new flag, no reconstruct wave, no idea.md write.
- **Result:** IDEA BRIEF CONTRACT PASS. Queue rows remain queued. No new packet folder.

## Earlier runs 001–55
See prior commits for full detail.
