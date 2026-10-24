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
`tools/card_generator.py` writes local PNGs. It marks ready only with `--mark-ready` after files exist.
`tools/card_text_suggest.py` — derives 2-3 short (<=5 word) on-screen phrase candidates from the Need column. No file writes. Use before building cards.

## Generate locally

Requires Pillow. Does not commit PNGs.

```bash
python3 tools/card_text_suggest.py PATH
python3 tools/card_generator.py PATH --write-manifest
python3 tools/card_generator.py PATH --inspect-only
```

`--mark-ready` only after inspect-only reports every planned file `yes` at 1920x1080.

## Editor tracks
Match `docs/editor.md`:
- text-cards go on `TITLES`
- diagrams go on `DIAGRAM`
- b-roll is optional and is not generated here

## After cards exist locally

Operator copy lives in `docs/human_session.md` step 6.

```bash
python3 tools/render_brief.py PATH --force
python3 tools/qa_checklist.py PATH --force
```

Refresh presence only. Do not mark a row `ready` from this page. Do not commit the pngs.

## Out of scope
No Unsplash/Pexels/Drive fetch. No ffmpeg stills. No thumbnail PSD.
