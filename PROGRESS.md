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
| 2026-08-28 Run 010   | ~215 estimate     | 11              | empty-only captions.md |
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
| 2026-08-28 Run 021   | ~162 estimate     | 21              | set_status evidence gate; board stays read-only |
| 2026-08-28 Run 022   | ~159 estimate     | 22              | hint.py maps next-action codes to copy-paste CLI |
| 2026-09-08 Run 023   | ~156 estimate     | 23              | doctor.py one-command health check |
| 2026-09-09 Run 024   | ~153 estimate     | 23              | human_session.md operator path; no new executable |
| 2026-09-09 Run 025   | ~152 estimate     | 24              | selftest.py fixture contract check |
| 2026-09-09 Run 026   | ~151 estimate     | 24              | selftest runtime PASS via reconstruct; agent_session.md |
| 2026-09-09 Run 027   | ~148 estimate     | 25              | topic queue + read-only next_topic.py |
| 2026-09-09 Run 028   | ~146 estimate     | 26              | predicted path + mark_topic folder gate |

Estimate basis (generic 8-min explainer):
- Research 30, idea lock 15, script 60, VO 25, assets 30, edit 90, captions 15, thumb/title 20, QA/upload 15
- Run 027: -3 stop inventing the first working title from a blank page
- Run 028: -2 stop guessing NNN-slug and hand-editing the queue status column

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 019: `tools/expand_prompt.py` prints a paste-ready expander pack; does not write script.md.
- Run 020: `tools/apply_script.py` dry-runs then optionally writes a human-pasted script to a non-fixture packet; refuses sample-001 and expand_prompt stdout; optional derived refresh; no status bump.
- Run 021: `tools/set_status.py` dry-runs then optionally writes packet.md status; refuses fixture promote, skip-ahead, duration-short ready_for_vo, and later statuses without disk evidence.
- Run 022: `tools/hint.py` prints the copy-paste command for the current next_action code; read-only; `--write` only as a commented follow-up; fixture lock on sample-001.
- Run 023: `tools/doctor.py` prints one health block per packet (gate, drift, duration WARN, next-action, hint CLI); read-only; `--strict` on FAIL/drift only.
- Run 024: `docs/human_session.md` is the operator path; README and production rules point at it. No new writer. Fixture freeze restated in one place a human can follow without the agent prompt.
- Run 025: `tools/selftest.py` asserts sample-001 PASS + duration WARN + expand-script + no live `--write` + apply/set_status fixture refuse. Read-only. Not a second human start command.
- Run 026: Reconstructed tools + sample-001 via GitHub download_url; `python3 tools/selftest.py` → SELFTEST PASS, exit 0, 153 words. `docs/agent_session.md` records the reconstruct list and last verified output.
- Run 027: `docs/topic_queue.md` holds five on-niche working titles. `tools/next_topic.py` prints the first unused queued row and scaffold commands. Read-only. Does not create packets or WORDS.
- Run 028: `tools/mark_topic.py` marks a queue row used only when a matching non-fixture folder exists. Dry-run default. `next_topic.py` prints predicted `videos/002-slug`. `new_packet.py` counts `sample-001-*` as id 001.
