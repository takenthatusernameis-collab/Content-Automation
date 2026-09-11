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
| 2026-09-11 Run 070 | ~104 estimate | 61 | verify_write_path.py runs shape then contract in one command |
| 2026-09-11 Run 071 | ~103 estimate | 62 | words.py prints draft.md band before apply |
| 2026-09-11 Run 072 | ~102 estimate | 63 | words.py prints add/cut Delta + Next; works without validate_packet sibling |
| 2026-09-11 Run 073 | ~101 estimate | 64 | words.py prints Hook Delta for the 20-35 hook band |
| 2026-09-11 Run 074 | ~100 estimate | 65 | words.py prints Beats + Thin so expand targets empty/thin headings |
| 2026-09-11 Run 075 | ~99 estimate | 66 | words.py prints Grow so expand picks one heading first |
| 2026-09-11 Run 076 | ~98 estimate | 67 | words.py prints Cut so an ABOVE trim picks one heading first |

Estimate basis (generic 8-min explainer):
- Run 076: -1 stop a future trim pass that cuts several headings instead of the longest surplus
- Run 075: -1 stop a future expand pass that grows several thin headings instead of the empty or shortest one
- Run 074: -1 stop a future expand pass that grows the wrong beat because only totals were visible
- Run 073: -1 stop a future expand pass that guesses how many hook words to add/cut
- Run 072: -1 stop a future expand pass that guesses how many words to add/cut
- Run 071: -1 stop a future apply-then-WARN loop by checking draft.md words first
- Run 070: -1 stop a reconstruct from running write_path_contract alone while contract_shape.py was never fetched
- Run 069: -1 stop a future run from treating a write_path_contract-only shape lock as enough when a sibling writer is gone
- Run 068: -1 stop a future run from treating a docstring-only lock file as PASS
- Run 067: -1 stop a future dry-run status write or silent no-op on in-band set_status; also stop claiming PASS on a docstring-only lock file
- Run 066: -1 stop a future dry-run-refresh or silent no-op on `--write --refresh`

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 076: `tools/words.py` prints Cut (one heading to trim first when ABOVE). --strict still keys off the total band. Still writes nothing.
- Run 075: `tools/words.py` prints Grow (one heading to expand first). Empty beats thin. --strict still keys off the total band. Still writes nothing.
- Run 074: `tools/words.py` prints Beats (per-heading spoken counts) and Thin (empty/thin headings). --strict still keys off the total band. Still writes nothing.
- Run 073: `tools/words.py` prints Hook Delta (add N / cut N vs 20-35). --strict still keys off the total band. Still writes nothing.
- Run 072: `tools/words.py` prints Delta (add N / cut N) and a Next line. Local counters if validate_packet.py is missing. Still writes nothing.
- Run 071: `tools/words.py` prints spoken WORDS vs the locked band from PATH/draft.md or script.md. Writes nothing. Not a lock. Not apply --write.
- Run 070: `tools/verify_write_path.py` subprocess-runs contract_shape then write_path_contract. Writes nothing. Not a substitute for those two files.
- Run 069: `tools/contract_shape.py` witnesses the write-path trio (write_path_contract, apply_script, set_status). Still does not import them and writes nothing.
- Run 068: `tools/contract_shape.py` is a second-file witness for write_path_contract.py.
- Run 067: `write_path_contract.py` is an executable lock again.
