# PROGRESS

## Efficiency ledger

| When                 | Human min / video | Automated steps | Notes |
|----------------------|-------------------|-----------------|-------|
| Pre-repo (implied)   | ~290 estimate     | 0               | no process |
| 2026-08-27 Run 001   | ~280 estimate     | 2               | packet scaffold + QA |
| 2026-08-27 Run 002   | ~265 estimate     | 3               | idea card + beat titles + writer prompt |
| 2026-08-27 Run 003   | ~250 estimate     | 4               | title/thumb brief; ~15 min off blank title/thumb start |
| 2026-08-27 Run 004   | ~245 estimate     | 5               | draft QA gate; empty-field parser fix |

Estimate basis (generic 8-min explainer):
- Research 30, idea lock 15, script 60, VO 25, assets 30, edit 90, captions 15, thumb/title 20, QA/upload 15
- Run 001: -10 setup/QA
- Run 002: -15 idea structuring + beat naming (still need WORDS)
- Run 003: -15 first title/thumb draft (human still picks Primary and designs the image)
- Run 004: -5 false-fail triage on intake packets + clearer edit naming

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 001: reusable video packet, validator, production rules, system memory.
- Run 002: working-niche lock, idea intake CLI, script-writer prompt.
- Run 003: heuristic title + thumbnail brief CLI with field self-check matching `validate_packet.py`.
- Run 004: `validate_packet.py --draft` intake gate; one-line field parser; `docs/editor.md` conventions.
