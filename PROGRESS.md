# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-09-09 Run 027 | ~148 estimate | 25 | topic queue + read-only next_topic.py |
| 2026-09-11 Run 061 | ~113 estimate | 52 | apply_script missing --from exits 2 with draft.md hint |
| 2026-09-11 Run 079 | ~95 estimate | 70 | prove_locks.py runs guard then words_contract then verify in one command |
| 2026-09-12 Run 088 | ~86 estimate | 71 | production_rules handoff names idea_brief, words.py, prove_locks |
| 2026-09-12 Run 089 | ~85 estimate | 71 | idea_brief --block fills the whole idea.md template |
| 2026-09-12 Run 090 | ~84 estimate | 71 | expand_prompt prints parsed idea locks; refuse names idea_brief |
| 2026-09-12 Run 091 | ~83 estimate | 72 | apply dry-run prints idea-lock INFO; script_writer uses draft.md |

Estimate basis (generic 8-min explainer):
- Run 091: -1 stop apply OK on a draft that never names the pasted mechanism
- Run 090: -1 stop a generic expand that ignores the pasted idea.md fields
- Run 089: -1 stop a second invent pass for viewer / why now / related after a three-field --check
- Runs 084–088: -1 each for naming idea_brief on boards and operator pages after a folder exists

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 091: apply_script.py idea_lock_notes() prints INFO for mechanism / topic token overlap. Never blocks --write. prompts/script_writer.md saves PATH/draft.md and runs words.py / apply dry-run.
- Run 090: expand_prompt.py Idea locks section parses topic / viewer / problem / mechanism / why now / related. Refuse path names idea_brief --block/--check. script_expander.md uses PATH/draft.md and words.py.
- Run 089: idea_brief --block pastes topic, viewer, problem, mechanism, why now, and related. --check still gates three fields. extras print INFO. No new file. Still does not write idea.md.
- Run 088: docs/production_rules.md Packet, Script, and Human handoff name idea_brief --block / paste / --check, words.py on PATH/draft.md, and prove_locks.py after a high-risk write.
