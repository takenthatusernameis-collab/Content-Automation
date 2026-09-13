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
| 2026-09-12 Run 098 | ~76 estimate | 79 | doctor all-packet Queue next footer; contract locks mark-needed skip |
| 2026-09-12 Run 099 | ~75 estimate | 80 | needed --plan WAVE 3 prints doctor + board; doctor stays unmapped |
| 2026-09-12 Run 100 | ~74 estimate | 81 | WAVE 3 reconstructs unmapped doctor.py before the start command |
| 2026-09-12 Run 101 | ~73 estimate | 82 | needed.py doctor.py lists imports; READY only when doctor can run |
| 2026-09-12 Run 102 | ~72 estimate | 83 | doctor reconstruct lists next_topic.py; READY only when WAVE 3 start can run |
| 2026-09-12 Run 103 | ~71 estimate | 84 | needed.py alias appends asked file; next_topic READY no longer lies |
| 2026-09-13 Run 104 | ~70 estimate | 84 | writer prompts name per-segment spoken-word allocation; no new CLI |
| 2026-09-13 Run 105 | ~69 estimate | 84 | template draft.md is the packet save target; no new CLI |

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 105: `videos/_template/draft.md` copies with every new_packet. Empty WORDS, spoken_words comment, not-script.md banner. Writer prompts untouched. Still no packet.
- Run 104: `prompts/script_writer.md` Band landing table (hook 20–35, payoff 40–70, body beat 140–220, CTA 40–80, target ~1200) plus a draft.md spoken_words comment. `prompts/script_expander.md` points at it. needed.py untouched. Still no packet.
- Run 103: `needed.py next_topic.py --missing` lists queue_contract paths plus tools/next_topic.py. Isolated tree without next_topic.py is NOT READY. which_contract.MAP unchanged. Still no packet.
