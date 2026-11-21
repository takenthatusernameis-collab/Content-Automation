# PROGRESS

Updated: 2026-11-21T13:25:00Z (Run 1324)

## Latest measurable delta
- Enhanced suggested_search_queries in tools/research_verification_checklist.py to append primary-source site operators (site:gov OR site:edu OR site:org) for statistical/research-like claims. Research stage human minutes est. reduced to 4-9 (from 5-10). Operators surface automatically for matching excerpts.
- Videos published: 0. STALL_OAUTH_IDLE continues (~49 days). No provider write. Pre-upload path unchanged.
- Automated steps: many local gates + research/script helpers. Remaining recurring human: OAuth secrets + dispatch (one-time), then post-publish review.

## Run 1323 (prior)
Added non-blocking grounded search query suggestions to tools/research_verification_checklist.py (from extracted claim excerpts; human use only; no invented sources). Research stage human minutes est. reduced to 5-10 (from 6-12). Queries surface automatically when quantitative items exist.

## Run 1322 (prior)
Deepened non-blocking originality signals in tools/apply_script.py dry-run (concrete marker density + lived-experience flags). Script stage human minutes est. reduced to 10-25 (from 12-28). Signals surface automatically in every dry-run.

## Compounding notes
- Pre-upload path (idea -> master after materialize) is reliable. Primary blocker remains human OAuth setup.
- Prefer tools that reduce minutes in the labor map over pure inspection or status restatement.
- Recurring failure pattern: claiming code/docs updates without verifying actual file contents (placeholders or stubs). Always check wc/head/grep after writes.
- After first private video id: follow post_publish path (docs/q1_post_publish_prep.md, after_upload_steps.py).

See docs/labor_reduction_map.md for stage-by-stage minutes. Older history in docs/progress_archive.md.
