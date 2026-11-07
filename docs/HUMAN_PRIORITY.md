# HUMAN PRIORITY — sole remaining step

**Videos published: 0. Pre-upload path complete. Media ready after materialize.**

**STALL_OAUTH_IDLE: 1000+ runs. HIGH suspicion. This is the only blocker.**

## Exact next action (10-20 minutes)

1. Run once:
   ```bash
   python3 tools/human_starter.py
   ```
   It checks environment, prints the HIGH stall status, and shows the one-pager.

2. Follow the printed sequence exactly:
   - Mint refresh token with preferred scopes: `https://www.googleapis.com/auth/youtube.force-ssl` + `https://www.googleapis.com/auth/yt-analytics.readonly`
     (force-ssl already covers youtube.upload and broader management; requesting overlapping scopes like youtube + youtube.upload + force-ssl can cause consent rejection. youtube.upload alone is insufficient for captions.)
   - `gh secret set` the three values (paste into prompts; never on command line)
   - One dispatch:
     ```bash
     gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false
     ```

3. Confirm success by a private video id appearing in the Actions log and packet upload_state.json. Do not invent an id. Do not re-dispatch until the id is visible.

Full details: `docs/human_oauth_checklist.md`

After the id appears: `python3 tools/human_success_check.py` then `python3 tools/post_publish_sequence.py`

Do not poll secrets from agents. Do not scaffold Q2. Do not rematerialize media if present.

This file exists so a human opening the repo sees the single action immediately. Agents: do not rewrite this solely to refresh the date.
