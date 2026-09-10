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

Earlier rows 001-026 remain in prior commits.

Estimate basis (generic 8-min explainer):
- Run 042: -1 stop agents guessing how to reconstruct queue_status before running it

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 037: `tools/needed.py` prints the reconstruct file list. Unmapped. Local PASS.
- Run 038: `needed.py --missing` reports PRESENT/MISSING and READY/NOT READY with exit 0. FALLBACK_ALIAS resolves edited-tool names when which_contract is absent. Still unmapped. Local PASS on `/tmp/ca/tools`.
- Run 039: `needed.py --bootstrap` prints the ordered first-fetch set. `--bootstrap --missing` uses the same PRESENT/MISSING flags. Still unmapped. Local PASS on `/tmp/ca/tools`.
- Run 040: `needed.py --plan` prints WAVE 1 bootstrap paths and the WAVE 2 command (`selftest.py --missing`) without dumping selftest files. Still unmapped. Local PASS on `/tmp/ca/tools`.
- Run 041: `needed.py --plan` WAVE 3 prints `queue_status.py` as the first operator command after reconstruct. Does not dump queue files. Does not auto-scaffold. Still unmapped. Local PASS on `/tmp/ca/tools`.
- Run 042: `needed.py --plan` WAVE 3 prints `needed.py queue_status.py --missing` before the operator line. Still no queue file dump. Still unmapped. Local PASS on `/tmp/ca/tools`.
