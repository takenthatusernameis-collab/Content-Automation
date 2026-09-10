# PROGRESS

## Efficiency ledger

| When                 | Human min / video | Automated steps | Notes |
|----------------------|-------------------|-----------------|-------|
| 2026-09-09 Run 027   | ~148 estimate     | 25              | topic queue + read-only next_topic.py |
| 2026-09-09 Run 028   | ~146 estimate     | 26              | predicted path + mark_topic folder gate |
| 2026-09-09 Run 029   | ~145 estimate     | 27              | queue_lib + new_packet reprints Q-id |
| 2026-09-09 Run 030   | ~144 estimate     | 28              | queue_status board for queue vs folder |
| 2026-09-09 Run 031   | ~143 estimate     | 29              | queue_status --strict + PACKET column |
| 2026-09-09 Run 032   | ~142 estimate     | 30              | queue_contract locks board codes and exits |
| 2026-09-09 Run 033   | ~141 estimate     | 31              | write_path_contract locks apply/set_status gates |
| 2026-09-09 Run 034   | ~140 estimate     | 32              | scaffold_contract locks new_packet mark-handoff |
| 2026-09-09 Run 035   | ~139 estimate     | 33              | which_contract routes tool edits to the right lock |
| 2026-09-09 Run 036   | ~138 estimate     | 34              | router_contract locks the tool→contract map |
| 2026-09-10 Run 037   | ~137 estimate     | 35              | needed.py prints reconstruct paths per contract |
| 2026-09-10 Run 038   | ~136 estimate     | 36              | needed.py --missing + FALLBACK_ALIAS |
| 2026-09-10 Run 039   | ~135 estimate     | 37              | needed.py --bootstrap first-fetch set |
| 2026-09-10 Run 040   | ~134 estimate     | 38              | needed.py --plan fetch waves |
| 2026-09-10 Run 041   | ~133 estimate     | 39              | needed.py --plan WAVE 3 operator command |
| 2026-09-10 Run 042   | ~132 estimate     | 40              | needed.py --plan WAVE 3 reconstruct command |
| 2026-09-10 Run 043   | ~131 estimate     | 40              | human_session first-video commands restored |
| 2026-09-10 Run 044   | ~130 estimate     | 40              | Q1 title/path pin + idea.md pre-expand edit |
| 2026-09-10 Run 045   | ~129 estimate     | 40              | new_packet reprints idea topic + mechanism |

Earlier rows 001-026 remain in prior commits.

Estimate basis (generic 8-min explainer):
- Run 045: -1 stop looking up the queue one_line after scaffold

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 045: `new_packet.idea_followup` reprints topic + matching queue one_line after scaffold. Does not write idea.md. SCAFFOLD CONTRACT PASS on `/tmp/ca`.
- Run 044: `docs/human_session.md` pins Q1 title and `videos/002-stop-deciding-what-to-work-on-every-morning`, plus idea.md problem/mechanism edit before expand. `prompts/script_expander.md` repeats the idea.md gate. No packet folder. No needed.py change.
- Run 043: `docs/human_session.md` again lists expand_prompt, apply_script dry-run/--write --refresh, validate, set_status ready_for_vo, and vo_session for the first non-fixture packet. Reconstruct-loop flagged. No needed.py change.
- Run 042: `needed.py --plan` WAVE 3 prints `needed.py queue_status.py --missing` before the operator line. Still no queue file dump. Still unmapped. Local PASS on `/tmp/ca/tools`.
