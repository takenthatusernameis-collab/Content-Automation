# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-09-09 Run 027 | ~148 estimate | 25 | topic queue + read-only next_topic.py |
| 2026-09-11 Run 061 | ~113 estimate | 52 | apply_script missing --from exits 2 with draft.md hint |
| 2026-09-11 Run 079 | ~95 estimate | 70 | prove_locks.py runs guard then words_contract then verify in one command |
| 2026-09-12 Run 088 | ~86 estimate | 71 | production_rules handoff names idea_brief, words.py, prove_locks |
| 2026-09-12 Run 089 | ~85 estimate | 71 | idea_brief --block fills the whole idea.md template |

Estimate basis (generic 8-min explainer):
- Run 089: -1 stop a second invent pass for viewer / why now / related after a three-field --check
- Runs 084–088: -1 each for naming idea_brief on boards and operator pages after a folder exists

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 089: idea_brief --block pastes topic, viewer, problem, mechanism, why now, and related. --check still gates three fields. extras print INFO. No new file. Still does not write idea.md.
- Run 088: docs/production_rules.md Packet, Script, and Human handoff name idea_brief --block / paste / --check, words.py on PATH/draft.md, and prove_locks.py after a high-risk write.
