# PROGRESS

Updated: 2026-11-20T16:50:00Z (Run 1321)

## Latest measurable delta
- Tracking files (NEXT.md, PROGRESS.md, FAILURES.md, docs/labor_reduction_map.md) were stubbed ("UPDATED_*") despite prior claims of updates. Restored labor map from historical good version (Run 1316) and updated with Run 1318-1320 gains (sources cross-check, skeleton writer, apply_script reliability).
- Research stage human minutes est. reduced to 6-12 (from 8-15). Script stage dry-run reliability restored after multiple placeholder regressions.
- Videos published: 0. STALL_OAUTH_IDLE continues (~48 days). No provider write. Pre-upload path unchanged.
- Automated steps: many local gates + research/script helpers. Remaining recurring human: OAuth secrets + dispatch (one-time), then post-publish review.

## Run 1320 (prior)
Restored tools/apply_script.py from placeholder regression. Properly integrated non-blocking originality_notes + anti-slop. Verified dry-run. Documentation-without-code and placeholder patterns recurred; agents must verify file contents after edits.

## Run 1319
Added --write-skeleton to research_verification_checklist.py (non-destructive). Compounds research linking efficiency.

## Run 1318
Added sources.md cross-check to research checklist. Reduced research stage minutes estimate.

## Compounding notes
- Pre-upload path (idea -> master after materialize) is reliable. Primary blocker remains human OAuth setup.
- Prefer tools that reduce minutes in the labor map over pure inspection or status restatement.
- Recurring failure pattern: claiming code/docs updates without verifying actual file contents (placeholders or stubs). Always check wc/head/grep after writes.
- After first private video id: follow post_publish path (docs/q1_post_publish_prep.md, after_upload_steps.py).

See docs/labor_reduction_map.md for stage-by-stage minutes. Older history in docs/progress_archive.md.
