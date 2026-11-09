#!/usr/bin/env python3
"""Print the non-secret YouTube OAuth setup recipe.

Does not call Google. Does not read secret values into output.
Presence is secret names only, matching tools/oauth_preflight.py.
"""

from __future__ import annotations

import os
import sys

SECRET_NAMES = (
    "YOUTUBE_CLIENT_ID",
    "YOUTUBE_CLIENT_SECRET",
    "YOUTUBE_REFRESH_TOKEN",
)
UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
FORCE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
ANALYTICS_SCOPE = "https://www.googleapis.com/auth/yt-analytics.readonly"
FULL_SCOPE = "https://www.googleapis.com/auth/youtube"
REPO = "takenthatusernameis-collab/Content-Automation"


def missing_names() -> list[str]:
    return [name for name in SECRET_NAMES if not os.environ.get(name, "").strip()]


def recipe() -> str:
    scopes = " ".join((UPLOAD_SCOPE, FORCE_SSL_SCOPE, ANALYTICS_SCOPE))
    return f"""YouTube OAuth setup recipe (no secret values)

This script does not call Google and does not print credential values.
The publish gate is still these three GitHub Actions secrets:
  {SECRET_NAMES[0]}
  {SECRET_NAMES[1]}
  {SECRET_NAMES[2]}

1. In Google Cloud Console, create or open a project.
2. Enable YouTube Data API v3 and YouTube Analytics API.
3. Configure the OAuth consent screen. Add the channel Google account as a test user if the app is in testing.
4. Create an OAuth client of type Desktop app. That client id and client secret are the first two secrets. Do not commit them.
5. Mint a refresh token for that client with either:
     {UPLOAD_SCOPE}
     {FORCE_SSL_SCOPE}
     {ANALYTICS_SCOPE}
   or the full scope {FULL_SCOPE} plus {ANALYTICS_SCOPE}.
   youtube.upload alone can insert a video and then fail captions.insert. Do not create that token.
6. Exchange the consent code locally. Do not paste the code or the refresh token into the repository, STATE.md, or a workflow log.
     python3 tools/oauth_exchange.py
     python3 tools/oauth_exchange.py --exchange --out /tmp/youtube-refresh-token
   The first command prints a consent URL when YOUTUBE_CLIENT_ID is set and does not print that id by itself on failure. The browser will not load http://localhost. Paste the full address-bar URL on stdin. The second reads that URL or a raw code and writes the refresh token only outside this repo.
7. Store the three values as Actions secrets by pasting into the prompt, not into the command line:
     gh secret set {SECRET_NAMES[0]} --repo {REPO}
     gh secret set {SECRET_NAMES[1]} --repo {REPO}
     gh secret set {SECRET_NAMES[2]} --repo {REPO}
8. After the three secrets exist, dispatch the production workflow once. Initial privacy stays private.
   Do not pass collect_feedback on this dispatch. Do not pass a different packet.
     gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false
   After a provider video id exists and uploaded_at is at least 10 days old (7 calendar + 3 Analytics lag), dispatch collect_feedback=true.
   Do not dispatch either input while any secret is empty.

Scope string for the consent URL:
  {scopes}
"""


def main() -> int:
    sys.stdout.write(recipe())
    absent = missing_names()
    if absent:
        sys.stdout.write("MISSING " + ",".join(absent) + "\n")
        return 3
    sys.stdout.write("PRESENT " + ",".join(SECRET_NAMES) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
