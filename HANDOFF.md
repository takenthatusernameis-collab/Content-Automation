2026-10-20T21:30:00Z (Run 689)

Operator and agent entry point. Primary status: `python3 tools/status_report.py` or `python3 tools/next_suggestion.py`.

**Current state**
- Videos published: 0
- Primary blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Issue #1. Do not poll.
- Media: Q1 VO + cards + r253 master ready after materialize; do not rematerialize if present. Do not regenerate.
- Preferred unblocked list: complete (research starters, draft coaches, quality/claim/metadata scanners, full_production_starter and package starters, experiment helpers, saturation_guard, stall_duration, publish_readiness, research_source_extract_check, topic_suggest with expanded candidate pool from tools/topic_candidates.json + idea skeletons via paste_block; now locked by tools/topic_suggest_contract.py; title_suggest now locked by tools/title_suggest_contract.py; description_suggest now locked by tools/description_suggest_contract.py; tags_suggest now locked by tools/tags_suggest_contract.py; first_comment_suggest now locked by tools/first_comment_suggest_contract.py; chapters_suggest now locked by tools/chapters_suggest_contract.py; end_screen_suggest now locked by tools/end_screen_suggest_contract.py). Next is the human step or a truly new production capability (not another status/polish/inspection tool).
- Claim path: filled Source column values (Primary claims or Source log tables) and non-placeholder bullets from research.md or sources.md are auto-extracted by claim_scan.py. Documented in research_sources_starter, research_brief_starter, research_package_starter, pre_production_package_starter, full_production_starter (Runs 659-665), script_writer.md (Run 667), script_expander.md (Run 668). Table extraction is header-aware and combines Claim+Source (Run 669). Preview with python3 tools/research_source_extract_check.py PATH (Run 674). Topic suggestions: python3 tools/topic_suggest.py (dynamic next Q id + idea.md skeletons via idea_brief.paste_block + candidates from tools/topic_candidates.json; contract-locked Run 683). Title suggestions: python3 tools/title_suggest.py (mechanism-aligned; contract-locked Run 684). Description suggestions: python3 tools/description_suggest.py (mechanism-aligned; contract-locked Run 685). Tags suggestions: python3 tools/tags_suggest.py (mechanism-aligned; contract-locked Run 686). First-comment suggestions: python3 tools/first_comment_suggest.py (mechanism-aligned; contract-locked Run 687). Chapters suggestions: python3 tools/chapters_suggest.py (mechanism-aligned; contract-locked Run 688). End-screen suggestions: python3 tools/end_screen_suggest.py (mechanism-aligned; contract-locked Run 689).

**Human step (only action that advances publish)**
1. Follow docs/human_oauth_checklist.md (ONLY ACTION NEEDED banner frozen at Run 473) or `python3 tools/operator_card.py` or `python3 tools/human_next_action.py`.
2. Mint refresh token with scopes: youtube.upload + youtube.force-ssl + yt-analytics.readonly (youtube.upload alone is insufficient).
3. Set the three secrets (human terminal only; paste into prompts; never from an agent):
   gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation
   (same for CLIENT_SECRET and REFRESH_TOKEN)
4. Confirm in GitHub UI: Settings > Secrets and variables > Actions.
5. Dispatch youtube-production.yml with execute=true (privacy stays private). Use `python3 tools/publish_readiness.py` first to confirm local READY_FOR_HUMAN_DISPATCH.

After provider_video_id exists and uploaded_at >=7 days, dispatch collect_feedback=true. Use `python3 tools/after_upload_steps.py` for the exact sequence.

Do not poll secrets. Do not rematerialize if media present. Logs via record_run.py. Do not scaffold Q2. Prefer quality improvements, true capability, or anti-rediscovery documentation over more status printers while saturation_guard reports SATURATED_ANTI_REDISCOVERY. Do not refresh the checklist banner solely for the timestamp.

# Previous handoff preserved below for context

2026-10-20T20:15:00Z (Run 688)

Operator and agent entry point. Primary status: `python3 tools/status_report.py` or `python3 tools/next_suggestion.py`.

**Current state**
- Videos published: 0
- Primary blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Issue #1. Do not poll.
- Media: Q1 VO + cards + r253 master ready after materialize; do not rematerialize if present. Do not regenerate.
- Preferred unblocked list: complete (research starters, draft coaches, quality/claim/metadata scanners, full_production_starter and package starters, experiment helpers, saturation_guard, stall_duration, publish_readiness, research_source_extract_check, topic_suggest with expanded candidate pool from tools/topic_candidates.json + idea skeletons via paste_block; now locked by tools/topic_suggest_contract.py; title_suggest now locked by tools/title_suggest_contract.py; description_suggest now locked by tools/description_suggest_contract.py; tags_suggest now locked by tools/tags_suggest_contract.py; first_comment_suggest now locked by tools/first_comment_suggest_contract.py; chapters_suggest now locked by tools/chapters_suggest_contract.py). Next is the human step or a truly new production capability (not another status/polish/inspection tool).
- Claim path: filled Source column values (Primary claims or Source log tables) and non-placeholder bullets from research.md or sources.md are auto-extracted by claim_scan.py. Documented in research_sources_starter, research_brief_starter, research_package_starter, pre_production_package_starter, full_production_starter (Runs 659-665), script_writer.md (Run 667), script_expander.md (Run 668). Table extraction is header-aware and combines Claim+Source (Run 669). Preview with python3 tools/research_source_extract_check.py PATH (Run 674). Topic suggestions: python3 tools/topic_suggest.py (dynamic next Q id + idea.md skeletons via idea_brief.paste_block + candidates from tools/topic_candidates.json; contract-locked Run 683). Title suggestions: python3 tools/title_suggest.py (mechanism-aligned; contract-locked Run 684). Description suggestions: python3 tools/description_suggest.py (mechanism-aligned; contract-locked Run 685). Tags suggestions: python3 tools/tags_suggest.py (mechanism-aligned; contract-locked Run 686). First-comment suggestions: python3 tools/first_comment_suggest.py (mechanism-aligned; contract-locked Run 687). Chapters suggestions: python3 tools/chapters_suggest.py (mechanism-aligned; contract-locked Run 688).

**Human step (only action that advances publish)**
1. Follow docs/human_oauth_checklist.md (ONLY ACTION NEEDED banner frozen at Run 473) or `python3 tools/operator_card.py` or `python3 tools/human_next_action.py`.
2. Mint refresh token with scopes: youtube.upload + youtube.force-ssl + yt-analytics.readonly (youtube.upload alone is insufficient).
3. Set the three secrets (human terminal only; paste into prompts; never from an agent):
   gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation
   (same for CLIENT_SECRET and REFRESH_TOKEN)
4. Confirm in GitHub UI: Settings > Secrets and variables > Actions.
5. Dispatch youtube-production.yml with execute=true (privacy stays private). Use `python3 tools/publish_readiness.py` first to confirm local READY_FOR_HUMAN_DISPATCH.

After provider_video_id exists and uploaded_at >=7 days, dispatch collect_feedback=true. Use `python3 tools/after_upload_steps.py` for the exact sequence.

Do not poll secrets. Do not rematerialize if media present. Logs via record_run.py. Do not scaffold Q2. Prefer quality improvements, true capability, or anti-rediscovery documentation over more status printers while saturation_guard reports SATURATED_ANTI_REDISCOVERY. Do not refresh the checklist banner solely for the timestamp.
