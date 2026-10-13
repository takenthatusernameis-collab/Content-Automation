# HANDOFF

2026-10-13T12:30:00Z (Run 516)

Operator and agent entry point. Primary status: `python3 tools/status_report.py` (self-contained; do not open other files solely to rediscover the lines it already prints).

**Current state**
- Videos published: 0
- Primary blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent: YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN). Issue #1.
- Media: materialize only if missing (`python3 tools/materialize_q1_release.py`); do not rematerialize if present. Target master SHA 4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546.
- remaining_open_boxes: upload only (captions and thumbnail reviews already recorded).
- Preferred unblocked list: complete. Next is the human step or a truly new small anti-rediscovery item that does not re-verify gates solely for confirmation, does not invent data, and does not refresh the checklist banner solely for its timestamp.

**Human step (only action that advances publish)**
1. Follow docs/human_oauth_checklist.md or `python3 tools/operator_card.py`.
2. Mint refresh token with scopes: youtube.upload + youtube.force-ssl + yt-analytics.readonly (youtube.upload alone is insufficient).
3. Set the three secrets (human terminal only; paste into prompts; never from an agent):
   ```
   gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation
   gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation
   gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation
   ```
4. Dispatch once:
   ```
   gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false
   ```
5. Confirm success only by a private provider video id appearing in the Actions log AND in the packet upload_state.json. Privacy stays private. Do not re-dispatch execute until that id is visible. Do not invent an id.

**After private video id**
- Observation window: due_at = uploaded_at + 7 calendar days + 3 days Analytics lag (= +10 days). Early collect returns OBSERVATION_WINDOW_NOT_DUE.
- Then: `gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=false -f collect_feedback=true`

**Agent rules while stalled**
- Do not poll secrets. Do not dispatch. Do not scaffold Q2. Do not reopen closed briefs.
- Do not rematerialize if media present. Do not re-verify local gates solely for confirmation (STALL_GATE_CONFIRM).
- Do not refresh the human_oauth_checklist.md banner solely for its timestamp (STALL_BANNER_REFRESH).
- Logs via `tools/record_run.py`. See production_rules.md for stall behavior.
- status_report.py now also prints exact_secret_set_commands, exact_dispatch_command, exact_collect_command, required_oauth_scopes, privacy_constraint, observation_window_formula, post_upload_confirmation_signals, and the other anti-rediscovery lines.

See STATE.md, NEXT.md, RUNS.md, and tools/status_report.py for full history. Preferred list remains complete.
