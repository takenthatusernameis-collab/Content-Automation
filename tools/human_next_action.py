#!/usr/bin/env python3
"""Concise human next action summary for the current primary blocker.

Prints only the essential OAuth secret setup steps. Does not poll secrets,
does not invent values, does not dispatch workflows, and does not restate
the full checklist. Reduces rediscovery of the exact human path while
STALL_OAUTH_IDLE continues.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    print("HUMAN NEXT ACTION (concise; human-only; do not invent credentials)")
    print("Primary blocker: YouTube Data API OAuth secrets absent on GitHub Actions.")
    print("Videos published remain 0 until the three secrets are set and execute is dispatched.")
    print("Confirm local readiness first (no poll, no materialize): python3 tools/publish_readiness.py")
    print("  (expects status: READY_FOR_HUMAN_DISPATCH when media fingerprint is PRESENT and next_action is upload-blocked)")
    print("Stall length signal: python3 tools/stall_duration.py")
    print("Anti-rediscovery saturation: python3 tools/saturation_guard.py")
    print()
    print("Exact human steps:")
    print("1. Google Cloud: enable YouTube Data API v3 + YouTube Analytics API.")
    print("   Create OAuth 2.0 Desktop client. Configure consent screen; add channel account as test user if needed.")
    print("2. Mint refresh token with scopes:")
    print("   - https://www.googleapis.com/auth/youtube.upload")
    print("   - https://www.googleapis.com/auth/youtube.force-ssl")
    print("   - https://www.googleapis.com/auth/yt-analytics.readonly")
    print("3. Local exchange (never commit or log tokens):")
    print("   python3 tools/oauth_exchange.py")
    print("   python3 tools/oauth_exchange.py --exchange --out /tmp/youtube-refresh-token")
    print("4. Set secrets (paste into prompts; never on the command line):")
    print("   gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation")
    print("   gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation")
    print("   gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation")
    print("5. Confirm in GitHub UI only: Settings > Secrets and variables > Actions (three names present).")
    print("   Optional terminal confirm (human terminal only): python3 tools/human_secret_confirm.py")
    print("6. Dispatch .github/workflows/youtube-production.yml with execute=true (privacy stays private).")
    print()
    print("After a private provider_video_id appears in upload_state.json, wait >=7 days then dispatch collect_feedback=true.")
    print("Post-upload sequence (once id exists): python3 tools/after_upload_steps.py")
    print("Do not poll secrets from an agent run. Full checklist: docs/human_oauth_checklist.md")
    print("Operator card and escalation: docs/operator_escalation.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
