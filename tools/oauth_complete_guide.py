#!/usr/bin/env python3
"""Print a single self-contained OAuth guide for the remaining human step.

Combines deep links, ordered checklist, copy-paste commands, recovery notes, and success criteria into one output.
Reduces tool-switching and rediscovery. Soft only. No secrets, no dispatch, no writes.
Usage: python3 tools/oauth_complete_guide.py
"""
from __future__ import annotations

from datetime import datetime, timezone


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"OAUTH COMPLETE GUIDE (single self-contained page; human only)  [{now}]")
    print()
    print("Estimated time: 10-20 minutes (mostly first-time Google Cloud setup).")
    print("Quick path: if you already have a Google Cloud project with YouTube APIs enabled and a Desktop OAuth client, skip to section 2 (mint). Still publish the consent screen to Production before minting.")
    print("STALL_OAUTH_IDLE: 1000+ runs, HIGH suspicion. This is the only remaining blocker.")
    print("Pre-upload is complete (materialize + media_qa PASS). Do not rematerialize if present.")
    print()
    print("=== 1. Google Cloud setup (longest part if first time) ===")
    print("[ ] Create or select a project at https://console.cloud.google.com/")
    print("[ ] Enable YouTube Data API v3: https://console.cloud.google.com/apis/library/youtube.googleapis.com")
    print("[ ] Enable YouTube Analytics API: https://console.cloud.google.com/apis/library/youtubeanalytics.googleapis.com")
    print("[ ] Configure OAuth consent screen: https://console.cloud.google.com/apis/credentials/consent")
    print("    - If Testing mode, add the channel Google account as a Test user.")
    print("    - CRITICAL: Publish the OAuth app to Production (or Internal for Workspace).")
    print("      Testing-mode refresh tokens expire after 7 days.")
    print("      The feedback observation window is uploaded_at + 10 days.")
    print("      A Testing-mode token will expire before collect_feedback can succeed. Publish before minting.")
    print("[ ] Create Desktop app OAuth client: https://console.cloud.google.com/apis/credentials")
    print("    - Create credentials > OAuth client ID > Desktop app")
    print("    - Copy Client ID and Client Secret (never commit them).")
    print()
    print("=== 2. Mint refresh token (preferred non-overlapping scopes) ===")
    print("# In terminal, set env (never print or commit):")
    print("# export YOUTUBE_CLIENT_ID=...")
    print("# export YOUTUBE_CLIENT_SECRET=...")
    print("python3 tools/oauth_exchange.py")
    print("# Open the printed consent URL, grant both scopes (force-ssl + yt-analytics.readonly).")
    print("# force-ssl already covers youtube.upload; do not request overlapping scopes.")
    print("python3 tools/oauth_exchange.py --exchange --out /tmp/youtube-refresh-token")
    print("# Paste the full localhost address-bar URL on stdin.")
    print("# Confirm /tmp/youtube-refresh-token exists and is non-empty (chmod 600).")
    print("# Optional soft format check before secrets (never prints values):")
    print("# export YOUTUBE_REFRESH_TOKEN=$(cat /tmp/youtube-refresh-token)")
    print("# python3 tools/oauth_credential_format_check.py")
    print()
    print("=== 3. Set the three GitHub Actions secrets ===")
    print("gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation")
    print("# paste value into the interactive prompt; never on the command line")
    print("gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation")
    print("gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation")
    print()
    print("=== 4. One dispatch only ===")
    print("gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false")
    print()
    print("=== 5. Success criteria ===")
    print("- Actions run completes (or reports POST_UPLOAD_INCOMPLETE after video id is written).")
    print("- Private video id appears in the Actions log under the upload step.")
    print("- Same id appears in videos/002-.../upload_state.json with privacy=private.")
    print("- Then: python3 tools/human_success_check.py && python3 tools/post_publish_sequence.py")
    print("- Do not invent an id. Do not re-dispatch execute=true until the id is visible in both places.")
    print()
    print("=== Recovery if something fails (most take <5 min) ===")
    print("- Consent rejected / invalid scope: re-run oauth_exchange.py (locked scopes).")
    print("- Access blocked / test-user: add channel account at the consent screen URL above, then re-consent.")
    print("- Refresh token expires after ~7 days: the OAuth app is still in Testing mode. Publish to Production")
    print("  (or switch to Internal for Workspace accounts) for long-lived tokens, then re-mint.")
    print("- No refresh_token: revoke app at https://myaccount.google.com/permissions then re-consent.")
    print("- gh secret set fails: use the exact interactive form above; never pipe the value.")
    print("- Dispatch fails with secret missing: re-set the empty one, wait 30s, re-dispatch once.")
    print("- Video id appears but captions fail: do NOT re-dispatch execute; id is persisted; finish Studio steps manually.")
    print()
    print("Full recovery details: python3 tools/oauth_recovery_hints.py")
    print("Soft format check (before secrets): python3 tools/oauth_credential_format_check.py")
    print("Checkbox version: python3 tools/oauth_step_checklist.py")
    print("Single entry that sequences checks: python3 tools/human_starter.py")
    print("Docs: docs/HUMAN_PRIORITY.md and docs/human_oauth_checklist.md")
    print()
    print("After the private video id appears, observation window is uploaded_at + 10 days before collect_feedback=true.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
