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
| 2026-08-28 Run 020   | ~167 estimate     | 20              | apply_script paste-back gate; no fixture write |

Estimate basis (generic 8-min explainer):
- Research 30, idea lock 15, script 60, VO 25, assets 30, edit 90, captions 15, thumb/title 20, QA/upload 15
- Run 019: -5 stop gathering channel + idea + rules + budget + script to brief a writer
- Run 020: -5 stop hand-swapping script.md and refreshing expand/vo/captions after a paste-back

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 019: `tools/expand_prompt.py` prints a paste-ready expander pack; does not write script.md.
- Run 020: `tools/apply_script.py` dry-runs then optionally writes a human-pasted script to a non-fixture packet; refuses sample-001 and expand_prompt stdout; optional derived refresh; no status bump.
