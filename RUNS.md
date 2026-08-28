# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-08-28T10:20:00+03:00 — Run 019

- **Objective:** When next_action says `expand-script` and expand.md already has Add-column targets, stop making the human open six files to brief a writer. No WORDS rewrite, no fixture pad, no wav, no TTS, no ffmpeg, no OAuth.
- **Inspected:** STATE/NEXT/ROADMAP after Run 018. Sample still 153 spoken words. Budget exists. Missing piece was a single paste pack.
- **Action taken:** Added `tools/expand_prompt.py` (stdout assembler + fixture lock banner + refuse `--out script.md`). Added `prompts/script_expander.md`. Did not change sample-001 script.md. Did not rewrite next_action.py, expand_brief.py, or validate_packet.py.
- **Result:** Local dry-run on a copy of sample fields: Spoken words 153, status short, fixture lock banner present, `--out script.md` exit 1. GitHub push of tool + expander prompt + memory. Commits on main include 9c8fd2a and follow-ups.
- **Verification status:** completed for tool logic on a local copy. GitHub push verified by ref update. No media created. Sample WORDS unchanged.
- **Important discovery:** A filled prompt looks like a draft. Printing it must not become writing script.md, especially on sample-001.
- **Blocker:** None for this step. ffmpeg recipe still parked until VO + cards exist. YouTube/TTS/stock remain in BLOCKED.md.
- **Recommended next action:** Wait for a human to paste expanded WORDS into a new non-fixture packet, or for a selected take / card file on a packet already in band. Still no OAuth, TTS, stock, ffmpeg recipe, fixture pad, WORDS autofill, or status auto-bump.

## 2026-08-28T07:20:00+03:00 — Run 018

- **Objective:** When next_action says `expand-script`, stop leaving the human to guess which beat to grow.
- **Recommended next action:** Wait for a real selected take or card file on a packet whose WORDS already sit in band.

## 2026-08-28T06:20:00+03:00 — Run 017

- **Objective:** Stop routing humans to record VO on a structurally PASS script that is far under the locked 6–10 min format.

## 2026-08-28T05:24:00+03:00 — Run 016

- **Objective:** Cut recurring VO-prep labor: turn PASS script WORDS into a packet-local reading card and named take path.

## Earlier runs 001–015
See prior commits for full detail.
