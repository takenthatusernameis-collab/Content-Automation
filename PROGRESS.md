# PROGRESS

Updated: 2026-10-05T17:25:00Z

Older progress notes live in `docs/progress_archive.md`. Do not paste the archive back.

## Run 343 — 2026-10-05T17:25:00Z
PROGRESS.md and FAILURES.md no longer sit past the known fetch cut. Newest 12 sections stay live. Older notes are in docs/progress_archive.md and docs/failures_archive.md. Estimated agent minutes saved on the next runs: about 10, by not reconstructing a cut lesson. Human minutes per video unchanged. Videos published stay 0.

## Run 342 — 2026-10-05T17:15:00Z
RUNS.md no longer truncates before the newest run log. Newest 12 entries stay in the live file. Older entries are in docs/runs_archive.md. Estimated agent minutes saved on the next runs: about 10, by not reconstructing the latest action from a cut fetch. Human minutes per video unchanged. Videos published stay 0.

## Run 341 (2026-10-05T16:20:00Z)
- NEXT.md dropped from 28596 bytes to 12 notes. Older notes are in docs/next_archive.md. Estimated agent minutes saved on the next truncated-fetch rediscovery: about 10, if the newest locks are read first. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 340 (2026-10-05T15:20:00Z)
- STATE.md dropped from 52418 bytes and 67 run sections to 12 sections. Older deltas are in docs/state_archive.md. Estimated agent minutes saved on the next truncated-fetch rediscovery: about 10, if the newest gate is read first. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 339 — 2026-10-05T14:20:00Z
The production stall printer no longer treats `No new scanner` as a local-gate run. Estimated agent minutes saved on the next runs: about 10, by not following a false `STALL_LOCAL_GATE` that Runs 336-338 kept rewriting. Human minutes per video unchanged. Videos published stay 0.

## Run 338 — 2026-10-05T12:30:00Z
Persist no longer commits a COLLECTED analytics file that lacks the first-calendar-days stamp. Estimated effect: one less way a sliding or unstamped window becomes the comparison evidence after a later collect. Videos published stay 0. Human minutes on Q1 unchanged.

# PROGRESS

Updated: 2026-10-05T11:20:00Z

- Run 337: a collected analytics file no longer counts unless its window is the video's first 7 calendar days. Estimated agent minutes saved on the first comparison: about 15, by not treating a sliding or unstamped file as the observation. Human minutes per video unchanged. Videos published stay 0.

## Run 336 — 2026-10-05T10:20:00Z
- Dry-run feedback plan now matches the first-7-calendar-day query. Removes a future wrong collect after secrets exist. Human minutes per video unchanged. Videos published stay 0.
- Run 334: a failed playlist insert now fails the production step and leaves a plan file, instead of exiting 0 with no record. Estimated human minutes saved after the first real upload: about 10, because Studio is not the only way to learn the video missed the series playlist. `not_set` still does not fail the upload. Videos published stay 0.

- Run 333: dry-run `scope` now matches the consent set, so copying that field no longer mints an upload-only token. The production job prints the existing idle flag before preflight. Estimated human minutes saved on the first token mint: about 20, if the operator copies `scope`. Videos published stay 0. No new refusal.

- Run 332: OAuth-idle is visible across eight subject changes, not only three matching topics. A mistyped playlist id now fails the production step (exit 2) without blocking `not_set`. Estimated agent minutes saved on the next rediscovery pass: about 15. Human minutes on Q1 unchanged. Videos published stay 0.

# PROGRESS

- Run 330: dry-run consent scope now includes force-ssl and analytics, not upload alone. Estimated human minutes saved on the first token mint: about 20, if the operator follows the dry-run line instead of the old scope field. Videos published stay 0. No new refusal.


## Run 329 (2026-10-05T06:15:00Z)
- Local-gate inflation is now a visible stall flag instead of a silent series of new scanners. Estimated agent minutes saved on the next runs: the rediscovery pass over Runs 326-328, about 10, if the flag is read first. No change to human minutes on Q1. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 328 (2026-10-05T05:13:00Z)
- Upload inspect now fails closed on the same quality, claim, and title hits that already block `ready_for_vo`.
- Estimated effect: one less class of bad packet that can reach videos.insert after a later script or title edit. No change to human minutes on Q1. Videos published stay 0.

## Run 327 — 2026-10-05T01:17:00Z
Shouted titles and an explicit thumbnail mismatch now refuse ready_for_vo. Estimated human minutes saved on each later title review: about 3, if the report is clear. Q1 was already clear, so this video does not change. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 326 — 2026-10-05T00:20:00Z
Unsourced spoken digits and survey hedges now refuse ready_for_vo. Estimated human minutes saved on each later script: about 5, because the status step catches the number instead of a remembered research read. Q1 was already clear, so this video does not change. Videos published stay 0. Publish still waits on the three YouTube secrets.

## Run 324 — 2026-10-04T22:13:00Z
The production workflow packet is now a dispatch input defaulting to Q1. A later video can reuse the same job instead of a copied workflow. Q1 materialize stays path-locked. Estimated human minutes to add video 2's upload job later: about 20 avoided. Videos published stay 0. Publish still waits on the three YouTube secrets.

