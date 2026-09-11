# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-11T06:22:00Z — Run 065

- **Objective:** After locking set_status blocked ready_for_vo, lock the advertised apply_script write refuse on the fixture: `apply_script.py FIXTURE --from draft.md --write` must exit 1, print BLOCKED, and leave script.md unchanged.
- **Inspected:** STATE/NEXT/RUNS after Run 064. write_path_contract already locked apply missing --from, existing-draft dry-run, and set_status blocked CLI. apply_script helper already refused fixtures; main() write-before-check was unlocked.
- **Action taken:** Reconstructed write_path tools locally. Added tempfile subprocess for apply_script `--from FIXTURE/draft.md --write`. Expects exit 1, Result BLOCKED, fixture/sample-001 text, script.md and draft.md unchanged. Did not edit apply_script or set_status. Did not scaffold Q1. Did not write idea.md.
- **Result:** WRITE PATH CONTRACT PASS (exit 0) on reconstructed tree. Standalone fixture `--write` lock also PASS. Queue rows remain queued. No new packet folder.
- **Verification status:** completed for write_path_contract runtime on reconstructed tree. No media.
- **Important discovery:** Helper-only apply_check cannot catch a main() that writes script.md before the fixture refuse. The printed human_session `--write` command is the CLI.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, `--block` / paste / `--check` / expand off-repo / save draft.md / apply dry-run. Do not add another idea_brief flag. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1. Do not edit set_status or apply_script unless the locked CLIs regress.

## 2026-09-11T05:05:00Z — Run 064

- **Objective:** After locking apply_script dry-run, lock the next advertised write tool CLI: `set_status.py PATH --to ready_for_vo` must stay blocked while WORDS are short (and on the fixture), and must not rewrite packet.md even if `--write` is passed.
- **Result:** WRITE PATH CONTRACT PASS (exit 0). Queue rows remain queued. No new packet folder.
- **Recommended next action:** Human follows `docs/human_session.md`.

## 2026-09-11T04:20:00Z — Run 063

- **Objective:** After the missing `--from` CLI lock, lock the advertised success path: dry-run `apply_script.py PATH --from PATH/draft.md` must exit 0, print Dry-run only, and leave script.md unchanged.
- **Result:** WRITE PATH CONTRACT PASS (exit 0).

## Earlier runs 001–62
See prior commits for full detail.
