# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-09-09 Run 027 | ~148 estimate | 25 | topic queue + read-only next_topic.py |
| 2026-09-11 Run 079 | ~95 estimate | 70 | prove_locks.py one command |
| 2026-09-13 Run 104 | ~70 estimate | 84 | writer prompts name per-segment spoken-word allocation; no new CLI |
| 2026-09-13 Run 105 | ~69 estimate | 84 | template draft.md is the packet save target; no new CLI |
| 2026-09-13 Run 106 | ~68 estimate | 84 | new_packet reprints draft.md overwrite path; scaffold_contract locks it |
| 2026-09-13 Run 107 | ~67 estimate | 84 | empty-script expand.md prints Band-landing targets; no new CLI |

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 107: `expand_brief.py` prints hook/payoff/beat/CTA Target rows from headings when WORDS are empty. Beats clamp to 140-220. Four empty template beats target 220 (land ~1010). No new CLI. Still no packet.
- Run 106: `new_packet.draft_followup()` reprints the copied draft.md overwrite path and not-script.md rule. `scaffold_contract` locks the reprint. No new CLI. Still no packet.
- Run 105: `videos/_template/draft.md` copies with every new_packet. Empty WORDS, spoken_words comment, not-script.md banner. Writer prompts untouched. Still no packet.
- Run 104: `prompts/script_writer.md` Band landing table plus a draft.md spoken_words comment. `prompts/script_expander.md` points at it. needed.py untouched. Still no packet.
