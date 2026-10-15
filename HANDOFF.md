2026-10-15T19:30:00Z (Run 568)

Operator and agent entry point. Primary status: `python3 tools/status_report.py`. **tools/title_scan.py strengthened with context snippets and additional high-precision weak title patterns (clickbait/weak claims); production rules updated. Detection gates remain unchanged otherwise.**

**Current state**
- Videos published: 0
- Primary blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Issue #1.
- Media: do not rematerialize if present.
- Preferred unblocked list: complete. Next is the human step or a truly new production capability (not another status one-liner). Prefer python3 tools/saturation_guard.py to detect SATURATED_ANTI_REDISCOVERY; python3 tools/quality_scan.py, python3 tools/claim_scan.py, and python3 tools/title_scan.py for checks; python3 tools/next_suggestion.py for preferred next action.

**Human step (only action that advances publish)**
1. Follow docs/human_oauth_checklist.md or `python3 tools/operator_card.py` or `python3 tools/human_next_action.py` or `python3 tools/next_suggestion.py`.
2. Mint refresh token with scopes: youtube.upload + youtube.force-ssl + yt-analytics.readonly (youtube.upload alone is insufficient).
3. Set the three secrets (human terminal only; paste into prompts; never from an agent):
   gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation
   (same for CLIENT_SECRET and REFRESH_TOKEN)
4. Confirm in GitHub UI: Settings > Secrets and variables > Actions.
5. Dispatch youtube-production.yml with execute=true (privacy stays private). Use `python3 tools/publish_readiness.py` first to confirm local READY_FOR_HUMAN_DISPATCH.

After provider_video_id exists and uploaded_at >=7 days, dispatch collect_feedback=true. Use `python3 tools/after_upload_steps.py` for the exact sequence.

Do not poll secrets. Do not rematerialize if media present. Logs via record_run.py. Do not scaffold Q2. Prefer quality improvements or true capability over more status printers while saturation_guard reports SATURATED_ANTI_REDISCOVERY.
