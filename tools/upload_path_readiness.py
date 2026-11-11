#!/usr/bin/env python3
"""Structural readiness check for the pre-upload / YouTube upload path.

Verifies presence of the dry-run uploader, API adapter, OAuth helpers,
and related contracts. Prints the fail-closed human + dispatch sequence.
Does not poll secrets, dispatch, write files, or invent credentials.
Reduces rediscovery of upload-path readiness across stalled runs.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

KEY_FILES = [
    "tools/youtube_upload.py",
    "tools/youtube_api.py",
    "tools/youtube_upload_contract.py",
    "tools/oauth_complete_guide.py",
    "tools/oauth_preflight.py",
    "tools/oauth_exchange.py",
    "tools/human_starter.py",
    "docs/HUMAN_PRIORITY.md",
    "docs/human_oauth_checklist.md",
]


def main() -> int:
    print("UPLOAD PATH READINESS (structural only; no invent, no poll, no writes, no dispatch)")
    print()
    present = 0
    for rel in KEY_FILES:
        path = ROOT / rel
        status = "PRESENT" if path.is_file() else "MISSING"
        if status == "PRESENT":
            present += 1
        print(f"  {status}  {rel}")
    print()
    print(f"Present: {present} / {len(KEY_FILES)}")
    if present == len(KEY_FILES):
        print("All key upload-path files are present.")
    else:
        print("Some upload-path files are missing. Do not invent them.")
    print()
    print("Fail-closed sequence to first private upload (human step required):")
    print("  1. python3 tools/oauth_complete_guide.py")
    print("     # or python3 tools/human_starter.py or open docs/HUMAN_PRIORITY.md")
    print("  2. Mint refresh token with preferred scopes (see guide).")
    print("  3. gh secret set YOUTUBE_CLIENT_ID / YOUTUBE_CLIENT_SECRET / YOUTUBE_REFRESH_TOKEN")
    print("     (paste into prompts; never on command line; never commit)")
    print("  4. One dispatch only:")
    print("     gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation \\")
    print("       -f execute=true -f collect_feedback=false")
    print("  5. Confirm private video id appears in Actions log and packet upload_state.json.")
    print("     Then: python3 tools/post_upload_confirm.py <packet>")
    print("  6. Do not re-dispatch until id is visible. Privacy stays private.")
    print()
    print("After id + window: use tools/feedback_ingestion_readiness.py and tools/experiment_loop_readiness.py.")
    print("Human OAuth remains the only blocker. Do not poll secrets. Do not rematerialize if media present.")
    print("UPLOAD PATH READINESS complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
