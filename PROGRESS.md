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
| 2026-09-11 Run 077 | ~97 estimate | 68 | words_contract.py fails placeholder/empty words.py and checks Grow/Cut |
| 2026-09-11 Run 078 | ~96 estimate | 69 | placeholder_guard.py fails emptied high-risk tools after a GitHub write |
| 2026-09-11 Run 079 | ~95 estimate | 70 | prove_locks.py runs guard then words_contract then verify in one command |
| 2026-09-11 Run 080 | ~94 estimate | 70 | NEXT_RUN_PROMPT names prove_locks first; no new tool |
| 2026-09-12 Run 081 | ~93 estimate | 71 | placeholder_guard witnesses prove_locks.py; isolated FAIL verified |
| 2026-09-12 Run 082 | ~92 estimate | 71 | hint.py prints idea_brief + words.py + draft.md apply lines |
| 2026-09-12 Run 083 | ~91 estimate | 71 | next_action fill-idea Why names idea_brief --block/--check |
| 2026-09-12 Run 084 | ~90 estimate | 71 | queue_status + next_topic print idea_brief after a folder exists |

Estimate basis (generic 8-min explainer):
- Run 084: -1 stop a future operator from treating queue_status/next_topic as "only mark_topic" after the folder exists
- Run 083: -1 stop a future operator from treating doctor/next_action Why as "remember the new_packet reprint"
- Run 082: -1 stop a future operator from scanning human_session after hint.py already printed the next packet code
- Run 081: -1 stop a future fallback from treating an emptied prove_locks.py as live while the inner three still pass
- Run 080: -1 stop a future run from skipping prove_locks because the operating addendum still listed the three inner commands first
- Run 079: -1 stop a future reconstruct from running one post-write lock while another was never fetched

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 084: `tools/queue_status.py` mark-needed follow-up and `tools/next_topic.py` after-folder lines name idea_brief --block / paste / --check. No new file. Still not a lock.
- Run 083: `tools/next_action.py` fill-idea Why names idea_brief --block / paste / --check. doctor.py and hint.py reprint that Why. No new file. Still not a lock.
- Run 082: `tools/hint.py` fill-idea prints idea_brief reprint/--block/--check. write-script/expand-script print words.py and apply from PATH/draft.md. Fixture still refuses apply --write. No new file. Still not a lock.
- Run 081: `tools/placeholder_guard.py` also witnesses prove_locks.py (800-byte floor + PROVE LOCKS PASS + inner three filenames). Isolated missing and 8-byte bodies FAIL. No new file. Still unmapped.
- Run 080: NEXT_RUN_PROMPT.md names `python3 tools/prove_locks.py` as the first post-write command. No new tool. The three inner commands remain fallback.
- Run 079: `tools/prove_locks.py` is an unmapped order wrapper for placeholder_guard, words_contract, and verify_write_path.
