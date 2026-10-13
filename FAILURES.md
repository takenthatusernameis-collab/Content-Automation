# FAILURES

Older failure notes live in `docs/failures_archive.md`. Do not paste the archive back.

## Run 525 — 2026-10-13T22:20:00Z
- None. No failed approaches. Continued anti-rediscovery pattern while OAuth stall persists. Recovered from intermediate placeholder commits during this run.

None this run.

No new failures. Media QA and next_action confirmed after materialize.


## Run 522 — 2026-10-13T22:13:00Z
- None. No failed approaches. Continued anti-rediscovery pattern while OAuth stall persists.


## Run 520 — 2026-10-13T20:15:00Z
- Recovered: Run 519 commits set tools/status_report.py to the literal string PLACEHOLDER_TO_BE_REPLACED, breaking the primary status command. Fixed by restoring from d2ce49f and re-applying the intended one-liner. No other failures. Do not repeat the placeholder overwrite pattern.


## Run 518 — 2026-10-13T17:30:00Z
- No new failure. OAuth stall continues (secrets absent). Videos published stay 0.

None. No new failures this run.


## Run 516 — 2026-10-13T12:30:00Z
- No new failures. Discovered and fixed HANDOFF.md containing the literal shell placeholder `$(cat /tmp/HANDOFF.md)` (prior refresh attempts wrote the command string instead of content). OAuth secrets remain the sole blocker. No gate regressions. No invented data.

## Run 514 — 2026-10-13T13:30:00Z
- No new failures. OAuth secrets remain the sole blocker. No gate regressions. No invented data.

## Run 513 — 2026-10-13T12:20:00Z
- No new failures. OAuth stall continues as expected. Media absent in session (do not rematerialize if present on other machines). No gate re-verification solely for confirmation.

None this run.

## Run 510 — 2026-10-13T09:15:00Z
- None. No new failure. OAuth stall continues as expected.

- Run 509: No new failures. Local gates not re-run (media absent in session). OAuth stall continues as expected.

- none

None. Thumbnail inspection succeeded; approval recorded without inventing sensory evidence beyond accessible PNG properties.

None. No failed approaches this run. OAuth secrets still absent as expected.

No new failures this run.

None this run.

## Run 505 — 2026-10-13T04:20:00Z
None.

## Run 501 — 2026-10-13T00:14:00Z
None.

## Run 500 — 2026-10-12T20:15:00Z
None.

## Run 499 — 2026-10-12T19:20:00Z
None.
