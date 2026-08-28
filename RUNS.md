# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-08-28T11:05:00+03:00 — Run 020

- **Objective:** After expand_prompt prints a pack, stop leaving the human to swap script.md and refresh three derived files by hand. Still no WORDS invention, no fixture pad, no wav, no TTS, no ffmpeg, no OAuth.
- **Inspected:** STATE/NEXT/ROADMAP after Run 019. Sample still 153 spoken words. Paste pack exists. Missing piece was a gated paste-back.
- **Action taken:** Added `tools/apply_script.py` (dry-run default, fixture refuse, expand-prompt refuse, heading/beat/hook checks, `--write`, optional `--refresh`). Did not change sample-001 script.md. Did not rewrite next_action.py, expand_prompt.py, or validate_packet.py.
- **Result:** Local dry-run on a copy of sample fields: fixture refuse exit 1; expand-prompt refuse exit 1; extra-beat mismatch exit 1; non-fixture same-script dry-run OK; `--write --refresh` wrote script + expand + vo_session + captions on a temp demo packet. GitHub push of tool + memory.
- **Verification status:** completed for tool logic on a local copy. GitHub push verified by ref update. No media created. Sample WORDS unchanged.
- **Important discovery:** A printed expand pack looks like a script. apply_script must refuse that stdout and must refuse sample-001 even when headings match.
- **Blocker:** None for this step. Still waiting on a human-owned non-fixture draft. ffmpeg recipe parked until VO + cards exist.
- **Recommended next action:** Wait for a human to apply expanded WORDS to a new non-fixture packet with apply_script, or for a selected take / card file on a packet already in band. Still no OAuth, TTS, stock, ffmpeg recipe, fixture pad, WORDS autofill, or status auto-bump.

## 2026-08-28T10:20:00+03:00 — Run 019

- **Objective:** When next_action says `expand-script` and expand.md already has Add-column targets, stop making the human open six files to brief a writer.
- **Recommended next action:** Wait for a human to paste expanded WORDS into a new non-fixture packet.

## Earlier runs 001–018
See prior commits for full detail.
