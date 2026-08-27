# PROGRESS

## Efficiency ledger

| When                 | Human min / video | Automated steps | Notes |
|----------------------|-------------------|-----------------|-------|
| Pre-repo (implied)   | ~290 estimate     | 0               | no process |
| 2026-08-27 Run 001   | ~280 estimate     | 2               | packet scaffold + QA |
| 2026-08-27 Run 002   | ~265 estimate     | 3               | idea card + beat titles + writer prompt |
| 2026-08-27 Run 003   | ~250 estimate     | 4               | title/thumb brief; ~15 min off blank title/thumb start |
| 2026-08-27 Run 004   | ~245 estimate     | 5               | draft QA gate; empty-field parser fix |
| 2026-08-27 Run 005   | ~240 estimate     | 6               | qa.md writer; editor human ticks listed |
| 2026-08-27 Run 006   | ~235 estimate     | 7               | research.md stub; digit scan + overwrite guard |
| 2026-08-27 Run 007   | ~230 estimate     | 8               | generate qa+research on scaffold; title-list newline fix |
| 2026-08-27 Run 008   | ~225 estimate     | 9               | empty-only titles/thumbs on scaffold; qa after titles |
| 2026-08-27 Run 009   | ~220 estimate     | 10              | empty-only publish.md (description/tags/comment) |
| 2026-08-27 Run 010   | ~215 estimate     | 11              | empty-only captions.md cues from WORDS |
| 2026-08-28 Run 011   | ~210 estimate     | 12              | empty-only assets.md cards from VISUAL |

Estimate basis (generic 8-min explainer):
- Research 30, idea lock 15, script 60, VO 25, assets 30, edit 90, captions 15, thumb/title 20, QA/upload 15
- Run 011: -5 first card filename list from VISUAL; human still builds the cards

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 010: `tools/caption_brief.py` writes `captions.md`; `docs/narration.md` path rules; scaffold empty-only; no Whisper.
- Run 011: `tools/asset_brief.py` writes `assets.md`; `docs/assets.md` filename rules; scaffold empty-only; no stock.
