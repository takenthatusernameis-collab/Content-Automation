#!/usr/bin/env python3
"""Print structured recovery hints for common human OAuth step failures.

Reduces rediscovery of fixes when the first attempt hits a pitfall.
Soft only. No secrets, no dispatch, no writes.
Usage: python3 tools/oauth_recovery_hints.py
"""
from __future__ import annotations

from datetime import datetime, timezone


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"OAUTH RECOVERY HINTS (human only; no secrets polled)  [{now}]")
    print()
    print("Use after a failed mint, consent, or secret-set attempt.")
    print("Most recoveries take <5 minutes once the root cause is identified.")
    print()
    print("1. Consent rejected or 'invalid scope' / overlapping scopes:")
    print("   Cause: Requested youtube.upload in addition to force-ssl, or full youtube + upload.")
    print("   Fix: Re-run python3 tools/oauth_exchange.py (uses locked non-overlapping scopes:")
    print("        youtube.force-ssl + yt-analytics.readonly only). Force-ssl already covers upload.")
    print("   Then re-exchange with the new code.")
    print()
    print("2. 'Access blocked: This app's request is invalid' or test-user error:")
    print("   Cause: OAuth consent screen in Testing mode and channel account not added as test user.")
    print("   Fix: Console > APIs & Services > OAuth consent screen > Test users > Add users.")
    print("   Direct: https://console.cloud.google.com/apis/credentials/consent")
    print("   Then re-open the consent URL.")
    print()
    print("3. No refresh_token returned (only access_token):")
    print("   Cause: Missing prompt=consent or previous consent without offline access.")
    print("   Fix: The exchange tool already sets prompt=consent and access_type=offline.")
    print("   Revoke the app at https://myaccount.google.com/permissions then re-consent.")
    print()
    print("4. gh secret set fails or secret not visible in Actions:")
    print("   Cause: Pasted value on command line instead of interactive prompt, or wrong repo.")
    print("   Fix: Run exactly: gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation")
    print("   (paste into the prompt that appears; never echo or pipe the value).")
    print("   Confirm in GitHub UI Settings > Secrets and variables > Actions (human only).")
    print()
    print("5. Dispatch fails immediately with secret missing:")
    print("   Cause: One of the three secrets empty or not yet propagated.")
    print("   Fix: Re-set the missing one. Wait 30s then re-dispatch once.")
    print("   Do not re-dispatch execute=true until a private video id appears in the log AND upload_state.json.")
    print()
    print("6. Video id appears but captions/thumbnail fail (POST_UPLOAD_INCOMPLETE):")
    print("   Cause: Expected; Data API upload succeeded but secondary assets incomplete.")
    print("   Fix: Do NOT re-dispatch execute. The id is persisted. Finish remaining Studio steps manually.")
    print("   Then run python3 tools/human_success_check.py && python3 tools/post_publish_sequence.py")
    print()
    print("Full sequence and deep links: python3 tools/oauth_step_checklist.py")
    print("Single entry: python3 tools/human_starter.py")
    print("STALL_OAUTH_IDLE remains primary until the three secrets exist and one execute=true succeeds.")
    print()
    print("7. Refresh token stops working after ~7 days (invalid_grant or auth errors on later dispatch):")
    print("   Cause: OAuth consent screen still in Testing mode. Testing apps issue 7-day refresh tokens.")
    print("   The observation window for feedback is uploaded_at + 10 days, so a 7-day token expires before collect_feedback.")
    print("   Fix: Publish the OAuth app to Production (or Internal for Workspace) in Google Cloud Console.")
    print("   Direct: https://console.cloud.google.com/apis/credentials/consent")
    print("   Then re-mint a new long-lived refresh token with python3 tools/oauth_exchange.py and update the YOUTUBE_REFRESH_TOKEN secret.")
    print("   Do not re-dispatch execute=true if a video id already exists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
