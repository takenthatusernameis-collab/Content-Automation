# PROGRESS

## Efficiency ledger

| When                 | Human min / video | Automated steps | Notes |
|----------------------|-------------------|-----------------|-------|
| 2026-09-09 Run 027   | ~148 estimate     | 25              | topic queue + read-only next_topic.py |
| 2026-09-09 Run 028   | ~146 estimate     | 26              | predicted path + mark_topic folder gate |
| 2026-09-09 Run 029   | ~145 estimate     | 27              | queue_lib + new_packet reprints Q-id |

Earlier rows 001-026 remain in prior commits.

Estimate basis (generic 8-min explainer):
- Run 029: -1 stop looking up the Q-id after scaffold

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 028: `tools/mark_topic.py` marks a queue row used only when a matching non-fixture folder exists. Dry-run default.
- Run 029: `tools/queue_lib.py` is the single source for slugify/next_id/parse/match. `new_packet.py` reprints the matching mark_topic dry-run after scaffold and does not write the queue.
