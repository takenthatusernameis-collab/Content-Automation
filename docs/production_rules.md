# Production rules

Apply to every video packet. QA checks what can be checked mechanically.

## Packet
- One video = one folder `videos/NNN-slug/`
- Required files: `packet.md`, `idea.md`, `script.md`, `titles.md`, `thumbnail.md`, `qa.md`
- Optional: `research.md`, `assets.md`, `narration.md`, `publish.md`, `captions.md`, `render.md`
- Status in `packet.md` must be one of: `draft`, `ready_for_vo`, `ready_for_edit`, `ready_to_publish`, `published`, `abandoned`
- Field values stay on the same line as the key
- `python3 tools/new_idea.py "topic"` / `python3 tools/new_packet.py "title"` copy the template and write generated titles/thumbs (if empty), `publish.md` (if empty), `captions.md` (if empty), `assets.md` (if empty), `render.md` (if empty), `research.md`, and `qa.md` unless `--no-generate`
- `python3 tools/pipeline_status.py` is the read-only board across packets. It does not write files.

## Format
- Default packet format is `explainer-6-10min` (face-free).
- Timing, holds, end-screen reserve, and named export paths: `docs/format.md`.
- Editor tracks: `docs/editor.md`. Do not treat named paths as existing files.
- `python3 tools/render_brief.py PATH` writes `render.md` exists-vs-missing for those names.
- A `missing` row is the expected state until a human puts a file on disk. Do not invent media.
- `--force` is required to replace a filled `render.md`.
- Scaffold writes render.md only when empty.

## Script
- Hook in the first 8–12 seconds of spoken words (about 20–35 words)
- State the viewer payoff before beat 2
- 4–7 beats after the hook
- One primary CTA
- No unverifiable statistics; if a number is used, cite source in `research.md`
- Working-niche tone: specific, calm, operational. No hustle slogans.

## Research
- `python3 tools/research_brief.py PATH` writes the stub (topic seed, source slots, spoken-number scan).
- Listing a URL is not verification. Do not scrape pages into Facts.
- `--source "line"` adds a human-provided pointer. `--force` is required to replace a filled file.
- Digit scan looks only at WORDS blocks (not `0:00` / `Beat 1` headings).
- Scaffold already runs this stub writer; do not treat the generated file as verified research.

## Titles
- Provide at least 5 options
- One must be under 50 characters
- No ALL CAPS words except a single acronym
- Numbered options stay on the same line as `1.` — blank `1.` is not a title
- Scaffold fills titles/thumbs from `title_thumb_brief.py` only when `titles.md` parses empty

## Thumbnail
- One sentence of on-image text, max 5 words
- Describe subject, contrast, and what *not* to include
- Must match the chosen title promise

## Publish metadata
- `python3 tools/publish_brief.py PATH` writes `publish.md`: title to upload, description, tags, first comment.
- No YouTube API call. A filled file is not a published video.
- `--force` is required to replace a filled `publish.md`.
- Scaffold writes publish.md after titles (so Primary exists) only when the file is still a placeholder.

## Captions and narration
- `python3 tools/caption_brief.py PATH` writes `captions.md` cues from script WORDS at 150 wpm.
- Not Whisper. Not an SRT. Estimated times are not aligned to a take.
- `--force` is required to replace a filled `captions.md`.
- Scaffold writes captions.md only when empty.
- VO file names live in `docs/narration.md`. Do not commit raw session dumps by default.

## Assets
- `python3 tools/asset_brief.py PATH` writes `assets.md` card rows from script VISUAL lines.
- Suggested filenames only. Not stock shopping. Not a download. Status stays `planned`.
- `--force` is required to replace a filled `assets.md`.
- Scaffold writes assets.md only when empty.
- Filename rules: `docs/assets.md`. Editor tracks: `docs/editor.md`.

## QA gates
- `python3 tools/validate_packet.py PATH` — publish/completeness. Empty WORDS fail.
- `python3 tools/validate_packet.py --draft PATH` — intake/structure. Empty WORDS/titles/thumb are incomplete, not fail.
- `python3 tools/qa_checklist.py PATH` — writes `qa.md` mechanical boxes from files + human ticks from editor conventions. Never invents scores or auto-checks VO/cards/export/captions.
- `python3 tools/pipeline_status.py` — read-only: status + gate + disk + drift. `--strict` fails on FAIL or drift.
- A hook that has words but is outside 20–35 still fails in both validate gates.
- Status drift: `ready_for_vo` needs a PASS script gate; `ready_for_edit` needs selected VO on disk; `ready_to_publish` / `published` need VO + export. Do not bump status to hide missing files.

## Human handoff
Anything a human must still do is listed under `Remaining human work` in `packet.md`.
Editing conventions: `docs/editor.md`.
Format timing: `docs/format.md`.
Narration paths: `docs/narration.md`.
Asset filenames: `docs/assets.md`.
Render presence: packet `render.md`.
Human visual/audio ticks live in `qa.md` under **Human**.
