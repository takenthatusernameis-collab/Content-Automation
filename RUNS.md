# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-08-27T23:10:00+03:00 — Run 010

- **Objective:** Add caption intake stub from script WORDS plus narration path conventions. No Whisper, no SRT, no TTS vendor.
- **Inspected:** STATE/NEXT/ROADMAP after Run 009. NEXT item 1 was captions or `docs/narration.md`. Read after_scaffold, validate_packet, qa_checklist, publish_brief, sample script.
- **Action taken:** New `tools/caption_brief.py` builds a cue list + 150 wpm estimates from WORDS blocks. Empty-file / `--force` guard. `docs/narration.md` names the selected take path. Scaffold `after_scaffold.generate` writes captions after publish, before research/qa. Template `captions.md` is a placeholder. sample-001 got a fixture `captions.md`; titles/thumbs untouched. QA gained a human caption tick and a presence note. Did not write `.srt`. Did not call Whisper or YouTube.
- **Result:** Caption typing starts from existing script text. Empty-script packets stay placeholders so later WORDS can fill them. VO naming is documented without audio in git.
- **Verification status:** completed (local reconstruction of sample script + tool; live GitHub push of tools/docs). Commands:
  - `caption_brief.py sample-001 --dry-run` -> Cue count 7; Spoken words 153; Estimated speech 01:01; first cue `00:00–00:12` hook 29w; exit 0
  - first write -> exit 0
  - second write without `--force` -> exit 1 `already filled`
  - `write_empty_captions` on filled sample -> `kept .../captions.md (already filled)`
  - empty WORDS render -> Status placeholder; `captions_is_filled` False
  - template `(add spoken lines...)` -> `captions_is_filled` False
- **Important discovery:** Do not emit `captions.srt` from estimates. A `.srt` filename reads as aligned captions even with a disclaimer.
- **Blocker:** None for this step. Publishing/TTS/YouTube API remain in BLOCKED.md. TTS row now points at the path convention.
- **Recommended next action:** Asset/card filename stub from script VISUAL lines. Still no OAuth or stock shopping.

## 2026-08-27T22:15:00+03:00 — Run 009

- **Objective:** Add `tools/publish_brief.py` that writes a `publish.md` stub (description, tags, first comment) from idea + primary title. Empty-file / `--force` guard. No YouTube API.
- **Inspected:** STATE/NEXT/ROADMAP after Run 008. NEXT item 1 was publish metadata stub. Read `after_scaffold.py`, `title_thumb_brief.py`, `research_brief.py`, `validate_packet.py`, sample titles/idea/packet.
- **Action taken:** New `tools/publish_brief.py` reuses `load_packet_inputs` (not a second title bank). Primary comes from `titles.md` then `working_title`. Scaffold `after_scaffold.generate` writes publish after titles, before research/qa. Template `publish.md` is a placeholder. sample-001 got a fixture `publish.md`; titles/thumbs untouched. Did not rewrite idea/research/qa generators. Did not call YouTube.
- **Result:** Description/tags/first-comment draft exists without an extra human blank page. Filled publish.md is kept.
- **Verification status:** completed (local reconstruction of packet fields + tool; live GitHub push of tools/docs). Commands:
  - `publish_brief.py sample-001 --dry-run` -> Title to upload `Why Systems Beat Motivation`; promise sentence present; exit 0
  - first write -> exit 0
  - second write without `--force` -> exit 1 `already filled`
  - `write_empty_publish` on filled sample -> `kept .../publish.md (already filled)`
  - template-style `(add YouTube description)` -> `publish_is_filled` False
- **Important discovery:** Filled-file detection must key off Description length + Title to upload, not the word "locks" in the disclaimer, or every generated stub looks empty.
- **Blocker:** None for this step. Publishing/TTS/YouTube API remain in BLOCKED.md.
- **Recommended next action:** Caption/subtitle intake stub or narration path conventions. Still no OAuth.

## 2026-08-27T21:10:00+03:00 — Run 008

- **Objective:** Optional title/thumb brief at scaffold time when those files are still empty, reusing `title_thumb_brief` (not a second generator).
- **Result:** Default intake writes heuristic titles + thumb when the template list is empty. Filled titles are kept. `--no-generate` still leaves template `1.` lines untitled.
- **Recommended next action:** `tools/publish_brief.py` stub for description/tags/first comment. No upload.

## 2026-08-27T19:25:00+03:00 — Run 007

- **Objective:** Wire scaffold CLIs so new packets get generated `qa.md` + `research.md` without a second command.
- **Result:** One intake command leaves a draft packet with generated checklist + research stub. Filled `research.md` is kept. `--no-generate` leaves template files.
- **Recommended next action:** Optional title/thumb brief at scaffold time when those files are still empty.

## 2026-08-27T17:10:00+03:00 — Run 006

- **Objective:** Add `tools/research_brief.py` so packets get a research.md stub without scraping the web.

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
