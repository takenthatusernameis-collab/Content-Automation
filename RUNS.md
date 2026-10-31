## Run 925 — 2026-10-31T07:20:00Z
- Objective: Eliminate remaining silent zero-word / divergent section extractors in duration tools by centralizing them.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Added phrase_utils.extract_sections and count_spoken_words. Updated end_screen_reserve_check.py, minimum_timeline_estimate.py (fixed latent false 0-word by removing re-application of spoken_words to section text), and speaking_time_estimate.py to use the shared helpers. Extended phrase_utils_contract.py and verified PASS. No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. Duration estimators now share identical section boundaries and word-count path. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Local clone + python3 tools/phrase_utils_contract.py reported PHRASE_UTILS_CONTRACT PASS. Code changes committed. No packet writes.
- Discovery: minimum_timeline_estimate had the same class of bug previously fixed in end_screen_reserve_check; local extractors continued to drift even after one alignment.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

## Run 924 — 2026-10-31T06:20:00Z
- Objective: Reduce future divergence in spoken-word duration estimates by aligning end_screen_reserve_check with the shared phrase_utils helpers.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Updated tools/end_screen_reserve_check.py so the official total word count uses phrase_utils.spoken_words (and section counts use the shared normalize). This keeps CTA/total estimates consistent with quality_scan, claim_scan, and other scanners that already rely on the same extractor. No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. End-screen check now shares the canonical spoken-words path. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Code change committed; shared helpers already locked by phrase_utils_contract.py. No packet writes.
- Discovery: Custom extractors can silently drift from the shared spoken_words path even after a local bug fix; centralizing the total count closes that gap for future packets.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)
