## Run 926 — 2026-10-31T08:20:00Z
- Objective: Reduce future duration misestimation for generated narration by calibrating speaking_time_estimate against real Selected VO.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Materialized Q1 media locally (verified PRESENT + media_qa PASS). Updated tools/speaking_time_estimate.py to default to 190 wpm when vo_origin.md marks generated, and to report observed duration + WPM whenever the packet-relative Selected VO exists. Q1 observed 199 wpm on 308.4 s take (estimate now 323 s vs prior 438 s at 140 wpm). No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. Duration estimates for generated VO now closer to reality and self-calibrating when a take exists. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Local run of the updated tool printed observed 199 wpm and 5:23 estimate; media_qa remained PASS. Code change committed.
- Discovery: Generated TTS on Q1 runs ~199 wpm; the previous fixed 140 wpm overestimated length by ~40% and could mis-size end-screen reserve or timeline planning on future generated packets.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

## Run 925 — 2026-10-31T07:20:00Z
- Objective: Eliminate remaining silent zero-word / divergent section extractors in duration tools by centralizing them.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Added phrase_utils.extract_sections and count_spoken_words. Updated end_screen_reserve_check.py, minimum_timeline_estimate.py (fixed latent false 0-word by removing re-application of spoken_words to section text), and speaking_time_estimate.py to use the shared helpers. Extended phrase_utils_contract.py and verified PASS. No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. Duration estimators now share identical section boundaries and word-count path. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Local clone + python3 tools/phrase_utils_contract.py reported PHRASE_UTILS_CONTRACT PASS. Code changes committed. No packet writes.
- Discovery: minimum_timeline_estimate had the same class of bug previously fixed in end_screen_reserve_check; local extractors continued to drift even after one alignment.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)
