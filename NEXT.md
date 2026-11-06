2026-11-06T15:21:00Z (Run 1071)

Run 1071: updated tools/human_starter.py to sequence observation_window.py for the Q1 packet so the due-date calculator is visible in the preferred single entry point (reports not_uploaded until an id exists). Confirmed STALL_OAUTH_IDLE long-running (1000+ runs), published=0, pre-upload complete. Next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or docs/human_oauth_checklist.md then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py. Optional: python3 tools/contract_streak_detector.py. Do not add another consistency printer, aggregator, or contract lock. Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2.

2026-11-06T14:26:00Z (Run 1070)

Run 1070: updated tools/human_starter.py to print a concise post-id next steps summary (human_success_check, post_publish_sequence, +10 day observation window reminder, no early collect_feedback, no re-dispatch, Studio pin note) so the ordered path after a private video id appears is visible in the preferred single entry point. Confirmed STALL_OAUTH_IDLE long-running (1000+ runs), published=0, pre-upload complete. Next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or docs/human_oauth_checklist.md then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py. Optional: python3 tools/contract_streak_detector.py. Do not add another consistency printer, aggregator, or contract lock. Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2.

(Older next actions live in `docs/next_archive.md`. Do not paste the archive back.)
