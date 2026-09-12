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
| 2026-09-12 Run 096 | ~78 estimate | 77 | idea_brief_contract locks --queue Q1 / missing / --check combo |
| 2026-09-12 Run 097 | ~77 estimate | 78 | queue printers print --queue; contract locks first ok-queued id |

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 097: queue_status.py and next_topic.py print idea_brief --queue ID before scaffold. queue_contract requires --queue Q2 on the tempfile board and forbids --queue Q1 there (mark-needed). Still no packet.
- Run 096: idea_brief_contract.py queue_locks() requires --queue Q1 six-field paste exit 0, missing id exit 2, --queue --check exit 2, and no predicted folder created. Still unmapped.
- Run 095: idea_brief.py --queue ID reprints paste_block from topic_queue without a packet folder. Does not write idea.md. --check still requires a folder.
- Run 094: words_contract.py IN_BAND_DRAFT must print Result: IN BAND and INFO, and --strict must exit 0. Still unmapped.
