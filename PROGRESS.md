# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-09-09 Run 027 | ~148 estimate | 25 | topic queue + read-only next_topic.py |
| 2026-09-11 Run 079 | ~95 estimate | 70 | prove_locks.py one command |
| 2026-09-12 Run 089 | ~85 estimate | 71 | idea_brief --block fills the whole idea.md template |
| 2026-09-12 Run 090 | ~84 estimate | 71 | expand_prompt prints parsed idea locks |
| 2026-09-12 Run 091 | ~83 estimate | 72 | apply dry-run prints idea-lock INFO |
| 2026-09-12 Run 092 | ~82 estimate | 73 | idea_lock.py prints the same INFO before apply |
| 2026-09-12 Run 093 | ~81 estimate | 74 | words.py prints idea-lock INFO; extra CLI optional |
| 2026-09-12 Run 094 | ~80 estimate | 75 | words_contract locks IN BAND --strict exit 0 + INFO |
| 2026-09-12 Run 095 | ~79 estimate | 76 | idea_brief --queue reprints paste before scaffold |

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 095: idea_brief.py --queue ID reprints paste_block from topic_queue without a packet folder. Does not write idea.md. --check still requires a folder.
- Run 094: words_contract.py IN_BAND_DRAFT must print Result: IN BAND and INFO, and --strict must exit 0. Still unmapped.
- Run 093: words.py print_idea_lock_notes() imports apply_script.idea_lock_notes after Next. INFO does not change --strict. words_contract checks the marker and that INFO prints.
- Run 092: tools/idea_lock.py wraps idea_lock_notes. Exit 0. Unmapped.
- Run 091: apply_script.py idea_lock_notes() prints INFO for mechanism / topic token overlap. Never blocks --write.
- Run 090: expand_prompt.py Idea locks section. Refuse path names idea_brief --block/--check.
- Run 089: idea_brief --block pastes six fields. --check still gates three.
