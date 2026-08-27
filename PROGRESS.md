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

Estimate basis (generic 8-min explainer):
- Research 30, idea lock 15, script 60, VO 25, assets 30, edit 90, captions 15, thumb/title 20, QA/upload 15
- Run 001: -10 setup/QA
- Run 002: -15 idea structuring + beat naming (still need WORDS)
- Run 003: -15 first title/thumb draft (human still picks Primary and designs the image)
- Run 004: -5 false-fail triage on intake packets + clearer edit naming
- Run 005: -5 not rewriting qa boxes; human still does VO/cards/export ticks
- Run 006: -5 research file structure + reminder; human still verifies any real source
- Run 007: -5 no extra CLI after `new_idea`/`new_packet` for stubs; intake draft gate no longer false-fails empty `1.` title lines
- Run 008: -5 no extra CLI for first title/thumb brief; human still locks Primary and designs the image
- Run 009: -5 first description/tags/pinned-comment draft; human still edits and uploads

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 001: reusable video packet, validator, production rules, system memory.
- Run 002: working-niche lock, idea intake CLI, script-writer prompt.
- Run 003: heuristic title + thumbnail brief CLI with field self-check matching `validate_packet.py`.
- Run 004: `validate_packet.py --draft` intake gate; one-line field parser; `docs/editor.md` conventions.
- Run 005: `tools/qa_checklist.py` writes mechanical + human `qa.md`; no scores.
- Run 006: `tools/research_brief.py` writes `research.md` stub from idea/script; no scrape; filled-file guard.
- Run 007: `tools/after_scaffold.py` + `--no-generate` opt-out on scaffold CLIs; `titles_from` ignores blank numbered lines.
- Run 008: scaffold reuses `title_thumb_brief` renderers when titles are empty; qa runs after so mechanical boxes match.
- Run 009: `tools/publish_brief.py` writes `publish.md`; scaffold empty-only; no YouTube API.
