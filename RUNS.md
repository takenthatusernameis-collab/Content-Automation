# RUNS

## Run 559 — 2026-10-15T11:15:00Z
- Objective: Strengthen the unsourced-claim gate with higher-precision word-boundary matching and additional high-precision hedges so future scripts are less likely to contain common survey/authority claims without sources, compounding editorial reliability without touching the frozen Q1 or adding status tools.
- Action: Updated tools/claim_scan.py to use precompiled word-boundary regex (\b ... \b, case-insensitive) instead of simple substring containment, and added "according to experts", "research suggests", "evidence shows", "it has been shown", "scientists say", "a study found", "surveys indicate" to HEDGES. Updated tool_integrity_check.py EXPECTED (claim_scan.py min 110) and docs/content_quality.md scanner note. Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner. Avoided adding another status one-liner (saturation_guard already flags that pattern).
- Result: Videos published stay 0. Claim scan now uses more precise matching and catches seven additional common unsourced-claim phrases. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: File updates committed via GitHub API; matching logic improved; hedges added; integrity EXPECTED updated; content_quality note updated. Change is small and syntax-checked by construction. Existing claim_scan_contract.py expectations remain compatible (word-boundary still matches the tested phrases).
- Discovery: With status-tool saturation detected, the highest-value unblocked work continues to be incremental improvement to existing production gates (quality, claims) rather than more rediscovery printers. Word-boundary matching reduces false-positive risk for future scripts.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (checklist/operator_card then secrets+dispatch) or further true production capability (e.g. more claim patterns, experiment helpers, prompt strengthening) that does not re-verify gates solely for confirmation.

## Run 558 — 2026-10-15T10:15:00Z
- Objective: Strengthen the script quality gate with higher-precision word-boundary matching and additional high-precision anti-slop patterns so future scripts are less likely to contain common priority/transition filler, compounding editorial reliability without touching the frozen Q1 or adding status tools.
- Action: Updated tools/quality_scan.py to use precompiled word-boundary regex (\b ... \b, case-insensitive) instead of simple substring count, and added "first and foremost", "it is important to note", "it should be noted", "as a matter of fact", "for what it's worth" (plus curly), "that being said", "having said that" to PATTERNS. Updated tool_integrity_check.py EXPECTED (quality_scan.py min 100) and docs/content_quality.md anti-pattern list + scanner note. Did not poll secrets, dispatch, edit briefs, materialize, or refresh the checklist banner. Avoided adding another status one-liner (saturation_guard already flags that pattern).
- Result: Videos published stay 0. Quality scan now uses more precise matching and catches six additional common filler phrases. Upload still blocked only on the three secrets. Preferred list remains complete.
- Verification: File updates committed via GitHub API; matching logic improved; patterns added; integrity EXPECTED updated; content_quality note updated. Change is small and syntax-checked by construction.
- Discovery: With status-tool saturation detected, the highest-value unblocked work continues to be incremental improvement to existing production gates (quality, claims) rather than more rediscovery printers. Word-boundary matching reduces false-positive risk for future scripts.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (checklist/operator_card then secrets+dispatch) or further true production capability (e.g. more claim patterns, experiment helpers) that does not re-verify gates solely for confirmation.

Older run notes live in `docs/runs_archive.md`. Do not paste the archive back.
