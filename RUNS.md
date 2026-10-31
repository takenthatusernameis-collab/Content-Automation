## Run 927 — 2026-10-31T09:17:00Z
- Objective: Eliminate remaining rate divergence across duration planning tools so generated-narration packets receive consistent estimates.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Updated tools/end_screen_reserve_check.py and tools/minimum_timeline_estimate.py to select 190 wpm when vo_origin.md marks generated and 140 wpm otherwise, matching the logic already present in speaking_time_estimate.py. No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. End-screen reserve and minimum-timeline estimates now share the same calibrated rate path as speaking-time estimates. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Code changes committed; rate selection is identical across the three duration tools. No packet writes.
- Discovery: Fixed 150 wpm in the two planning tools continued to diverge from the calibrated 190/140 path, risking inconsistent end-screen and hold planning on future generated packets.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

## Run 926 — 2026-10-31T08:20:00Z
- Objective: Reduce future duration misestimation for generated narration by calibrating speaking_time_estimate against real Selected VO.
- Action: Inspected STATE/NEXT (STALL_OAUTH_IDLE, published=0). Materialized Q1 media locally (verified PRESENT + media_qa PASS). Updated tools/speaking_time_estimate.py to default to 190 wpm when vo_origin.md marks generated, and to report observed duration + WPM whenever the packet-relative Selected VO exists. Q1 observed 199 wpm on 308.4 s take (estimate now 323 s vs prior 438 s at 140 wpm). No secrets polled, no dispatch, no packet content edits, no media committed.
- Result: Videos published stay 0. Duration estimates for generated VO now closer to reality and self-calibrating when a take exists. Pre-upload path remains stable. Upload still blocked only on the three secrets. Text output stays local.
- Verification: Local run of the updated tool printed observed 199 wpm and 5:23 estimate; media_qa remained PASS. Code change committed.
- Discovery: Generated TTS on Q1 runs ~199 wpm; the previous fixed 140 wpm overestimated length by ~40% and could mis-size end-screen reserve or timeline planning on future generated packets.
- Blocker: STALL_OAUTH_IDLE (secrets absent). Do not poll.
- Recommended next: human step (docs/human_oauth_checklist.md or tools/oauth_exchange.py / human_next_action.py / operator_card.py, then secrets + single execute=true dispatch). Prefer another truly new production capability if it does not require credentials. Avoid more sequence printers, briefs, candidates tools, suites, suggests, signals, starters, packages, or pure confirmation entries.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)
