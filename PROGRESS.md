# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-09-09 Run 027 | ~148 estimate | 25 | topic queue + read-only next_topic.py |
| 2026-09-11 Run 061 | ~113 estimate | 52 | apply_script missing --from exits 2 with draft.md hint |
| 2026-09-11 Run 062 | ~112 estimate | 53 | write_path_contract locks missing --from CLI exit 2 |
| 2026-09-11 Run 063 | ~111 estimate | 54 | write_path_contract locks dry-run --from existing draft.md |
| 2026-09-11 Run 064 | ~110 estimate | 55 | write_path_contract locks set_status CLI blocked ready_for_vo |
| 2026-09-11 Run 065 | ~109 estimate | 56 | write_path_contract locks apply_script CLI --write fixture refuse |
| 2026-09-11 Run 066 | ~108 estimate | 57 | write_path_contract locks non-fixture --write / --refresh CLIs |
| 2026-09-11 Run 067 | ~107 estimate | 58 | write_path_contract body restored + in-band set_status success CLI lock |

Estimate basis (generic 8-min explainer):
- Run 067: -1 stop a future dry-run status write or silent no-op on in-band set_status; also stop claiming PASS on a docstring-only lock file
- Run 066: -1 stop a future dry-run-refresh or silent no-op on `--write --refresh`

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 067: `write_path_contract.py` is an executable lock again. Subprocess-runs in-band non-fixture set_status ready_for_vo dry-run and --write. Re-locks Runs 062–066 CLIs in the same file.
