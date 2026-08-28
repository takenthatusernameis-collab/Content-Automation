# PROGRESS

## Efficiency ledger

| When                 | Human min / video | Automated steps | Notes |
|----------------------|-------------------|-----------------|-------|
| Pre-repo (implied)   | ~290 estimate     | 0               | no process |
| 2026-08-27 Run 001   | ~280 estimate     | 2               | packet scaffold + QA |
| 2026-08-27 Run 002   | ~265 estimate     | 3               | idea card + beat titles + writer prompt |
| 2026-08-27 Run 003   | ~250 estimate     | 4               | title/thumb brief |
| 2026-08-27 Run 004   | ~245 estimate     | 5               | draft QA gate |
| 2026-08-27 Run 005   | ~240 estimate     | 6               | qa.md writer |
| 2026-08-27 Run 006   | ~235 estimate     | 7               | research.md stub |
| 2026-08-27 Run 007   | ~230 estimate     | 8               | generate qa+research on scaffold |
| 2026-08-27 Run 008   | ~225 estimate     | 9               | empty-only titles/thumbs on scaffold |
| 2026-08-27 Run 009   | ~220 estimate     | 10              | empty-only publish.md |
| 2026-08-27 Run 010   | ~215 estimate     | 11              | empty-only captions.md |
| 2026-08-28 Run 011   | ~210 estimate     | 12              | empty-only assets.md |
| 2026-08-28 Run 012   | ~205 estimate     | 12              | format lock |
| 2026-08-28 Run 013   | ~200 estimate     | 13              | empty-only render.md |
| 2026-08-28 Run 014   | ~195 estimate     | 14              | read-only pipeline board |
| 2026-08-28 Run 015   | ~192 estimate     | 15              | read-only next action |
| 2026-08-28 Run 016   | ~187 estimate     | 16              | VO session reading card |
| 2026-08-28 Run 017   | ~182 estimate     | 17              | duration WARN + expand-script |
| 2026-08-28 Run 018   | ~177 estimate     | 18              | expand.md beat budget |
| 2026-08-28 Run 019   | ~172 estimate     | 19              | expand_prompt paste pack; no WORDS rewrite |

Estimate basis (generic 8-min explainer):
- Research 30, idea lock 15, script 60, VO 25, assets 30, edit 90, captions 15, thumb/title 20, QA/upload 15
- Run 018: -5 stop guessing which beat to grow when next_action says expand-script
- Run 019: -5 stop gathering channel + idea + rules + budget + script to brief a writer

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 018: `tools/expand_brief.py` writes `expand.md` per-beat targets; empty-only on scaffold; does not rewrite script.md; sample WORDS unchanged.
- Run 019: `tools/expand_prompt.py` prints a paste-ready expander pack; `prompts/script_expander.md` documents the human loop; does not write script.md; sample WORDS unchanged.
