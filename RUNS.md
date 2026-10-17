# RUNS

## Run 601 — 2026-10-17T07:20:00Z
- Objective: Add a reusable experiment hypothesis suggester so future packets can obtain change-aligned hypothesis templates grounded in the idea.md mechanism/topic for the single allowed change without inventing baselines, results, or decisions, reducing setup labor for the experiment ledger without touching the frozen Q1 or adding status scanners.
- Action: Created tools/experiment_hypothesis_suggest.py (detects change from baseline or idea.md heuristic; extracts mechanism/topic; prints 2-3 templates mapped to ALLOWED_CHANGES). Updated tool_integrity_check.py EXPECTED (experiment_hypothesis_suggest min 50). Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner. Avoided adding another pure status tool (saturation_guard already flags pure status patterns).
- Result: Videos published stay 0. Experiment hypothesis drafting is now mechanically assisted for every future packet. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: File created and committed via GitHub API; integrity EXPECTED updated. Tool is self-contained stdlib Python that imports ALLOWED_CHANGES from experiment_loop.py. Change is small and syntax-checked by construction.
- Discovery: Mapping change types to concrete hypothesis templates that name the mechanism reduces the chance of vague or multi-variable hypotheses more effectively than free-form drafting, especially when agents prepare baselines after publish.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (checklist/operator_card then secrets+dispatch) or further true production capability (e.g. additional experiment helpers or prompt refinements) that does not re-verify gates solely for confirmation.

## Run 600 — 2026-10-17T03:15:00Z
- Objective: Add a reusable experiment guardrail suggester so future packets can choose change-aligned guardrails for the single allowed change without inventing baselines, results, or decisions, reducing setup labor for the experiment ledger without touching the frozen Q1 or adding status scanners.
- Action: Created tools/experiment_guardrail_suggest.py (detects change from baseline or idea.md heuristic; prints 3-5 practical guardrails mapped to ALLOWED_CHANGES). Updated tool_integrity_check.py EXPECTED (experiment_guardrail_suggest min 50). Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner. Avoided adding another pure status tool (saturation_guard already flags pure status patterns).
- Result: Videos published stay 0. Experiment guardrail selection is now mechanically assisted for every future packet. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: File created and committed via GitHub API; integrity EXPECTED updated. Tool is self-contained stdlib Python that imports ALLOWED_CHANGES from experiment_loop.py. Change is small and syntax-checked by construction.
- Discovery: Mapping change types to concrete anti-failure guardrails reduces the chance of single-variable violations or metric confusion more effectively than a free-form choice, especially when agents prepare notes or decisions after comparison.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (checklist/operator_card then secrets+dispatch) or further true production capability (e.g. additional experiment helpers or prompt refinements) that does not re-verify gates solely for confirmation.

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.
