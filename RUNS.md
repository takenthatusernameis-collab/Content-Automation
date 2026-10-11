# RUNS

## Run 468 — 2026-10-11T08:20:00Z
- Objective: Restore green selftest by reducing NEXT.md size below the 12000-byte cap after long notes accumulated in the preamble.
- Action: Materialized Q1 (checksums matched). Verified media_qa PASS, closed_brief_gate PASS, next_action upload-blocked, operator_card PASS. Ran runs_compact and next_compact, then manually moved 16 older Run notes from NEXT.md preamble into docs/next_archive.md. Resulting NEXT.md is 4499 bytes. Updated status_report.py preferred list and docs/human_oauth_checklist.md banner. Used record_run.py. Did not poll secrets, dispatch, edit briefs, or commit media.
- Result: Videos published stay 0. Selftest now PASS. Upload still blocked only on the three secrets.
- Verification: materialize ignored truncated r249. media_qa PASS. closed_brief_gate PASS. next_action upload-blocked. operator_card PASS. next_compact_contract PASS. compact_all OK. selftest SELFTEST PASS.
- Discovery: The next_compact tool only archives numeric-timestamp items; long 'Run N:' notes stay in the preamble and can push size over the contract limit even when item count is under max. Manual archive of older notes restores the cap.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prefers remaining unblocked improvements from status_report, does not invent data.

## Run 467 — 2026-10-11T07:15:00Z
- Objective: Reduce agent rediscovery of preferred unblocked work while the long OAuth stall continues by making while-stalled guidance explicit in the primary handoff document.
- Action: Updated HANDOFF.md timestamp and added an explicit 'While the OAuth stall continues' section pointing to status_report preferred improvements and production_rules agent-behavior section. Marked the item done in tools/status_report.py preferred list. Refreshed docs/human_oauth_checklist.md banner and note to Run 467. Did not poll secrets, dispatch, edit briefs, or commit media.
- Result: Videos published stay 0. Future agents see clear guidance against pure verification and toward the listed preparations in the main entry-point document. Upload still blocked only on the three secrets.
- Verification: Files updated and committed. No new tool surface. Local gates not re-run (media absent). Typo in status_report.py __name__ fixed before final push.
- Discovery: HANDOFF.md was still dated to Run 456; refreshing it with stall-specific guidance closes one preferred anti-rediscovery item without inventing data or expanding locked surfaces.
- Blocker: YouTube OAuth secrets still absent. Playlist id still not_set.
- Next: Human follows docs/human_oauth_checklist.md or operator_card.py / issue #1. Next agent materializes only if media missing, uses record_run.py, prefers remaining unblocked improvements from status_report, does not invent data.

Permanent log. Newest first. Do not paste the archive back into this file.

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.
