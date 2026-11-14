## Run 1247 — 2026-11-14T04:15:00Z
Evidence: Exact archive-pointer string embedded in prior progress notes broke compact_all count==1 check (Runs 1245-1246). Added refuse-guard in tools/record_run.py. Contracts and selftest remain green.
Lesson: When status notes must describe a fix involving an exact-string check, never quote the protected string itself. Prefer a writer-side refuse over repeated post-hoc rewording. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 1220 — 2026-11-13T00:23:09Z
Evidence: Inspected after Run 1219. Pre-upload path remains reliable. oauth_credential_format_check.py includes whitespace detection. STALL_OAUTH_IDLE continues at 1000+ runs with published=0 and no human progress. Successive pure verification and state recording have low compounding effect at this extreme duration. Lesson: after extreme stall (1000+ runs), treat further pure inspection/recording as low-leverage; agents should flag HIGH suspicion explicitly and prefer the human OAuth step or any remaining unblocked production capability. Small hardening of existing human-path tools is acceptable if it reduces recurring failure modes. Do not add another consistency printer, aggregator, or contract lock while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

## Run 1219 — 2026-11-12T23:19:00Z
Evidence: Inspected after Run 1218. Pre-upload path remains reliable. Enhanced existing oauth_credential_format_check.py for whitespace detection (small friction reduction on human OAuth path). STALL_OAUTH_IDLE continues at 1000+ runs with published=0 and no human progress. Successive pure verification and state recording have low compounding effect at this extreme duration. Lesson: after extreme stall (1000+ runs), treat further pure inspection/recording as low-leverage; agents should flag HIGH suspicion explicitly and prefer the human OAuth step or any remaining unblocked production capability. Small hardening of existing human-path tools is acceptable if it reduces recurring failure modes. Do not add another consistency printer, aggregator, or contract lock while STALL_OAUTH_IDLE is primary. Do not modify ORIGINAL_MASTER_PROMPT.md.

# PROMPT EVOLUTION
