# Human OAuth Checklist

**ONLY ACTION NEEDED (as of Run 473, 2026-10-11T13:22:00Z)**

**Banner timestamp intentionally frozen at Run 473 (STALL_BANNER_REFRESH). Agents will not update it solely to refresh the date.**

**Estimated human time: 10-20 minutes** (Google Cloud project setup is the longest part if starting from scratch; mint + secrets + dispatch is ~5 minutes once the client exists).

Videos published: 0. Local Q1 media (VO + cards + r253 master) is ready and gates pass after materialize. After the single execute dispatch, confirm success by a private provider video id appearing in the Actions log and in the packet upload_state.json (privacy stays private). Do not invent an id. Do not re-dispatch until that id is visible.

Do not poll secrets from an agent run. Do not commit any secret or token file.

## Quick start (recommended)

Run once for environment check + media presence + stall status + recurring pattern flag + contract streak + readiness + exact next commands + observation window reminder:

```bash
python3 tools/human_starter.py
```

It now sequences: media presence check (surfaces materialize if needed) + human_preflight + long_stall_report + recurring_pattern_flag + contract_streak_detector + publish_readiness + human_one_pager + observation_window.py (Q1 packet; reports not_uploaded until an id exists).

Then follow the printed sequence (oauth_exchange, gh secret set, one dispatch). The starter also prints a concise post-id next steps summary (success check, post_publish_sequence, +10 day observation window, no early collect, no re-dispatch, Studio pin reminder).

## Quick copy-paste sequence (for the human)

**Scopes reminder (must be granted during mint):** youtube.upload + youtube.force-ssl + yt-analytics.readonly (youtube.upload alone is insufficient).

Once Google Cloud client is created and scopes are ready:

```bash
# 1. Mint token (run twice as shown; paste full localhost URL on second)
python3 tools/oauth_exchange.py
python3 tools/oauth_exchange.py --exchange --out /tmp/youtube-refresh-token

# 2. Set secrets (paste values into the interactive prompts; never on the command line)
gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation
gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation
gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation

# 3. Optional confirm (human terminal only; never from agent)
python3 tools/human_secret_confirm.py

# 4. Dispatch once
gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false
```

Then watch the Actions run for a private video id. Do not dispatch again until that id appears in upload_state.json.

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
- [ ] 7c. Optional terminal confirmation (human terminal only, never from an agent or workflow):
  ```bash
  python3 tools/human_secret_confirm.py
  ```
  It prints PRESENT/MISSING for each name and never shows values. Exit 0 means all three exist.
- [ ] 8. Dispatch once:
  ```bash
  gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false
  ```
  Initial privacy stays private. Do not collect_feedback until a video id exists and 7 days have passed.

## Current Google Cloud UI tip (Run 1079)

Navigation may show "Google Auth platform" or "APIs & Services". For the Desktop client:

- Go to https://console.cloud.google.com/apis/credentials or the Clients page under Google Auth platform.
- Click Create credentials > OAuth client ID (or Create client).
- Choose Application type: Desktop app.
- Name it and Create. Copy Client ID and Client Secret immediately.
- For consent screen: ensure YouTube Data API v3 and YouTube Analytics API are enabled first; add the channel Google account as a test user if status is Testing.

This tip reduces navigation friction if the console labels have shifted. Core steps remain unchanged.

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

## Success verification (after dispatch)

Once the three secrets are set and you dispatch with execute=true:

- Watch the Actions run. Look for a private video id in the upload step log.
- Confirm the packet has upload_state.json with a real provider_video_id and privacy=private.
- Local one-command check: `python3 tools/human_success_check.py` (reports PRESENT only on a real non-placeholder id; never invents).
- Videos published in STATE.md should move from 0 only after that id is persisted by the job.
- If the job fails before any id, check the oauth_preflight step and secret presence. Do not re-dispatch blindly.
- After the id exists, run `python3 tools/post_publish_sequence.py` for the ordered next steps (observation window, feedback collect, experiment baseline, Studio pin/end-screen).

Do not invent an id. Do not re-upload the master on POST_UPLOAD_INCOMPLETE.

## Note for the human (as of Run 473)

Agents have verified materialize + all local gates on fresh clones across ~181+ runs with no change in the external blocker. The long oauth_idle_without_publish stall continues and is machine-visible via stall_watch.py. The pre-upload path is stable. Further pure-verification agent runs have diminishing returns. The only remaining step that advances the system is completing the three secrets above and the one dispatch. Once a private video id appears, the system can move to feedback collection after the observation window. Preferred agent work while stalled is listed in status_report.py (list complete; prioritize human step or truly new small anti-rediscovery items). HANDOFF.md surfaces the while-stalled guidance. Run 468 restored NEXT.md under the size cap. Run 469–473 keep the banner current with confirmation signals. Banner timestamp intentionally frozen at Run 473 (STALL_BANNER_REFRESH); agents will not refresh it solely for the date.

## Current stall note (Run 1079)
The STALL_OAUTH_IDLE has persisted across 1000+ runs with videos published remaining 0. This is HIGH suspicion and the sole primary blocker. Complete the three secrets and single dispatch as soon as practical. Start with `python3 tools/human_starter.py` (sequences media presence check + preflight + long stall report + recurring pattern flag + contract streak detector + publish readiness + one-pager + observation_window for Q1, and prints concise post-id next steps summary). After dispatch: `python3 tools/human_success_check.py` then `python3 tools/post_publish_sequence.py`. Do not poll from agents. Do not add further contract locks, aggregators, or soft reports while stalled. Prefer the human step now. Added current UI tip for Google Cloud Clients page / Desktop app to reduce navigation friction.
