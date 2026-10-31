## Run 924 — 2026-10-31T06:20:00Z
- Objective: Reduce future divergence in spoken-word duration estimates by aligning end_screen_reserve_check with the shared phrase_utils helpers.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Updated tools/end_screen_reserve_check.py so the official total word count uses phrase_utils.spoken_words (and section counts use the shared normalize). This keeps CTA/total estimates consistent with quality_scan, claim_scan, and other scanners that already rely on the same extractor. No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. End-screen check now shares the canonical spoken-words path. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Code change committed; shared helpers already locked by phrase_utils_contract.py. No packet writes.
- Discovery: Custom extractors can silently drift from the shared spoken_words path even after a local bug fix; centralizing the total count closes that gap for future packets.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

## Run 923 — 2026-10-31T05:16:00Z
- Objective: Eliminate false zero-word / SHORT warnings from end_screen_reserve_check so duration estimates are reliable on standard script.md files.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Materialized Q1 r253. Confirmed media_qa / master_sha / pre_upload_qa_suite PASS except end_screen_reserve_check reporting 0 words. Root cause: count_words re-applied spoken_words (expects full WORDS: blocks) to already-extracted section text. Updated the function to count the provided spoken body directly and removed the unused import. Verified on Q1: 941 total words, CTA 20.0s, overall PASS; suite now fully PASS. No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. End-screen check now produces accurate estimates instead of false SHORT. Pre-upload path remains stable and cleaner. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Local materialize + fixed tool PASS + suite overall PASS confirmed. Syntax OK. No packet writes.
- Discovery: The check had been silently failing on every packet that used the standard WORDS:/VISUAL: format, generating noise that could trigger unnecessary revisions.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)
