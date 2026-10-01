# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-10-01T18:25:00Z — Run 252

- **Objective:** Stop treating a killed mux as a master. Run 251 already locked finite apad. This run closes the header hole.
- **Inspected:** STATE/NEXT/RUNS/HANDOFF/FAILURES after Run 251. Live assemble.py already uses apad=pad_dur=20. Sandbox reminder: ffmpeg mux with bare apad was Killed; new.mp4 had no moov.
- **Action taken:** execute now requires mp4_header_ok on export/master.mp4 before deleting .segments. Failed mux leaves the work dir. Did not re-download. Did not bump status. Did not upload. Did not scaffold Q2.
- **Result:** Assemble is fail-closed on incomplete mp4. Automated steps stay 96. Videos published stay 0. Packet status stays ready_for_vo.
- **Verification status:** Code change on main. Live Q1 re-encode still not run in this sandbox (no DROP on this machine; gh not on PATH).
- **Important discovery:** Bare `[1:a]apad[a]` plus -shortest still hangs or is killed. pad_dur lock from Run 251 is necessary but not sufficient if the process dies mid-mux.
- **Blocker:** YouTube OAuth absent. Finished export still needs assemble --execute on a checkout that has DROP + cards, after moving the truncated r249 master aside.
- **Recommended next action:** On a checkout with wav and cards, move truncated master aside, run assemble.py --execute, confirm duration is VO+20 and ftyp present. Do not upload r249 master. Do not regenerate.

