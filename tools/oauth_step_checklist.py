#!/usr/bin/env python3
"""Print a checkbox-style checklist for the remaining human OAuth step.

Reduces rediscovery of the exact sequence. Soft only. No secrets, no dispatch, no writes.
Usage: python3 tools/oauth_step_checklist.py
"""
from __future__ import annotations

from datetime import datetime, timezone

def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"OAUTH STEP CHECKLIST (human only; no secrets polled)  [{now}]")
    print()
    print("Estimated time: 10-20 minutes (mostly Google Cloud setup if first time).")
    print()
    print("[ ] 1. Google Cloud project exists with YouTube Data API v3 + YouTube Analytics API enabled.")
    print("      Direct: https://console.cloud.google.com/apis/library/youtube.googleapis.com")
    print("      Direct: https://console.cloud.google.com/apis/library/youtubeanalytics.googleapis.com")
    print("[ ] 2. OAuth consent screen configured. Channel Google account added as test user if Testing mode.")
    print("      Direct: https://console.cloud.google.com/apis/credentials/consent")
    print("[ ] 3. Desktop app OAuth client created. Client ID and Client Secret copied (never commit them).")
    print("      Direct: https://console.cloud.google.com/apis/credentials")
    print("      (Create credentials > OAuth client ID > Desktop app)")
    print("[ ] 4. In terminal: export YOUTUBE_CLIENT_ID=... and YOUTUBE_CLIENT_SECRET=... (env only).")
    print("[ ] 5. python3 tools/oauth_exchange.py   # prints consent URL; open it and grant both scopes")
    print("      Scopes: youtube.force-ssl + yt-analytics.readonly (do not add youtube.upload; overlapping can reject).")
    print("[ ] 6. After consent, paste the full localhost address-bar URL into:")
    print("      python3 tools/oauth_exchange.py --exchange --out /tmp/youtube-refresh-token")
    print("[ ] 7. Confirm the file /tmp/youtube-refresh-token exists and is non-empty (chmod 600).")
    print("[ ] 8. gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation")
    print("      (paste value into prompt; never on command line)")
    print("[ ] 9. Same for YOUTUBE_CLIENT_SECRET and YOUTUBE_REFRESH_TOKEN.")
    print("[ ] 10. One dispatch only:")
    print("       gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false")
    print("[ ] 11. Wait for Actions run. Success = private video id in log + videos/.../upload_state.json.")
    print("       Then: python3 tools/human_success_check.py && python3 tools/post_publish_sequence.py")
    print()
    print("Full details and pitfalls: docs/human_oauth_checklist.md")
    print("Single self-contained guide: python3 tools/oauth_complete_guide.py")
    print("Recovery hints if something fails: python3 tools/oauth_recovery_hints.py")
    print("Single entry: python3 tools/human_starter.py")
    print("Do not invent an id. Do not re-dispatch until the id is visible.")
    print("STALL_OAUTH_IDLE remains the primary blocker (1000+ runs).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
