# RUNS

## Run 1223 — 2026-11-13T03:17:11Z
- Objective: Reduce residual post-publish failure risk by documenting that Testing-mode 7-day refresh tokens expire before the 10-day observation window required for feedback collection.
- Action: Inspected STATE.md, NEXT.md, RUNS.md, human_starter.py, post_publish_sequence.py, human_oauth_checklist.md. Added the window-conflict warning to the observation window section in tools/post_publish_sequence.py and strengthened the common pitfalls note in tools/human_starter.py. No secrets polled, no dispatch, no media writes. Updated state files.
- Result: Primary human entry points and the post-publish sequence now surface the token-lifetime vs observation-window pitfall. Pre-upload path unchanged and reliable. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion, increasingly so with published=0). Pure inspection has low compounding value.
- Verification: Files updated. Logic preserves soft-only contracts. State files updated.
- Discovery: A 7-day Testing-mode token is insufficient for the documented 10-day observation window; publishing the app is required for reliable later collect_feedback.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, use python3 tools/oauth_credential_format_check.py and note token lifetime including window conflict, then secrets + single execute=true). Avoid additional pure confirmation or soft printers while stall persists.



## Run 1222 — 2026-11-13T02:16:00Z
- Objective: Reduce residual human friction on the sole remaining OAuth setup step by making the Testing-mode 7-day refresh token warning consistent across all primary human entry points.
- Action: Inspected STATE.md, NEXT.md, RUNS.md, human_starter.py, oauth_complete_guide.py, human_oauth_checklist.md. Added the Testing-mode token lifetime note (7-day expiry; recommend Production or Internal) to the Google Cloud setup summary and common pitfalls section in tools/human_starter.py. No secrets polled, no dispatch, no media writes. Updated state files.
- Result: All primary human OAuth entry points (starter, complete guide, checklist) now surface the token-lifetime pitfall. Pre-upload path unchanged and reliable. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion, increasingly so with published=0). Pure inspection has low compounding value.
- Verification: File updated and committed. Logic preserves soft-only contracts. State files updated.
- Discovery: Consistency across human entry points reduces the chance a user misses the Testing-mode expiry warning depending on which starter they use.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, use python3 tools/oauth_credential_format_check.py and note token lifetime, then secrets + single execute=true). Avoid additional pure confirmation or soft printers while stall persists.

## Run 1221 — 2026-11-13T01:22:00Z
- Objective: Reduce residual human friction and future failures on the sole remaining OAuth setup step by documenting the Testing-mode 7-day refresh token expiry.
- Action: Inspected STATE.md, NEXT.md, RUNS.md, ROADMAP.md, BLOCKED.md, HANDOFF.md, HUMAN_PRIORITY.md, oauth_complete_guide.py, human_oauth_checklist.md. Added explicit warnings in tools/oauth_complete_guide.py and docs/human_oauth_checklist.md about Testing-mode apps issuing 7-day tokens and the need to publish to Production (or Internal) for long-lived tokens. No secrets polled, no dispatch, no media writes. Updated state files.
- Result: Guides now surface the common token-lifetime pitfall. Pre-upload path unchanged and reliable. STALL_OAUTH_IDLE continues (1000+ runs, HIGH suspicion, increasingly so with published=0). Pure inspection has low compounding value.
- Verification: Files updated and committed. Logic preserves never-print-values and soft-only contracts. State files updated.
- Discovery: Testing-mode token expiry is a frequent silent post-setup failure mode for YouTube OAuth automations; documenting it early reduces failed human attempts without adding a new tool or gate.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py, use python3 tools/oauth_credential_format_check.py and note token lifetime, then secrets + single execute=true). Avoid additional pure confirmation or soft printers while stall persists.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)

Permanent log. Newest first.
