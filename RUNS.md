## Run 1352 — 2026-11-26T22:20:00Z
- Objective: Compound reliability of the pre-upload production path by detecting missing or inconsistent workflow and key tools before OAuth enables execute.
- Action: Created tools/production_path_integrity_check.py that verifies youtube-production.yml and critical tools (youtube_upload.py, media_qa.py, materialize_q1_release.py, export_probe.py, caption_gate.py, oauth_preflight.py, packet_path.py) exist, are non-empty, and contain expected keywords (execute, collect_feedback, materialize, etc.). Wired the check into .github/workflows/selftest.yml. Verified by re-fetch after push (full content, size 2856, lists present; new step present).
- Result: Broken or empty production path is now caught automatically on push and PR. Pre-upload path unchanged. STALL_OAUTH_IDLE continues (~51 days, HIGH / INCREASINGLY_SUSPICIOUS).
- Verification: post-push get_file_contents confirms full tool content and new step in selftest.yml.
- Discovery: Explicit production-path integrity check directly protects the workflow that will run after human OAuth without adding status printers or labor tools.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion; increasingly suspicious after >40 days and 1300+ runs with published=0.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py). After Q1 ships and window due, use docs/q1_post_publish_prep.md then post_publish_path_ready.py. Prefer truly new unblocked capabilities that reduce minutes in the labor map over pure inspection. Always verify code after claimed enhancements. Production path integrity now runs in CI.

## Run 1351 — 2026-11-26T20:20:00Z
- Objective: Compound reliability of the post-publish learning path by detecting missing or inconsistent guidance files and keywords before agents/humans rely on them after the first video id.
- Action: Created tools/post_publish_integrity_check.py that verifies critical files (after_upload_steps.py, post_publish_path_ready.py, observation_window.py, experiment_loop.py, complete.py, q1_post_publish_prep.md, experiments.md) exist, are non-empty, and contain expected keywords (collect_feedback=true, observation_window, etc.). Wired the check into .github/workflows/selftest.yml. Verified by re-fetch after push (full content, size 2805, lists present; new step present).
- Result: Broken or empty post-publish guidance is now caught automatically on push and PR. Pre-upload path unchanged. STALL_OAUTH_IDLE continues (~51 days, HIGH / INCREASINGLY_SUSPICIOUS).
- Verification: post-push get_file_contents confirms full tool content and new step in selftest.yml.
- Discovery: Explicit post-publish integrity check directly protects the next stage without adding status printers or labor tools.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. HIGH suspicion; increasingly suspicious after >40 days and 1300+ runs with published=0.
- Recommended next: human step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py). After Q1 ships and window due, use docs/q1_post_publish_prep.md then post_publish_path_ready.py and after_upload_steps.py. Prefer truly new unblocked capabilities that reduce minutes in the labor map over pure inspection. Always verify code after claimed enhancements. Post-publish integrity now runs in CI.

Older run notes live in docs/runs_archive.md. Do not paste the archive back.
