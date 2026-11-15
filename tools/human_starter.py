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
    print("Sequences media check + preflight + long stall report + recurring pattern flag + contract streak detector + publish readiness + one-pager + observation window reminder + saturation guard.", flush=True)
    print()
    print("=== SATURATION NOTE ===")
    print("Recent agent runs (1281-1285) saturated on polishing tools/feedback_to_topic_suggest.py while videos published remain 0.")
    print("saturation_guard.py now flags SATURATED_ANTI_REDISCOVERY. Further soft-tool polishing has diminishing returns until after first private video id exists.")
    print("The only advancing action is the human OAuth step below. Do not spend more runs on suggestor polish.")
    print()
    print("Estimated human time: 10-20 minutes total.")
    print("Longest part is usually creating the Google Cloud project + OAuth client if none exists yet (~10-15 min).")
    print("Once Client ID and Client Secret exist, mint + secrets + dispatch is ~5 minutes.")
    print()
    print("=== PHASED ACTION PLAN (follow in order; do not skip) ===")
    print("Phase A (if no OAuth client yet): Google Cloud project + enable APIs + consent screen.")
    print("  CRITICAL: Publish the OAuth consent screen to Production (or Internal for Workspace).")
    print("  Testing mode tokens expire after 7 days; the feedback observation window is +10 days.")
    print("  A 7-day token will expire before collect_feedback can run. Publish before minting.")
    print("  Then create Desktop client and copy Client ID + Secret.")
    print("Phase B: Mint refresh token with preferred scopes (force-ssl + yt-analytics.readonly).")
    print("Phase C: gh secret set the three values (interactive paste only).")
    print("Phase D: One dispatch with execute=true. Then confirm private video id in Actions log + upload_state.json.")
    print("Full self-contained version: python3 tools/oauth_complete_guide.py")
    print()
    print("=== Google Cloud setup summary (longest part; do this first if no client exists) ===")
    print("1. Open https://console.cloud.google.com/ and create or select a project.")
    print("2. Enable APIs: YouTube Data API v3 and YouTube Analytics API.")
    print("3. Configure OAuth consent screen. Add the channel Google account as a test user if the app is in Testing mode.")
    print("   IMPORTANT: Apps left in Testing mode issue refresh tokens that expire after 7 days.")
    print("   For long-lived tokens (recommended), publish the app to Production (or Internal for Workspace).")
    print("4. Create OAuth 2.0 Client ID of type Desktop app. Copy Client ID and Client Secret.")
    print("5. Set them in your terminal environment (never commit or paste into the repo):")
    print("   export YOUTUBE_CLIENT_ID=...   # then run the mint commands printed later")
    print("Full checklist with pitfalls: docs/human_oauth_checklist.md")
    print("Single self-contained guide (deep links + copy-paste + recovery): python3 tools/oauth_complete_guide.py")
    print("Soft format check (after export; never prints values): python3 tools/oauth_credential_format_check.py")
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
    for script in [
        "human_preflight.py",
        "long_stall_report.py",
        "recurring_pattern_flag.py",
        "contract_streak_detector.py",
        "publish_readiness.py",
        "human_one_pager.py",
    ]:
        codes.append(run_tool(script))

    print("\n=== After the private video id appears (do this next; observation window is +10 days) ===")
    print("- Confirm with: python3 tools/human_success_check.py (reports PRESENT only on a real id).")
    print("- Then run: python3 tools/post_publish_sequence.py for the ordered steps.")
    print("- Observation window: first 7 calendar days of the video + 3 days Analytics lag = due at uploaded_at + 10 days.")
    print("- Do not dispatch collect_feedback=true until that due date. Early collect returns OBSERVATION_WINDOW_NOT_DUE.")
    print("- Do not re-dispatch execute=true. Privacy stays private. Do not invent metrics or an id.")
    print("- Studio pin and end screen are manual in YouTube Studio (Data API cannot finish them).")
    print("- Exact due date calculator: python3 tools/observation_window.py videos/002-stop-deciding-what-to-work-on-every-morning")
    print()
    print("=== Common pitfalls (avoid these to finish in one pass) ===")
    print("- Missing or overlapping scopes: preferred are youtube.force-ssl + yt-analytics.readonly (force-ssl covers upload; overlapping youtube + upload + force-ssl can cause consent rejection; upload alone is insufficient for captions).")
    print("- Pasting secrets on the command line or into a file instead of the interactive gh secret set prompt.")
    print("- Dispatching a second execute=true before a private video id appears in both the Actions log and upload_state.json.")
    print("- Using the truncated r249 master; materialize installs the verified r253 only.")
    print("- Forgetting to add the channel Google account as a test user when the OAuth consent screen is in Testing mode.")
    print("- Leaving the OAuth app in Testing mode (refresh tokens expire after ~7 days). Publish to Production or Internal for long-lived tokens. The observation window is +10 days, so a 7-day token will expire before feedback collection unless the app is published.")
    print("Full list: docs/human_oauth_checklist.md#common-pitfalls")
    print()
    print("Do not poll secrets from an agent. Do not add another consistency printer or contract lock.")
    print("Checkbox checklist: python3 tools/oauth_step_checklist.py")
    print("Single self-contained guide: python3 tools/oauth_complete_guide.py")
    print("Soft format check (before secrets): python3 tools/oauth_credential_format_check.py")
    print("Recovery hints if a step fails: python3 tools/oauth_recovery_hints.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
