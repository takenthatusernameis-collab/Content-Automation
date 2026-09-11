# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-11T04:20:00Z — Run 063

- **Objective:** After the missing `--from` CLI lock, lock the advertised success path: dry-run `apply_script.py PATH --from PATH/draft.md` must exit 0, print Dry-run only, and leave script.md unchanged.
- **Inspected:** STATE/NEXT/RUNS after Run 062. write_path_contract already subprocess-ran a missing draft. apply_script main() already dry-runs by default. Q1 still queued.
- **Action taken:** Reconstructed write_path tools locally. Added a tempfile subprocess that runs `python3 tools/apply_script.py LIVE --from LIVE/draft.md` (no `--write`), expects exit 0, `Dry-run only`, Result OK, script.md still the short body, draft.md unchanged. Did not edit apply_script, idea_brief, needed.py, doctor, or human_session. Did not scaffold Q1. Did not write idea.md.
- **Result:** WRITE PATH CONTRACT PASS (exit 0). Queue rows remain queued. No new packet folder.
- **Verification status:** completed for write_path_contract runtime on reconstructed tree. No media.
- **Important discovery:** The printed PASTE READY command is the no-`--write` argv. A helper-only check cannot catch a default-write regression in main().
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, `--block` / paste / `--check` / expand off-repo / save draft.md / apply dry-run. Do not add another idea_brief flag. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1. Do not edit apply_script unless the missing --from CLI or the dry-run existing-draft CLI regresses.

## 2026-09-11T03:20:00Z — Run 062

- **Objective:** Close the Run 061 verification gap: execute write_path_contract, then lock the advertised apply_script CLI (`--from` missing) so a helper-only check cannot hide a main() regression.
- **Result:** WRITE PATH CONTRACT PASS (exit 0). Queue rows remain queued. No new packet folder.
- **Recommended next action:** Human follows `docs/human_session.md`.

## 2026-09-11T02:10:00Z — Run 061

- **Objective:** After PASTE READY prints apply `--from PATH/draft.md`, stop the missing-file traceback.
- **Result:** Helper unit check locally printed the missing-source block.

## 2026-09-11T01:20:00Z — Run 060

- **Objective:** Pin PASTE READY apply to PATH/draft.md.
- **Result:** IDEA BRIEF CONTRACT PASS.

## Earlier runs 001–59
See prior commits for full detail.
