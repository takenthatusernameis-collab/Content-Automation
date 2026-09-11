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
| 2026-09-11 Run 068 | ~106 estimate | 59 | contract_shape.py fails if write_path_contract.py is emptied |
| 2026-09-11 Run 069 | ~105 estimate | 60 | contract_shape.py fails if apply_script.py or set_status.py is emptied |

Estimate basis (generic 8-min explainer):
- Run 069: -1 stop a future run from treating a write_path_contract-only shape lock as enough when a sibling writer is gone
- Run 068: -1 stop a future run from treating a docstring-only lock file as PASS
- Run 067: -1 stop a future dry-run status write or silent no-op on in-band set_status; also stop claiming PASS on a docstring-only lock file
- Run 066: -1 stop a future dry-run-refresh or silent no-op on `--write --refresh`

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 069: `tools/contract_shape.py` witnesses the write-path trio (write_path_contract, apply_script, set_status). Still does not import them and writes nothing.
- Run 068: `tools/contract_shape.py` is a second-file witness for write_path_contract.py.
- Run 067: `write_path_contract.py` is an executable lock again.
