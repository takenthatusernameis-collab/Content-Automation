# RUNS

## Run 731 — 2026-10-22T17:30:00Z
- Objective: Lock the shared idea.md field extractor with a contract so future runs cannot reintroduce local parser drift.
- Action: Added tools/idea_utils_contract.py that exercises extract on full fields, missing fields, case-insensitive + trailing-period strip, extra prose, and empty input. Asserts expected tuples. Updated state files. Did not poll secrets, dispatch, scaffold, edit any live packets, materialize, or refresh the checklist banner.
- Result: Videos published stay 0. Shared extractor now has an explicit contract lock. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: Local execution of the contract prints IDEA_UTILS_CONTRACT PASS and exits 0. No packet changes.
- Discovery: After systematic migration of high-frequency tools, a small contract prevents regression of the single source of truth.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or python3 tools/human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Avoid more status/polish/suggest-contract tools.

# RUNS

## Run 730 — 2026-10-22T16:20:00Z
- Objective: Migrate remaining experiment starters, mechanism alignment scan, expand starter, and research brief/sources tools to the shared idea.md field extractor so more production paths use one consistent parser.
- Action: Refactored tools/experiment_baseline_starter.py, tools/experiment_notes_starter.py, tools/mechanism_align_scan.py, tools/expand_starter.py, tools/research_brief_starter.py, and tools/research_sources_starter.py to import extract from tools/idea_utils.py. Removed local MECH_RE/TOPIC_RE definitions and extract functions (kept viewer extraction local where needed). Dropped unused imports. Preserved previous behavior and fallbacks at call sites. Updated state files. Did not poll secrets, dispatch, scaffold, edit any live packets, materialize, or refresh the checklist banner.
- Result: Videos published stay 0. Six additional tools now use the single source of truth. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: py_compile succeeds on all six files. Import and extract calls return expected tuples. Fallbacks and extra fields (viewer) applied at call sites match prior behavior. Live packets unchanged. No local extract defs remain in the migrated files.
- Discovery: Experiment starters, research paths, and expand/align scans still carried duplicated parsers; shared module now covers more of the experiment and pre-production paths.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or python3 tools/human_next_action.py / operator_card.py, then secrets + single execute=true dispatch) or migrate any remaining lower-frequency local extracts if desired. Avoid more status/polish/suggest-contract tools.
