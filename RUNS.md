## Run 923 — 2026-10-31T05:16:00Z
- Objective: Eliminate false zero-word / SHORT warnings from end_screen_reserve_check so duration estimates are reliable on standard script.md files.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Materialized Q1 r253. Confirmed media_qa / master_sha / pre_upload_qa_suite PASS except end_screen_reserve_check reporting 0 words. Root cause: count_words re-applied spoken_words (expects full WORDS: blocks) to already-extracted section text. Updated the function to count the provided spoken body directly and removed the unused import. Verified on Q1: 941 total words, CTA 20.0s, overall PASS; suite now fully PASS. No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. End-screen check now produces accurate estimates instead of false SHORT. Pre-upload path remains stable and cleaner. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Local materialize + fixed tool PASS + suite overall PASS confirmed. Syntax OK. No packet writes.
- Discovery: The check had been silently failing on every packet that used the standard WORDS:/VISUAL: format, generating noise that could trigger unnecessary revisions.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

## Run 922 — 2026-10-31T04:15:21Z
- Objective: Fix the NEXT.md size-lock failure that was causing SELFTEST FAIL and risking truncated fetches of the newest notes.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Updated tools/next_compact.py ITEM_RE to match lines starting with "Run " as well as digits, lowered MAX_ITEMS to 6, and adjusted next_compact_contract.py expected move counts. Ran compact (moved older notes to docs/next_archive.md). Verified NEXT COMPACT CONTRACT PASS and SELFTEST PASS. No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. NEXT.md is now under the 12kB cap with the newest locks visible. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Compact succeeded, contracts PASS, selftest PASS. No packet writes.
- Discovery: Recent Run notes started with "Run N:" which the previous item regex ignored, so the size lock never triggered archiving and the file grew past the truncated-fetch threshold.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)
