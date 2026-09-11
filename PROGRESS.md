# PROGRESS

## Efficiency ledger

| When                 | Human min / video | Automated steps | Notes |
|----------------------|-------------------|-----------------|-------|
| 2026-09-09 Run 027   | ~148 estimate     | 25              | topic queue + read-only next_topic.py |
| 2026-09-11 Run 061   | ~113 estimate     | 52              | apply_script missing --from exits 2 with draft.md hint |
| 2026-09-11 Run 062   | ~112 estimate     | 53              | write_path_contract locks missing --from CLI exit 2 |
| 2026-09-11 Run 063   | ~111 estimate     | 54              | write_path_contract locks dry-run --from existing draft.md |
| 2026-09-11 Run 064   | ~110 estimate     | 55              | write_path_contract locks set_status CLI blocked ready_for_vo |
| 2026-09-11 Run 065   | ~109 estimate     | 56              | write_path_contract locks apply_script CLI --write fixture refuse |

Estimate basis (generic 8-min explainer):
- Run 065: -1 stop a future write-before-check regression from replacing sample-001 script.md when `--write` is passed
- Run 064: -1 stop a future write-before-check regression from promoting packet.md while WORDS are short or the packet is the fixture
- Run 063: -1 stop a future default-write regression from turning the printed apply dry-run into a silent script.md write

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 065: `write_path_contract.py` subprocess-runs `apply_script.py --from FIXTURE/draft.md --write`. Expects exit 1, BLOCKED, script.md unchanged. WRITE PATH CONTRACT PASS on reconstructed tree.
- Run 064: `write_path_contract.py` subprocess-runs `set_status.py --to ready_for_vo` dry-run, blocked `--write`, and fixture `--write`. Expects exit 1, BLOCKED, packet.md unchanged.
- Run 063: `write_path_contract.py` subprocess-runs `apply_script.py --from PATH/draft.md` when that file exists. Expects exit 0, Dry-run only, no script.md write.
- Run 062: `write_path_contract.py` subprocess-runs `apply_script.py --from` on a missing file. Expects exit 2, draft.md hint, no script.md write.
