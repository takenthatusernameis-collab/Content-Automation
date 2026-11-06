#!/usr/bin/env python3
"""One-command starter for the remaining human OAuth step.

Sequences media check + human_preflight.py, long_stall_report.py, recurring_pattern_flag.py,
contract_streak_detector.py, publish_readiness.py, and human_one_pager.py so the human has a single entry point instead of remembering multiple commands.
Does not poll secrets, invent values, dispatch, or write files.
Soft only; does not change gates.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str) -> int:
    cmd = [sys.executable, str(ROOT / "tools" / script)]
    print(f"\n=== Running {script} ===\n")
    proc = subprocess.run(cmd, cwd=ROOT)
    return proc.returncode


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"HUMAN STARTER (single entry for OAuth step; no secrets polled)  [{now}]", flush=True)
    print("Sequences media check + preflight + long stall report + recurring pattern flag + contract streak detector + publish readiness + one-pager.", flush=True)
    print()
    print("Estimated human time: 10-20 minutes total.")
    print("Longest part is usually creating the Google Cloud project + OAuth client if none exists yet (~10-15 min).")
    print("Once Client ID and Client Secret exist, mint + secrets + dispatch is ~5 minutes.")
    print()
    print("=== Google Cloud setup summary (longest part; do this first if no client exists) ===")
    print("1. Open https://console.cloud.google.com/ and create or select a project.")
    print("2. Enable APIs: YouTube Data API v3 and YouTube Analytics API.")
    print("3. Configure OAuth consent screen. Add the channel Google account as a test user if the app is in Testing mode.")
    print("4. Create OAuth 2.0 Client ID of type Desktop app. Copy Client ID and Client Secret.")
    print("5. Set them in your terminal environment (never commit or paste into the repo):")
    print("   export YOUTUBE_CLIENT_ID=...   # then run the mint commands printed later")
    print("Full checklist with pitfalls: docs/human_oauth_checklist.md")
    print()

    # Soft media presence check so fresh clones see the materialize step immediately
    print("\n=== Media presence check ===\n", flush=True)
    media_proc = subprocess.run([sys.executable, str(ROOT / "tools" / "media_fingerprint.py")], cwd=ROOT, text=True, capture_output=True)
    print(media_proc.stdout or media_proc.stderr or "(no output)")
    if "PRESENT" not in (media_proc.stdout or ""):
        print("NOTE: Media not present on this machine.", flush=True)
        print("Run once: python3 tools/materialize_q1_release.py", flush=True)
        print("(requires gh auth; installs verified VO + cards + r253 master; does not commit media)", flush=True)
        print("Then re-run this starter. Do not regenerate.", flush=True)
        print()

    codes = []
    for script in ["human_preflight.py", "long_stall_report.py", "recurring_pattern_flag.py", "contract_streak_detector.py", "publish_readiness.py", "human_one_pager.py"]:
        code = run_tool(script)
        codes.append(code)
        if code != 0:
            print(f"\nHUMAN STARTER FAIL: {script} exited {code}")
            return code

    print("\nHUMAN STARTER PASS: media checked, environment ready, stall HIGH, recurring pattern flagged, contract streak checked, publish readiness shown, one-pager shown.")
    print("Next: follow the exact sequence printed below (mint then secrets then one dispatch).")
    print("Full checklist: docs/human_oauth_checklist.md")
    print()
    print("=== COPY-PASTE READY (full sequence; run in a terminal with client id/secret in env for mint) ===")
    print("# 1. Mint (set YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET in env first; never print them)")
    print("python3 tools/oauth_exchange.py")
    print("python3 tools/oauth_exchange.py --exchange --out /tmp/youtube-refresh-token")
    print("# Paste the full localhost address-bar URL on stdin for the second command.")
    print()
    print("# 2. Set secrets (paste values into the interactive prompts; never on the command line)")
    print("gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation")
    print("gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation")
    print("gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation")
    print()
    print("# 3. Dispatch once")
    print("gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false")
    print()
    print("=== SUCCESS LOOKS LIKE (after one execute=true dispatch) ===")
    print("- Actions workflow run completes (or reports POST_UPLOAD_INCOMPLETE after a video id is written).")
    print("- A private YouTube video id appears in the Actions log under the upload step.")
    print("- The same id appears in the packet upload_state.json with privacy=private.")
    print("- Videos published count moves from 0 once the id is persisted.")
    print("- Do not invent an id. Do not re-dispatch execute until the id is visible in both places.")
    print("- Verify locally: python3 tools/human_success_check.py")
    print("- After the id appears: python3 tools/post_publish_sequence.py")
    print()
    print("Do not poll secrets from an agent. Do not add another consistency printer or contract lock.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
