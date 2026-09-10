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

Earlier rows remain in prior commits.

Estimate basis (generic 8-min explainer):
- Run 048: -1 stop a future run from restoring expand-first on blank idea.md

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 048: `tools/idea_gate_contract.py` locks blank/filled mechanism + fill-idea hint map on tempfile. IDEA GATE CONTRACT PASS. Unmapped in which_contract. No packet folder. No needed.py change.
- Run 047: `next_action.py` code `fill-idea` when idea.md mechanism is blank. `hint.py` maps it to a paste comment + doctor, not expand_prompt. HINT + NEXT_ACTION UNIT PASS. Fixture path unchanged. No packet folder. No needed.py change.
- Run 046: `expand_prompt.py` exits 2 on blank / template-default idea.md mechanism. `scaffold_contract.py` locks idea_followup reprint. IDEA GATE UNIT PASS + SCAFFOLD CONTRACT PASS on `/tmp/ca`.
- Run 045: `new_packet.idea_followup` reprints topic + matching queue one_line after scaffold. Does not write idea.md.
- Run 044: `docs/human_session.md` pins Q1 title and `videos/002-stop-deciding-what-to-work-on-every-morning`, plus idea.md problem/mechanism edit before expand.
