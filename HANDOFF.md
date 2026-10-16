2026-10-16T22:15:00Z (Run 595)

Operator and agent entry point. Primary status: `python3 tools/status_report.py`. **tools/metadata_qa_report.py added: one-command aggregator of metadata scanners (title, description, tags, first-comment, chapters, thumbnail, end-screen). Content quality remains scanner-backed.**

**Current state**
- Videos published: 0
- Primary blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Issue #1.
- Media: do not rematerialize if present.
- Preferred unblocked list: complete. Next is the human step or a truly new production capability (not another status one-liner). Prefer python3 tools/saturation_guard.py to detect SATURATED_ANTI_REDISCOVERY; python3 tools/quality_scan.py, python3 tools/claim_scan.py, python3 tools/title_scan.py, python3 tools/description_scan.py, python3 tools/tags_scan.py, python3 tools/first_comment_scan.py, python3 tools/chapters_scan.py, python3 tools/thumbnail_scan.py, python3 tools/end_screen_scan.py, python3 tools/cta_suggest.py, python3 tools/draft_starter.py, python3 tools/metadata_starter.py, python3 tools/full_production_starter.py, python3 tools/mechanism_align_scan.py, python3 tools/text_qa_report.py, and python3 tools/metadata_qa_report.py for checks/suggestions; python3 tools/next_suggestion.py for preferred next action.

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
