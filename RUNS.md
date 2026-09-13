# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-13T06:30:00Z — Run 112

- **Objective:** Run 111 (other agent) scaffolded Q1 and pasted idea.md but left draft.md empty and the packet missing template files. Remaining labor was a first draft in band, not another Target reprint.
- **Inspected:** Live HEAD after commits 64c286b..c614594. Packet had idea.md + empty draft.md + empty script.md + packet.md only. Queue Q1 already used. STATE/NEXT still described Run 110 (docs lagged the scaffold).
- **Action taken:** Wrote spoken WORDS into `videos/002-.../draft.md` targeting hook 20-35 / beats 140-220 / total 900-1500 (manual count 941). Copied missing template files into the packet. Did not apply --write. Did not edit script.md. Did not map forbidden tools. No new CLI.
- **Result:** First non-fixture draft exists. script.md still empty. words.py official count unverified in this sandbox (no checkout). No media.
- **Verification status:** Packet files pushed (commit 3d671cd for draft+templates). Manual word count only. apply_script and words.py not executed here.
- **Important discovery:** Parallel Run 111 already auto-scaffolded Q1 despite the standing do-not-auto-scaffold rule. STATE was not updated in that burst. Inspect HEAD commits before acting.
- **Blocker:** HTTPS clone still parked. Official words.py count and apply --write need a machine that can run the tools against the packet.
- **Recommended next action:** `words.py` on PATH, then apply dry-run / `--write --refresh` if IN BAND. Do not scaffold Q2. Do not add a reprint CLI.

## 2026-09-13T06:20:00Z — Run 111 (other agent)

- **Action taken:** Scaffolded Q1 folder, filled idea.md, copied draft template, marked queue used (commits 64c286b, ff846a3, ba06f81, c614594). Did not write spoken WORDS.
- **Result:** Packet exists. draft.md still empty until Run 112.

## 2026-09-13T05:05:00Z — Run 110

- **Action taken:** hint.py write-script/expand-script Command includes empty-draft Target comment.

## Earlier runs 001–109
See prior commits for full detail.
