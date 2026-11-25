# PROGRESS

Updated: 2026-11-25T21:20:00Z (Run 1347)

## Latest measurable delta
- Added tracking_integrity_check.py step to .github/workflows/selftest.yml so every push and PR automatically verifies durable memory files against stub/placeholder risk. Builds on Run 1346 tool. Verified by workflow re-fetch. No invented content.
- Videos published: 0. STALL_OAUTH_IDLE continues (~51 days). No provider write. Pre-upload path unchanged.
- Automated steps: many local gates + research/script/caption/metadata helpers + priority aggregator (with next step) + labor estimate with next step + tracking integrity check (now CI-enforced). Remaining recurring human: OAuth secrets + dispatch (one-time), then post-publish review.

## Compounding notes
- Pre-upload path (idea -> master after materialize) is reliable. Primary blocker remains human OAuth setup.
- Prefer tools that reduce minutes in the labor map or improve reliability over pure inspection or status restatement.
- Recurring failure pattern: claiming code/docs updates without verifying actual file contents (placeholders or stubs). Always check wc/head/grep after writes. This run verified by re-fetch of workflow content. Integrity check now runs automatically in CI.
- After first private video id: follow post_publish path (docs/q1_post_publish_prep.md, after_upload_steps.py).
- Tracking integrity is enforced on every selftest run.

See docs/labor_reduction_map.md for stage-by-stage minutes. Older history in docs/progress_archive.md.
