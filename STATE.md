# STATE

2026-11-09T03:21:00Z (Run 1128)

Added tools/claim_source_table_contract.py locking fail-closed no-invent behavior of the claim-to-source table generator (unique_preserve, hedges extraction, CLI table with blank source column, no URLs/citations invented, clean no-claims path). Pure and temp-dir tests only. No secrets polled, no dispatch, no live packet writes. Improves long-term reliability of the research claim extraction step used before every script is finalized so future changes cannot silently invent sources. Pre-upload remains complete. Long stall (1000+ runs) remains HIGH suspicion. Contract locks remain higher leverage than additional starter tools while stalled.

2026-11-09T02:30:00Z (Run 1127)

Strengthened tools/experiment_loop_contract.py with additional pure-function tests for load_baseline (rejects missing fields, invalid change, invented source) and compare_primary (computes delta without inventing keep/discard). Keeps the original HOLD_UNPUBLISHED CLI path. No secrets polled, no dispatch, no live packet writes. Improves long-term reliability of the post-publish experiment ledger so future changes cannot silently weaken fail-closed behavior used after every published video. Pre-upload remains complete. Long stall (1000+ runs) remains HIGH suspicion. Contract locks remain higher leverage than additional starter tools while stalled.

2026-11-09T01:20:00Z (Run 1126)

Refactored tools/queued_field_check.py to expose pure check_rows() function. Added tools/queued_field_check_contract.py that locks HARD/SOFT classification with in-memory test cases (missing id, invalid status, empty title, duplicates, short one_line, empty problem). No writes to live queue. Improves reliability of the integrity checker so future changes cannot silently weaken the queue gate that all pre-scaffold tools depend on. Pre-upload remains complete. No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/oauth_complete_guide.py). Long stall (1000+ runs) remains HIGH suspicion. Successive starter tools have diminishing returns; contract locks are higher leverage for long-term reliability.

2026-11-09T00:20:00Z (Run 1125)

Added tools/queued_field_check.py: read-only integrity checker for docs/topic_queue.md. Validates required fields (id/status/title/one_line), valid status values, non-empty problem for queued, reasonable lengths, unique ids/titles, and slug collision risk. Prints HARD/SOFT issues; exit 1 only on hard. No writes, no invent, no packet. Complements existing queue_status.py and the starter family by catching bad queue data early so it does not propagate into every future packet. Reduces future labor and improves reliability of the queue that all pre-scaffold tools depend on. Pre-upload remains complete. No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/oauth_complete_guide.py). Long stall (1000+ runs) remains HIGH suspicion. Pattern of successive queue-starter tools has diminishing returns; prefer integrity, clarity, or non-starter advances.

(Older state notes remain below or in docs/state_archive.md. Do not paste the archive back.)
