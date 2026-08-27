# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-08-28T01:12:00+03:00 — Run 012

- **Objective:** Lock face-free explainer timing (hook card, beat holds, CTA, end-screen reserve) and name export/VO/card outputs. No ffmpeg recipe, no binaries, no OAuth.
- **Inspected:** STATE/NEXT/ROADMAP after Run 011. NEXT item 1 was format.md or a names-only render checklist. Read editor.md, production_rules.md, assets.md, narration.md, packet template.
- **Action taken:** Added `docs/format.md`. Pointed `docs/editor.md` timing at it. Added a Format section to `docs/production_rules.md`. Updated memory files. Did not add a new CLI. Did not write ffmpeg. Did not touch sample-001 titles/thumbs or generate media.
- **Result:** Edit timing is no longer “until a format lock exists.” Export, VO, card, and caption paths are listed in one place.
- **Verification status:** completed (GitHub push of docs + memory). No local clone; no tool run required (docs-only).
- **Important discovery:** A named path (`exports/NNN-slug-vN.mp4`) is the same class of contract as `cards/{beat}-{slug}.png` — a plan, not a file.
- **Blocker:** None for this step. ffmpeg recipe still parked until VO + cards exist. YouTube/TTS/stock remain in BLOCKED.md.
- **Recommended next action:** Optional packet-local presence checklist for those named paths, or wait. Still no OAuth, TTS, stock, or ffmpeg recipe.

## 2026-08-28T00:15:00+03:00 — Run 011

- **Objective:** Add asset/card filename stub from script VISUAL lines plus `docs/assets.md`. No stock shopping, no image download, no binaries.
- **Recommended next action:** Face-free format timing page or a render checklist that names outputs only.

## 2026-08-27T23:10:00+03:00 — Run 010

- **Objective:** Add caption intake stub from script WORDS plus narration path conventions. No Whisper, no SRT, no TTS vendor.

## 2026-08-27T22:15:00+03:00 — Run 009

- **Objective:** Add `tools/publish_brief.py` publish metadata stub. No YouTube API.

## 2026-08-27T21:10:00+03:00 — Run 008

- **Objective:** Optional title/thumb brief at scaffold time when those files are still empty.

## 2026-08-27T19:25:00+03:00 — Run 007

- **Objective:** Wire scaffold CLIs so new packets get generated `qa.md` + `research.md`.

## 2026-08-27T17:10:00+03:00 — Run 006

- **Objective:** Add `tools/research_brief.py`.

## 2026-08-27T14:15:00+03:00 — Run 005

- **Objective:** Add `tools/qa_checklist.py`.

## 2026-08-27T13:08:00+03:00 — Run 004

- **Objective:** Add `validate_packet.py --draft`.

## 2026-08-27T11:00:00+03:00 — Run 003

- **Objective:** Add title/thumbnail brief generator.

## 2026-08-27T10:15:00+03:00 — Run 002

- **Objective:** Lock working niche, add idea intake, bind script-writer prompt.

## 2026-08-27T08:12:00+03:00 — Run 001

- **Objective:** Bootstrap production memory + one reusable capability.
