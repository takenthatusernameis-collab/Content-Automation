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

Estimate basis (generic 8-min explainer):
- Run 060: -1 stop inventing FILE after PASTE READY apply dry-run
- Run 059: -1 stop hunting apply_script after PASTE READY expand_prompt
- Run 058: -1 stop replacing PATH after a default reprint
- Run 057: -1 stop hunting --block after an incomplete --check
- Run 056: -1 stop hunting expand_prompt after a confirmed paste

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 060: `idea_brief.py --check` PASTE READY prints dry-run `python3 tools/apply_script.py PATH --from PATH/draft.md` and a save-to-draft.md line. Still does not write idea.md or print `--write`. idea_brief_contract requires draft_path and that apply line. Unmapped. IDEA BRIEF CONTRACT PASS on tempfile. No packet folder.
- Run 059: `idea_brief.py --check` PASTE READY prints dry-run `python3 tools/apply_script.py PATH --from FILE` after expand_prompt.
