# PROGRESS

## Efficiency ledger

| When                 | Human min / video | Automated steps | Notes |
|----------------------|-------------------|-----------------|-------|
| 2026-09-09 Run 027   | ~148 estimate     | 25              | topic queue + read-only next_topic.py |
| 2026-09-09 Run 034   | ~140 estimate     | 32              | scaffold_contract locks new_packet mark-handoff |
| 2026-09-10 Run 042   | ~132 estimate     | 40              | needed.py --plan WAVE 3 reconstruct command |
| 2026-09-10 Run 043   | ~131 estimate     | 40              | human_session first-video commands restored |
| 2026-09-10 Run 044   | ~130 estimate     | 40              | Q1 title/path pin + idea.md pre-expand edit |
| 2026-09-10 Run 045   | ~129 estimate     | 40              | new_packet reprints idea topic + mechanism |
| 2026-09-10 Run 046   | ~128 estimate     | 40              | expand_prompt refuses blank mechanism |
| 2026-09-10 Run 047   | ~127 estimate     | 40              | next_action/hint fill-idea before expand |
| 2026-09-10 Run 048   | ~126 estimate     | 41              | idea_gate_contract locks fill-idea map |
| 2026-09-10 Run 049   | ~125 estimate     | 42              | operator_pin_contract locks Q1 pin vs queue |
| 2026-09-10 Run 050   | ~124 estimate     | 42              | operator_pin also locks Q1 problem paste line |
| 2026-09-10 Run 051   | ~123 estimate     | 42              | new_packet reprints locked Q1 problem |
| 2026-09-10 Run 052   | ~122 estimate     | 43              | idea_brief recovers the three-field paste |
| 2026-09-10 Run 053   | ~121 estimate     | 44              | idea_brief_contract locks no-write reprint |
| 2026-09-10 Run 054   | ~120 estimate     | 45              | idea_brief --block prints paste-ready idea.md body |
| 2026-09-10 Run 055   | ~119 estimate     | 46              | idea_brief --check confirms paste without writing |
| 2026-09-10 Run 056   | ~118 estimate     | 47              | --check PASTE READY prints exact expand_prompt command |
| 2026-09-10 Run 057   | ~117 estimate     | 48              | --check PASTE INCOMPLETE prints exact --block command |
| 2026-09-10 Run 058   | ~116 estimate     | 49              | default idea_brief reprint prints exact --check command |
| 2026-09-11 Run 059   | ~115 estimate     | 50              | PASTE READY prints apply_script dry-run --from FILE |
| 2026-09-11 Run 060   | ~114 estimate     | 51              | PASTE READY apply dry-run uses PATH/draft.md |
| 2026-09-11 Run 061   | ~113 estimate     | 52              | apply_script missing --from exits 2 with draft.md hint |
| 2026-09-11 Run 062   | ~112 estimate     | 53              | write_path_contract locks missing --from CLI exit 2 |
| 2026-09-11 Run 063   | ~111 estimate     | 54              | write_path_contract locks dry-run --from existing draft.md |
| 2026-09-11 Run 064   | ~110 estimate     | 55              | write_path_contract locks set_status CLI blocked ready_for_vo |

Estimate basis (generic 8-min explainer):
- Run 064: -1 stop a future write-before-check regression from promoting packet.md while WORDS are short or the packet is the fixture
- Run 063: -1 stop a future default-write regression from turning the printed apply dry-run into a silent script.md write
- Run 062: -1 stop a future CLI regression from turning the printed apply line back into a traceback
- Run 061: -1 stop decoding a traceback when the printed apply line is run before draft.md exists

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 064: `write_path_contract.py` subprocess-runs `set_status.py --to ready_for_vo` dry-run, blocked `--write`, and fixture `--write`. Expects exit 1, BLOCKED, packet.md unchanged. WRITE PATH CONTRACT PASS on reconstructed tree.
- Run 063: `write_path_contract.py` subprocess-runs `apply_script.py --from PATH/draft.md` when that file exists. Expects exit 0, Dry-run only, no script.md write.
- Run 062: `write_path_contract.py` subprocess-runs `apply_script.py --from` on a missing file. Expects exit 2, draft.md hint, no script.md write.
- Run 061: `apply_script.py --from` on a missing path exits 2 and prints a draft.md save hint. Does not write script.md.
