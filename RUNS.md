# RUNS

## Run 732 — 2026-10-22T18:15:00Z
- Objective: Lock the shared idea.md extractor into CI so future pushes catch parser drift automatically.
- Action: Added a step to .github/workflows/selftest.yml that runs python3 tools/idea_utils_contract.py. Verified the contract passes locally. Updated state files. Did not poll secrets, dispatch, scaffold, edit any live packets, materialize, or refresh the checklist banner.
- Result: Videos published stay 0. Shared extractor is now enforced on every selftest CI run. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: Local execution of tools/idea_utils_contract.py prints IDEA_UTILS_CONTRACT PASS and exits 0. Workflow file updated and committed.
- Discovery: The contract added in Run 731 was not yet in the CI path; wiring it prevents silent regression.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or python3 tools/human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Avoid more status/polish/suggest-contract tools.

## Run 731 — 2026-10-22T17:30:00Z
- Objective: Lock the shared idea.md field extractor with a contract so future runs cannot reintroduce local parser drift.
- Action: Added tools/idea_utils_contract.py that exercises extract on full fields, missing fields, case-insensitive + trailing-period strip, extra prose, and empty input. Asserts expected tuples. Updated state files. Did not poll secrets, dispatch, scaffold, edit any live packets, materialize, or refresh the checklist banner.
- Result: Videos published stay 0. Shared extractor now has an explicit contract lock. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: Local execution of the contract prints IDEA_UTILS_CONTRACT PASS and exits 0. No packet changes.
- Discovery: After systematic migration of high-frequency tools, a small contract prevents regression of the single source of truth.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or python3 tools/human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Avoid more status/polish/suggest-contract tools.
