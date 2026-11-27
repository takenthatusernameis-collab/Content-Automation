# PROGRESS

Updated: 2026-11-27T00:20:00Z (Run 1353)

## Latest measurable delta
- Added tools/caption_spotcheck_assistant.py that prints a structured captions review list with timings and soft flags. Reduces estimated human captions spot-check minutes (labor map). Verified by re-fetch. No invented content.
- Videos published: 0. STALL_OAUTH_IDLE continues (~51 days). No provider write. Pre-upload path unchanged.
- Automated steps: many local gates + research/script/caption/metadata helpers + priority aggregator (with next step) + labor estimate with next step + tracking integrity check (CI-enforced) + run-number consistency check (CI-enforced) + status one-pager + human guidance integrity check (CI-enforced) + post-publish integrity check (CI-enforced) + production path integrity check (CI-enforced) + caption spot-check assistant. Remaining recurring human: OAuth secrets + dispatch (one-time), then post-publish review.

## Compounding notes
- Pre-upload path (idea -> master after materialize) is reliable. Primary blocker remains human OAuth setup.
- Prefer tools that reduce minutes in the labor map or improve reliability over pure inspection or status restatement.
- Recurring failure pattern: claiming code/docs updates without verifying actual file contents (placeholders or stubs). Always check wc/head/grep after writes. This run verified by re-fetch after push. Caption spot-check assistance available.
- After first private video id: follow post_publish path (docs/q1_post_publish_prep.md, after_upload_steps.py).
- Tracking integrity, run-number consistency, human guidance integrity, post-publish integrity, and production path integrity are enforced on every selftest run.

See docs/labor_reduction_map.md for stage-by-stage minutes. Older history in docs/progress_archive.md.
