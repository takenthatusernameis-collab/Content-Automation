# Asset conventions

Text-card first. No stock API. No image download from this repo.

## Where files live
- Packet list: `videos/NNN-slug/assets.md` (this is the intake stub)
- Local card exports: `videos/NNN-slug/cards/` (usually not committed)
- Do not invent binaries in git to make a row look ready

## Filename pattern
`cards/{beat}-{short-slug}.png`

Beat prefixes:
- `hook`
- `payoff`
- `beat1` … `beatN`
- `cta`

Slug is lowercase words from the VISUAL line, hyphenated, short.

## Types
- `text-card` — on-screen words, same promise as the beat
- `diagram` — simple board, checklist, contrast, arrow

Heuristic only. A human may retype the Type cell.

## Status values
- `planned` — listed from VISUAL, file not made
- `ready` — file exists locally for the editor
- `dropped` — VISUAL line will not get a card

`tools/asset_brief.py` always writes `planned`. It does not mark ready.

## Editor tracks
Match `docs/editor.md`:
- text-cards go on `TITLES`
- diagrams go on `DIAGRAM`
- b-roll is optional and is not generated here

## Out of scope
No Unsplash/Pexels/Drive fetch. No ffmpeg stills. No thumbnail PSD.
