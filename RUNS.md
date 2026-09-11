# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-11T01:20:00Z — Run 060

- **Objective:** After PASTE READY prints apply_script `--from FILE`, stop the human from inventing FILE. Pin a packet-local `draft.md` path. No new flag, no reconstruct wave, no idea.md write.
- **Inspected:** STATE/NEXT/RUNS after Run 059. idea_brief already printed expand_prompt then apply_script `--from FILE`. Contract required the FILE token. Q1 still queued. Leftover labor: choosing where to save the off-repo draft.
- **Action taken:** Added `draft_path` (`PATH/draft.md`). `apply_command` now prints `python3 tools/apply_script.py PATH --from PATH/draft.md`. PASTE READY also prints a save-to-draft.md line. Still does not print `--write`. Extended idea_brief_contract for draft_path, human_session draft.md, and PASTE READY `--from draft.md` without FILE or `--write`. Updated human_session apply examples to the same path. Did not write idea.md. Did not scaffold Q1. Did not edit needed.py / which_contract / new_packet / doctor / apply_script.
- **Result:** Local `/tmp/ca-work` run: IDEA BRIEF CONTRACT PASS, exit 0. PASTE READY stdout includes expand_prompt then apply_script --from .../draft.md. Blank --check still exit 2. idea.md hash unchanged under default, --block, and --check on the contract tempfile. Queue rows remain queued. No new packet folder in the repo.
- **Verification status:** completed for draft.md apply dry-run + contract lock (local PASS, no write). Full selftest / operator_pin_contract not reconstructed this run (clone-less). No media.
- **Important discovery:** After printed apply `--from FILE`, leftover labor was inventing FILE. Naming `PATH/draft.md` is cheaper than another flag. Keep `--write` off that stdout.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, run printed `--block`, paste, run printed `--check`, then run the printed expand_prompt off-repo, save to PATH/draft.md, then the printed apply_script dry-run. After editing idea_brief PASTE READY lines, run `idea_brief_contract.py`. Do not add another idea_brief flag unless new leftover labor appears after the printed draft.md apply dry-run. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1.

## 2026-09-11T00:20:00Z — Run 059

- **Objective:** After PASTE READY prints expand_prompt, stop the human from hunting the apply_script dry-run. Also lock the Run 058 check_command / exact default --check claims that were not fully in idea_brief_contract. No new flag, no reconstruct wave, no idea.md write.
- **Result:** IDEA BRIEF CONTRACT PASS. PASTE READY stdout includes expand_prompt then apply_script --from FILE.
- **Recommended next action:** Human runs queue_status then human_session.

## Earlier runs 001–58
See prior commits for full detail.
