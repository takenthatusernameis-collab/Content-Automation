2026-10-23T11:20:00Z (Run 749)

Operator and agent entry point. Primary status: `python3 tools/status_report.py` or `python3 tools/next_suggestion.py`.

**Current state**
- Videos published: 0
- Primary blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Issue #1. Do not poll.
- Media: Q1 VO + cards + r253 master ready after materialize; do not rematerialize if present. Do not regenerate.

- Master sha256: 4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546 (q1-master-r253.mp4, 328.40s). Do not regenerate while this matches. Do not install the truncated r249 master.
- Preferred unblocked list: complete. tools/phrase_utils.py holds the canonical whole-word shorten (enhanced with which/when/if/while/or separators in Run 749) and ANTI_SLOP_PATTERNS (now includes six additional explanatory/meta fillers). tools/idea_utils.py holds the canonical idea.md field extractor. Key structure suggestors, draft starters, metadata suggestors, and quality tools import from shared helpers. No remaining local shorten copies. packet_rewrite_report.py includes cleaner whole-word script structure starters + originality_report signals. full_qa_report.py / text_qa_report.py cover originality. next_topic.py ranks by mechanism continuity. saturation_guard flags suggest-contract locking loops. Next is the human step or a truly new production capability (not another status/polish/inspection/suggest-contract tool).
- ANTI_SLOP_PATTERNS now includes six additional high-precision explanatory/meta fillers (what you need to understand, let me put it this way, the key takeaway is, if there's one thing + curly, here's what I mean + curly, the reality of the situation is) as of Run 749, plus prior transition/starter and YouTube engagement sets.
- oauth_exchange.py now prints a prominent REQUIRED SCOPES banner (short names + full URIs) when generating the consent URL (Run 746).

**Human step (only action that advances publish)**
1. Follow docs/human_oauth_checklist.md (quick copy-paste sequence + scopes reminder) or `python3 tools/operator_card.py` or `python3 tools/human_next_action.py` or `python3 tools/oauth_exchange.py` (scopes banner at mint).
2. Mint refresh token with scopes: youtube.upload + youtube.force-ssl + yt-analytics.readonly (youtube.upload alone is insufficient).
3. Set the three secrets (human terminal only; paste into prompts; never from an agent):
   gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation
   (same for CLIENT_SECRET and REFRESH_TOKEN)
4. Confirm in GitHub UI: Settings > Secrets and variables > Actions.
5. Dispatch youtube-production.yml with execute=true (privacy stays private). Use `python3 tools/publish_readiness.py` first to confirm local READY_FOR_HUMAN_DISPATCH.

After provider_video_id exists and uploaded_at >=7 days, dispatch collect_feedback=true. Use `python3 tools/after_upload_steps.py` for the exact sequence.

Do not poll secrets. Do not rematerialize if media present. Logs via record_run.py. Do not scaffold Q2. Prefer quality improvements or true capability over more status printers or suggest-contract locks. Do not refresh the checklist banner solely for the timestamp.
