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

Earlier rows 001-026 remain in prior commits.

Estimate basis (generic 8-min explainer):
- Run 033: -1 stop re-checking apply_script/set_status refuse/allow by hand after a write-tool edit

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 028: `tools/mark_topic.py` marks a queue row used only when a matching non-fixture folder exists. Dry-run default.
- Run 029: `tools/queue_lib.py` is the single source for slugify/next_id/parse/match. `new_packet.py` reprints the matching mark_topic dry-run after scaffold and does not write the queue.
- Run 030: `tools/queue_status.py` is a read-only board.
- Run 031: same board prints packet.md status when a folder exists. `--strict` opt-in.
- Run 032: `tools/queue_contract.py` is the queue equivalent of selftest. Temp tree only. Runtime PASS.
- Run 033: `tools/write_path_contract.py` is the write-path equivalent of selftest. Temp tree only. Asserts apply fixture/prompt/hook refuse, apply allow on a non-fixture body, set_status duration/skip/fixture blocks. Runtime PASS this run.
