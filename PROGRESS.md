# PROGRESS

## Efficiency ledger

| When                 | Human min / video | Automated steps | Notes |
|----------------------|-------------------|-----------------|-------|
| 2026-09-09 Run 027   | ~148 estimate     | 25              | topic queue + read-only next_topic.py |
| 2026-09-09 Run 028   | ~146 estimate     | 26              | predicted path + mark_topic folder gate |
| 2026-09-09 Run 029   | ~145 estimate     | 27              | queue_lib + new_packet reprints Q-id |
| 2026-09-09 Run 030   | ~144 estimate     | 28              | queue_status board for queue vs folder |
| 2026-09-09 Run 031   | ~143 estimate     | 29              | queue_status --strict + PACKET column |

Earlier rows 001-026 remain in prior commits.

Estimate basis (generic 8-min explainer):
- Run 031: -1 stop guessing whether a folder is still draft after a glance at the queue

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 028: `tools/mark_topic.py` marks a queue row used only when a matching non-fixture folder exists. Dry-run default.
- Run 029: `tools/queue_lib.py` is the single source for slugify/next_id/parse/match. `new_packet.py` reprints the matching mark_topic dry-run after scaffold and does not write the queue.
- Run 030: `tools/queue_status.py` is a read-only board. Codes: ok-queued, mark-needed, missing-folder, ok-used, parked, fixture-refuse. Prints dry-run mark_topic only when a folder already exists.
- Run 031: same board prints packet.md status when a folder exists. `--strict` exits 2 on missing-folder, 1 on mark-needed/unknown-status, 0 when clean. Default still exit 0.
