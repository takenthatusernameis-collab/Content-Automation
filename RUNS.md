# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-11T05:05:00Z — Run 064

- **Objective:** After locking apply_script dry-run, lock the next advertised write tool CLI: `set_status.py PATH --to ready_for_vo` must stay blocked while WORDS are short (and on the fixture), and must not rewrite packet.md even if `--write` is passed.
- **Inspected:** STATE/NEXT/RUNS after Run 063. write_path_contract already locked apply missing --from and existing-draft dry-run via subprocess. set_status helpers already blocked duration/skip/fixture. Q1 still queued.
- **Action taken:** Reconstructed write_path tools locally. Added tempfile subprocesses for `set_status.py LIVE --to ready_for_vo` (no --write), the same argv plus `--write`, and fixture `--write`. Expects exit 1, Result BLOCKED, duration or fixture text, packet.md still draft. Did not edit set_status, apply_script, idea_brief, needed.py, doctor, or human_session. Did not scaffold Q1. Did not write idea.md.
- **Result:** WRITE PATH CONTRACT PASS (exit 0). Queue rows remain queued. No new packet folder.
- **Verification status:** completed for write_path_contract runtime on reconstructed tree. No media.
- **Important discovery:** Helper-only status_check cannot catch a main() write-before-check regression. The printed human_session command is the CLI.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, `--block` / paste / `--check` / expand off-repo / save draft.md / apply dry-run. Do not add another idea_brief flag. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1. Do not edit set_status or apply_script unless the locked CLIs regress.

## 2026-09-11T04:20:00Z — Run 063

- **Objective:** After the missing `--from` CLI lock, lock the advertised success path: dry-run `apply_script.py PATH --from PATH/draft.md` must exit 0, print Dry-run only, and leave script.md unchanged.
- **Result:** WRITE PATH CONTRACT PASS (exit 0). Queue rows remain queued. No new packet folder.
- **Recommended next action:** Human follows `docs/human_session.md`.

## 2026-09-11T03:20:00Z — Run 062

- **Objective:** Close the Run 061 verification gap: execute write_path_contract, then lock the advertised apply_script CLI (`--from` missing) so a helper-only check cannot hide a main() regression.
- **Result:** WRITE PATH CONTRACT PASS (exit 0).

## Earlier runs 001–61
See prior commits for full detail.
