# RUNS

## Run 667 — 2026-10-20T03:15:00Z
- Objective: Compound the research-to-claim path by embedding the native Source table / bullet auto-extraction fact into the primary script-writing prompt so every future draft knows citations are recognized without rewriting a ## Sources section.
- Action: Updated prompts/script_writer.md Constraints bullet and anti-slop section to explicitly document auto-extraction of filled Source column values and non-placeholder bullets from research.md or sources.md by claim_scan.py. Updated STATE.md, NEXT.md, RUNS.md, and PROGRESS.md. Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner.
- Result: Videos published stay 0. Future drafts that follow the script writer prompt now see the exact recognition path for research files without rediscovery. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: File updated via GitHub API. Change is small, self-contained, adds no new tools or dependencies. Existing documentation in starters preserved and extended into the core writing prompt.
- Discovery: Documenting the extraction inside the main script_writer.md eliminates rediscovery for agents who start from the writing prompt rather than a research or production starter.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or python3 tools/human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer full_production_starter, pre_production_package_starter, research_package_starter, claim_scan, and other preferred unblocked tools. Avoid more status/polish tools.

## Run 666 — 2026-10-20T02:15:00Z
- Objective: Reduce rediscovery for future agents and operators by updating the outdated HANDOFF.md entry point to the current system state after ~70 runs of incremental polish.
- Action: Updated HANDOFF.md with accurate current preferred unblocked list, STALL_OAUTH_IDLE primary blocker, completed claim-source auto-extraction documentation (Runs 659-665), frozen banner note, and explicit human next step. Updated STATE.md. Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner.
- Result: Videos published stay 0. Future runs starting from HANDOFF now see the current preferred tools and the research-to-claim recognition path without reconstructing recent history. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: File updated via GitHub API. Change is self-contained, adds no new tools or dependencies. Existing guidance preserved and refreshed.
- Discovery: HANDOFF had drifted (last major update ~Run 595); refreshing the entry point compounds clarity across subsequent runs.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or python3 tools/human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer full_production_starter, pre_production_package_starter, research_package_starter, claim_scan, and other preferred unblocked tools. Avoid more status/polish tools.
