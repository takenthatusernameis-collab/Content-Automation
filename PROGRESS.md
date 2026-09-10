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

Earlier rows remain in prior commits.

Estimate basis (generic 8-min explainer):
- Run 053: -1 stop a future run from turning idea_brief into a silent idea.md writer
- Run 052: -1 stop hunting human_session + queue when scaffold stdout is gone
- Run 051: -1 stop joining operator page + queue after scaffold to assemble idea.md
- Run 050: -1 stop a future run from dropping the idea.md problem field off the only human page
- Run 049: -1 stop a future run from shipping a human_session that no longer matches Q1

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 053: `tools/idea_brief_contract.py` locks idea_brief as read-only reprint recover (source note, human_session command, Q1 three-field stdout, unchanged idea.md hash). Unmapped. IDEA BRIEF CONTRACT PASS on tempfile. No packet folder.
- Run 052: `tools/idea_brief.py` reprints current vs suggested idea.md fields for an existing packet. Reuses `new_packet.idea_followup`. Does not write idea.md. human_session documents the recover command. No packet folder.
- Run 051: `new_packet.idea_followup` reprints Q1 problem from `Q1_PROBLEM`. `scaffold_contract` requires that line. SCAFFOLD CONTRACT PASS. No packet folder. No needed.py change. Still does not write idea.md.
- Run 050: `operator_pin_contract.py` requires the Q1 problem sentence on human_session. AGENT session lists unmapped locks. OPERATOR PIN CONTRACT PASS. No packet folder. No needed.py change.
