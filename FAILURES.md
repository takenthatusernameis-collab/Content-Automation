# FAILURES

None. Materialize, media_qa, SHA match, and contracts all succeeded as expected. STALL_OAUTH_IDLE continues as sole blocker.

None. Materialize, media_qa, SHA match, and contracts all succeeded as expected.

Run 1257: No new failures. Prior size-cap overflow (Run 1255/1256) addressed by size-aware compaction to prevent recurrence.

None. Size-cap regression fixed. No new failure modes.

None. No regressions. Suites remain green.

None. Phased plan addition only; no new failure modes. STALL_OAUTH_IDLE continues as sole blocker (1000+ runs, HIGH suspicion).

No new failures. Exact-string compact checks remain sensitive to status notes; refuse-guard in record_run.py continues to protect them.

None. The long OAuth stall continues as the sole external blocker.

No new failures. STALL_OAUTH_IDLE continues as sole blocker (1000+ runs, HIGH suspicion).

None this run. Stall detection predicates expanded for robustness; no new failure modes introduced.

None this run. Refuse-guard remains active to prevent known archive-pointer quote failure mode.

None this run. Guard added to prevent known exact-string failure mode.

None. Guidance update only; no failures.

None this run. Materialize and media_qa succeeded. No repeated failure patterns observed.

none this run

none this run

2026-11-10T06:20:00Z (Run 1154)

None. Quality brief enhancement completed and verified locally on Q1 packet (clear script scans; metadata scans ran).


(Older failures remain in docs/failures_archive.md.)

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.
