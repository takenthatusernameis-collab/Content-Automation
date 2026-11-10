2026-11-10T05:20:00Z (Run 1153)

Enhanced tools/experiment_readiness.py to also report experiment_decision.json status (absent/template/recorded/incomplete) after a filled baseline. Expanded recommended_actions in experiment_decision_starter.py to include notes, package, and readiness commands for consistency with other starters. Advances post-publish readiness and reduces human rediscovery of next steps for every future video without credentials or invented results. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion). Pre-upload remains complete. No secrets polled, no dispatch, no live packet writes. Next remains the human OAuth step.

# RUNS

## Run 1153 — 2026-11-10T05:20:00Z
- Objective: Improve post-publish experiment readiness reporting and consistency of recommended next steps so future videos require less human rediscovery after the first private id.
- Action: Updated tools/experiment_readiness.py to check decision file status in addition to baseline. Updated tools/experiment_decision_starter.py recommended_actions to parallel other starters (notes, package, readiness). Pushed the changes. Recorded in state files. No secrets polled, no dispatch, no live packet writes.
- Result: The readiness tool now gives a complete picture of baseline + decision status and exact next commands. Decision starter suggests the full set of related tools. Compounds reliability for the improvement loop. STALL_OAUTH_IDLE continues.
- Verification: Source inspection confirms the new decision status logic and expanded recommendations. Soft only (no live packet or secrets).
- Discovery: Completing the decision-side reporting pairs with the existing starters and reduces the chance a future agent or human misses the decision step. Long stall remains HIGH suspicion after 1000+ runs.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/contracts_suite.py && python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1152 — 2026-11-10T04:20:00Z
- Objective: Advance post-publish readiness by adding a reusable, fail-closed starter for experiment_decision.json that cannot invent a decision.
- Action: Created tools/experiment_decision_starter.py and its contract. Updated docs/experiments.md to document it. Pushed the tools. Recorded in state files. No secrets polled, no dispatch, no live packet writes.
- Result: Future videos have a consistent way to scaffold the decision file that stays a template until a documented review after comparison. Reduces human error on the experiment path. STALL_OAUTH_IDLE continues.
- Verification: Source inspection confirms TEMPLATE guard and no recorded decision values in the skeleton. Contract locks the property. Soft only.
- Discovery: Completing the decision-side starter pairs with the baseline starter and compounds reliability for the improvement loop that runs after the first private video id. Long stall remains HIGH suspicion after 1000+ runs.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/contracts_suite.py && python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1151 — 2026-11-10T01:26:00Z
- Objective: Eliminate remaining local duplicates of the 7+3 observation window constants so the formula stays consistent in the core feedback adapter after the first private video id.
- Action: Added CALENDAR_DAYS=7 and DATA_LAG_DAYS=3 to tools/upload_date.py; OBSERVATION_WINDOW_DAYS now derived. Updated youtube_feedback.py to import and use them, removing local definitions. Verified contracts_suite.py. Recorded in state files. No secrets polled, no dispatch, no live packet writes.
- Result: Single source of truth now covers both the due-date arithmetic and the query length / lag components. Suite stays 90/90 PASS. Reduces future rediscovery or silent divergence on the post-upload path. STALL_OAUTH_IDLE continues.
- Verification: Local execution of contracts_suite.py exits 0 (90/90). Inspection confirms imports and derived constant. Soft only.
- Discovery: Completing the shared module for the full formula compounds reliability for the feedback path that will run after the first private video id. Long stall remains HIGH suspicion after 1000+ runs. Prefer the human step or a true post-publish capability over further pure confirmation.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, then secrets + single execute=true). After id appears: python3 tools/contracts_suite.py && python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)

Permanent log. Newest first.
