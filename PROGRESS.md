# PROGRESS

Updated: 2026-11-21T17:21:00Z (Run 1326)

## Latest measurable delta
- Enhanced ranking in tools/research_verification_checklist.py with type summary counts and secondary-dominance WARNING. Research stage human minutes est. reduced to 3-7 (from 3-8). Heuristic only; no invented sources.
- Videos published: 0. STALL_OAUTH_IDLE continues (~49 days). No provider write. Pre-upload path unchanged.
- Automated steps: many local gates + research/script helpers. Remaining recurring human: OAuth secrets + dispatch (one-time), then post-publish review.

## Run 1325 (prior)
Added classify_source() + extract_source_candidates() to tools/research_verification_checklist.py. When sources.md exists, checklist now ranks candidates by type (primary preferred). Research stage human minutes est. reduced to 3-8 (from 4-9). Heuristic only; no invented sources.

## Compounding notes
- Pre-upload path (idea -> master after materialize) is reliable. Primary blocker remains human OAuth setup.
- Prefer tools that reduce minutes in the labor map over pure inspection or status restatement.
- Recurring failure pattern: claiming code/docs updates without verifying actual file contents (placeholders or stubs). Always check wc/head/grep after writes.
- After first private video id: follow post_publish path (docs/q1_post_publish_prep.md, after_upload_steps.py).

See docs/labor_reduction_map.md for stage-by-stage minutes. Older history in docs/progress_archive.md.
