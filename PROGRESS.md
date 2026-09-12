# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-09-09 Run 027 | ~148 estimate | 25 | topic queue + read-only next_topic.py |
| 2026-09-11 Run 061 | ~113 estimate | 52 | apply_script missing --from exits 2 with draft.md hint |
| 2026-09-11 Run 079 | ~95 estimate | 70 | prove_locks.py runs guard then words_contract then verify in one command |
| 2026-09-11 Run 080 | ~94 estimate | 70 | NEXT_RUN_PROMPT names prove_locks first; no new tool |
| 2026-09-12 Run 081 | ~93 estimate | 71 | placeholder_guard witnesses prove_locks.py; isolated FAIL verified |
| 2026-09-12 Run 082 | ~92 estimate | 71 | hint.py prints idea_brief + words.py + draft.md apply lines |
| 2026-09-12 Run 083 | ~91 estimate | 71 | next_action fill-idea Why names idea_brief --block/--check |
| 2026-09-12 Run 084 | ~90 estimate | 71 | queue_status + next_topic print idea_brief after a folder exists |
| 2026-09-12 Run 085 | ~89 estimate | 71 | human_session start names idea_brief after a folder exists |
| 2026-09-12 Run 086 | ~88 estimate | 71 | agent_session WAVE 3 names idea_brief after a folder exists |

Estimate basis (generic 8-min explainer):
- Run 086: -1 stop a future clone-less agent from treating WAVE 3 as "only mark_topic" after the folder exists
- Run 085: -1 stop a future operator from treating human_session start as "only mark_topic" after the folder exists
- Run 084: -1 stop a future operator from treating queue_status/next_topic as "only mark_topic" after the folder exists

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 086: `docs/agent_session.md` WAVE 3 board paragraph and Stop list name idea_brief --block / paste / --check after a mark-needed folder exists. No new file. Still not a lock.
- Run 085: `docs/human_session.md` start-of-session text names idea_brief --block / paste / --check after a mark-needed folder exists and after next_topic prints an existing predicted path. No new file. Still not a lock.
- Run 084: `tools/queue_status.py` mark-needed follow-up and `tools/next_topic.py` after-folder lines name idea_brief --block / paste / --check. No new file. Still not a lock.
