# RUNS

## Run 662 — 2026-10-19T19:13:00Z
- Objective: Compound the research-to-claim path by extending table extraction in claim_scan.py to research.md (matching sources.md) and making the research_brief_starter skeleton self-documenting about the native table format.
- Action: Updated tools/claim_scan.py extract_sources_from_md and scan_path to process tables/bullets from both research.md and sources.md. Updated tools/research_brief_starter.py skeleton comment and RECOMMENDED NEXT. Updated STATE.md, NEXT.md, RUNS.md, and PROGRESS.md. Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner.
- Result: Videos published stay 0. Future packets that use either research starter now see and can use the exact table format that clears claim hits without extra ## Sources rewriting. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: Files updated via GitHub API. Change is small, self-contained, adds no new tools or dependencies. Existing sources.md extraction and research.md bullet behavior preserved and extended.
- Discovery: Applying the same extraction logic to both research files eliminates the remaining format difference between the two starters for every future research packet.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or python3 tools/human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer research_brief_starter, research_sources_starter, claim_scan, and other preferred unblocked tools. Avoid more status/polish tools.

## Run 661 — 2026-10-19T18:12:16Z
- Objective: Compound the research-to-claim path by making the research_sources_starter skeleton self-documenting so operators and future agents know the native Source-log table / bullet format is already recognized by claim_scan.py.
- Action: Updated tools/research_sources_starter.py skeleton comment and RECOMMENDED NEXT line. Updated STATE.md, NEXT.md, RUNS.md, and PROGRESS.md. Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner.
- Result: Videos published stay 0. Future packets that use the starter now see the exact format that clears claim hits without extra research.md rewriting. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: File updated via GitHub API. Change is small, self-contained, adds no new tools or dependencies. Existing extraction behavior (Runs 659-660) unchanged.
- Discovery: Explicit documentation inside the starter that produces the skeleton eliminates the remaining rediscovery of the table-to-citation linkage for every future research packet.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or python3 tools/human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer research_sources_starter, claim_scan, and other preferred unblocked tools. Avoid more status/polish tools.
