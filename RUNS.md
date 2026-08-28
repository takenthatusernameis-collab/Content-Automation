# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-08-28T14:15:00+03:00 — Run 021

- **Objective:** After apply_script lands WORDS, stop leaving humans to hand-edit packet.md status (the main source of board drift). Still no WORDS invention, no fixture pad, no wav, no TTS, no ffmpeg, no OAuth.
- **Inspected:** STATE/NEXT/ROADMAP after Run 020. Sample still short + draft. apply_script does not bump status by design. Board tools must stay read-only.
- **Action taken:** Added `tools/set_status.py` (dry-run default, `--to` required, `--write` to persist, fixture refuse except draft/abandon, skip-ahead refuse, duration WARN blocks ready_for_vo and ready_for_edit, VO/export presence required for later statuses). Did not change sample-001 packet.md. Did not rewrite pipeline_status.py or next_action.py.
- **Result:** Local copy tests: fixture `--to ready_for_vo` exit 1; skip `draft -> published` exit 1; short non-fixture `--to ready_for_vo` exit 1 (duration WARN); `--to abandoned --write` rewrote only status + updated on a temp demo packet. GitHub push of tool + memory.
- **Verification status:** completed for tool logic on a local copy. GitHub push to be verified by ref update. No media created. Sample status unchanged.
- **Important discovery:** A replacement string written as `rf"\\1 value"` can land as a literal `\\1` instead of the captured field key. Use `r"\\1 " + value` with a non-raw interpretation that yields group 1.
- **Blocker:** None for this step. Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist.
- **Recommended next action:** Wait for a human to apply expanded WORDS to a new non-fixture packet with apply_script, then dry-run set_status `--to ready_for_vo`. Still no OAuth, TTS, stock, ffmpeg recipe, fixture pad, WORDS autofill, or board auto-bump.

## 2026-08-28T11:05:00+03:00 — Run 020

- **Objective:** After expand_prompt prints a pack, stop leaving the human to swap script.md and refresh three derived files by hand. Still no WORDS invention, no fixture pad, no wav, no TTS, no ffmpeg, no OAuth.
- **Recommended next action:** Wait for a human to apply expanded WORDS to a new non-fixture packet with apply_script.

## Earlier runs 001–019
See prior commits for full detail.
