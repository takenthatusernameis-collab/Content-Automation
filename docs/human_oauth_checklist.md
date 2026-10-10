# Human OAuth Checklist

One-time setup to unblock YouTube publish. Videos published stay 0 until these three GitHub Actions secrets exist.

Do not poll secrets from an agent run. Do not commit any secret or token file.

## Steps

- [ ] 1. Open Google Cloud Console and create or select a project.
- [ ] 2. Enable YouTube Data API v3 and YouTube Analytics API.
- [ ] 3. Configure the OAuth consent screen. Add the channel Google account as a test user if the app is in testing mode.
- [ ] 4. Create an OAuth 2.0 client of type Desktop app. Note the Client ID and Client Secret.
- [ ] 5. Mint a refresh token that includes the required scopes:
  - https://www.googleapis.com/auth/youtube.upload
  - https://www.googleapis.com/auth/youtube.force-ssl
  - https://www.googleapis.com/auth/yt-analytics.readonly
  - (or the full youtube scope plus yt-analytics.readonly)
  - youtube.upload alone is insufficient for later caption steps.
- [ ] 6. Run locally (do not paste values into the repo):
  ```bash
  python3 tools/oauth_exchange.py
  # Follow the consent URL, paste the full localhost address-bar URL
  python3 tools/oauth_exchange.py --exchange --out /tmp/youtube-refresh-token
  ```
- [ ] 7. Store the three secrets by pasting into the prompts (never on the command line):
  ```bash
  gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation
  gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation
  gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation
  ```
- [ ] 7b. Confirm the three secrets appear under Settings > Secrets and variables > Actions in the repository (human UI check only). Do not run `gh secret list` from an agent session.
- [ ] 8. Dispatch once:
  ```bash
  gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false
  ```
  Initial privacy stays private. Do not collect_feedback until a video id exists and 7 days have passed.

## Expected outcomes after a successful dispatch

After the single `execute=true` dispatch:

- The Actions workflow run should complete green (or report a specific post-upload incomplete if captions/thumbnail fail after a video id was created).
- A private YouTube video id should appear. Look for it in the workflow log under the upload step and in the packet `upload_state.json` (or equivalent provider state file) that the job may commit.
- Privacy remains private. Do not expect a public video.
- Videos published count in the repository state files should move from 0 once the id is persisted.
- Do not dispatch a second execute until you see a video id. Do not set collect_feedback=true until that id exists and at least 7 days have passed since uploaded_at.
- If the run fails before any video id, check the oauth_preflight step and the three secret presence lines. Do not re-dispatch blindly.

## Common pitfalls

- Wrong scope (missing force-ssl or analytics) causes later caption or analytics failures.
- Pasting secrets into a repo file, commit, or command line instead of the `gh secret set` prompt.
- Dispatching more than once before a video id appears.
- Using the truncated r249 master instead of the r253 padded master.
- Forgetting to add the channel account as a test user when the OAuth app is in Testing status.

## Success criteria

- All three secrets exist as GitHub Actions secrets.
- One workflow run with execute=true completes and produces a private video id.
- Videos published count moves from 0.

See also `python3 tools/operator_card.py` and issue #1.
