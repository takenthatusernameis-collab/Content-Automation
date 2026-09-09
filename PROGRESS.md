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

Earlier rows 001-026 remain in prior commits.

Estimate basis (generic 8-min explainer):
- Run 035: -1 stop scanning NEXT/agent_session for which contract to run after a tools/ edit

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 028: `tools/mark_topic.py` marks a queue row used only when a matching non-fixture folder exists. Dry-run default.
- Run 029: `tools/queue_lib.py` is the single source for slugify/next_id/parse/match. `new_packet.py` reprints the matching mark_topic dry-run after scaffold and does not write the queue.
- Run 030: `tools/queue_status.py` is a read-only board.
- Run 031: same board prints packet.md status when a folder exists. `--strict` opt-in.
- Run 032: `tools/queue_contract.py` is the queue equivalent of selftest. Temp tree only. Runtime PASS.
- Run 033: `tools/write_path_contract.py` is the write-path equivalent of selftest. Temp tree only. Runtime PASS.
- Run 034: `tools/scaffold_contract.py` locks new_packet mark_followup (dry-run then commented --write), no subprocess queue write, empty `1.` untitled, next_id sample-001 => 002. Runtime PASS on `/tmp/ca`.
- Run 035: `tools/which_contract.py` maps edited tool basenames to the contract command. Read-only. `--run` SKIP if deps missing.
