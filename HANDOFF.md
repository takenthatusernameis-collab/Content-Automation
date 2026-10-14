# HANDOFF

2026-10-14T13:45:00Z (Run 538)

Operator and agent entry point. Primary status: `python3 tools/status_report.py` (self-contained; do not open other files solely to rediscover the lines it already prints). **status_report.py integrity: verified full and executable (tool_integrity_check.py PASS with min-lines now 250). Truncation guard added in Run 535; sensitivity raised in Run 538.**

**Current state**
- Videos published: 0
- Primary blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent: YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN). Issue #1.
- Media: materialize if missing (do not commit); do not rematerialize if present. Target master SHA 4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546. Release tags: VO+cards from q1-media-r249; master from q1-media-r253 (never install truncated r249 master). Verified PRESENT + SHA MATCH in this session after materialize.
- remaining_open_boxes: upload only (captions and thumbnail reviews already recorded).
- Preferred unblocked list: complete. Next is the human step or a truly new small anti-rediscovery item that does not re-verify gates solely for confirmation, does not invent data, and does not refresh the checklist banner solely for its timestamp. Prefer local clone verification for large file updates (or run python3 tools/tool_integrity_check.py).
**Human step (only action that advances publish)**
1. Follow docs/human_oauth_checklist.md or `python3 tools/operator_card.py`.
2. Mint refresh token with scopes: youtube.upload + youtube.force-ssl + yt-analytics.readonly (youtube.upload alone is insufficient).
3. Set the three secrets (human terminal only; paste into prompts; never from an agent):
   ```
   gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation
   gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation
   gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation
   ```
4. Optional human-terminal confirmation (never from an agent): `python3 tools/human_secret_confirm.py` (prints PRESENT/MISSING, never values; exit 0 = all three exist).
5. Dispatch once:
   ```
   gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false
   ```
6. Confirm success only by a private provider video id appearing in the Actions log AND in the packet upload_state.json. Privacy stays private. Do not re-dispatch execute until that id is visible. Do not invent an id. Use `python3 tools/post_upload_confirm.py PATH` (Run 531) for a single-command CONFIRMED/INCOMPLETE check.

**After private video id**
- Observation window: due_at = uploaded_at + 7 calendar days + 3 days Analytics lag (= +10 days). Early collect returns OBSERVATION_WINDOW_NOT_DUE.
- Use `python3 tools/observation_window.py PATH` to see DUE/WAITING without recalculating (Run 526; reusable for future packets).
- Use `python3 tools/post_upload_confirm.py PATH` to confirm provider_video_id + privacy + uploaded_at (Run 531; no invent).
- Use `python3 tools/run_history_summary.py` for last-3 runs concise summary (Run 528; reduces rediscovery of recent history).
- Use `python3 tools/stall_pattern_detector.py` to see if the oauth_idle / published_zero streak is HIGH and prefer new capability (Run 533).
- Use `python3 tools/tool_integrity_check.py` to verify key tools are not truncated/PLACEHOLDER after updates (Run 535).
- Use `python3 tools/media_fingerprint.py` for a quick local PRESENT/MISSING + master SHA match without full media_qa (Run 536).
- Then: `gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=false -f collect_feedback=true`

**Agent rules while stalled**
- Do not poll secrets. Do not dispatch. Do not scaffold Q2. Do not reopen closed briefs.
- Do not rematerialize if media present. Do not re-verify local gates solely for confirmation (STALL_GATE_CONFIRM).
- Do not refresh the human_oauth_checklist.md banner solely for its timestamp (STALL_BANNER_REFRESH).
- Logs via `tools/record_run.py`. See production_rules.md for stall behavior.
- status_report.py now also prints stall_pattern_detector_tool (Run 533), reusable_commands_index_tool (Run 532), post_upload_confirm_tool (Run 531), run_history_summary_tool, run_log_note, observation_window_tool, exact_record_run_usage, status_report_maintainability, exact_post_materialize_verify, exact_oauth_exchange_command, exact_materialize_command, media_release_tags, checklist_banner_status, exact_secret_set_commands, optional_human_secret_confirm, upload_state_status, exact_dispatch_command, exact_collect_command, required_oauth_scopes, privacy_constraint, observation_window_formula, post_upload_confirmation_signals, and the other anti-rediscovery lines. tool_integrity_check_tool one-liner now present in status_report.py (Run 537).

See STATE.md, NEXT.md, RUNS.md, and tools/status_report.py for full history. Preferred list remains complete.
