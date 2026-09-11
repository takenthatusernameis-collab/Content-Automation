# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-11T07:25:00Z — Run 066

- **Objective:** After locking fixture apply --write refuse, lock the advertised success path on a non-fixture packet: `--refresh` without `--write` must write nothing; `--write` must replace script.md only; `--write --refresh` must replace script.md and refresh expand.md / vo_session.md / captions.md without bumping packet.md.
- **Inspected:** STATE/NEXT/RUNS after Run 065. write_path_contract already locked apply missing --from, existing-draft dry-run, set_status blocked CLI, and fixture --write. apply_script already implemented --write / --refresh; those CLIs were unlocked.
- **Action taken:** Reconstructed write_path tools locally. Added tempfile subprocesses for `--refresh` (no --write), `--write`, and `--write --refresh` on a live 002 packet with sentinel derived files. Did not edit apply_script or set_status. Did not scaffold Q1. Did not write idea.md.
- **Result:** WRITE PATH CONTRACT PASS (exit 0) on reconstructed tree. Queue rows remain queued. No new packet folder.
- **Verification status:** completed for write_path_contract runtime on reconstructed tree. No media.
- **Important discovery:** `--refresh` is gated behind `--write` in apply_script.main. A helper-only check cannot catch a future change that refreshes derived files on dry-run or that writes script.md without honoring --refresh.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human runs `python3 tools/queue_status.py` then follows `docs/human_session.md`. After scaffold, `--block` / paste / `--check` / expand off-repo / save draft.md / apply dry-run / `--write --refresh` on the non-fixture packet only. Do not add another idea_brief flag. Do not add WAVE 4. Do not auto-write idea.md. Do not auto-scaffold Q1. Do not edit set_status or apply_script unless the locked CLIs regress.

## 2026-09-11T06:22:00Z — Run 065

- **Objective:** After locking set_status blocked ready_for_vo, lock the advertised apply_script write refuse on the fixture: `apply_script.py FIXTURE --from draft.md --write` must exit 1, print BLOCKED, and leave script.md unchanged.
- **Result:** WRITE PATH CONTRACT PASS (exit 0). Queue rows remain queued. No new packet folder.
- **Recommended next action:** Human follows `docs/human_session.md`.

## Earlier runs 001–64
See prior commits for full detail.
