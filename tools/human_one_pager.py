#!/usr/bin/env python3
"""Print a single-page human summary for the remaining OAuth/dispatch step.

Aggregates time estimate, key metadata glance, exact commands, and success criteria
so the human does not need to open multiple files or rediscover the sequence.
Does not poll secrets, invent values, dispatch, or write files.
Reusable across future stalled runs and packets.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
EXPECTED_MASTER_SHA = "4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546"
DISPATCH = (
    "gh workflow dispatch youtube-production.yml "
    "--repo takenthatusernameis-collab/Content-Automation "
    "-f execute=true -f collect_feedback=false"
)


def extract_section(text: str, header: str) -> str:
    lines = text.splitlines()
    capture = False
    collected = []
    for line in lines:
        if line.strip() == header:
            capture = True
            continue
        if capture and line.startswith("## ") and line.strip() != header:
            break
        if capture:
            collected.append(line)
    return "\n".join(collected).strip()


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    publish = packet / "publish.md"
    if not publish.is_file():
        print(f"HUMAN ONE-PAGER FAIL: publish.md missing in {packet}")
        return 1

    text = publish.read_text(encoding="utf-8")
    title = extract_section(text, "## Title to upload").splitlines()
    title = title[0].strip() if title else "(missing)"

    print("HUMAN ONE-PAGER (STALL_OAUTH_IDLE; published=0)")
    print("Estimated human time: 10-20 minutes (setup longest if from scratch).")
    print()
    print("1. Metadata glance (fail-closed):")
    print(f"   TITLE: {title}")
    print(f"   MASTER SHA (use r253 only): {EXPECTED_MASTER_SHA}")
    print("   Full review: python3 tools/pre_dispatch_review.py")
    print()
    print("2. Exact sequence (human terminal only; never paste secrets into files or CLI):")
    print("   python3 tools/oauth_exchange.py")
    print("   python3 tools/oauth_exchange.py --exchange --out /tmp/youtube-refresh-token")
    print("   gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation")
    print("   gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation")
    print("   gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation")
    print("   (scopes must include youtube.upload + youtube.force-ssl + yt-analytics.readonly)")
    print()
    print("3. Dispatch once:")
    print(f"   {DISPATCH}")
    print()
    print("4. Success criteria:")
    print("   - Private provider_video_id appears in Actions log AND packet/upload_state.json")
    print("   - Privacy stays private")
    print("   - Videos published moves from 0")
    print("   - Do not re-dispatch until id is visible. Do not invent an id.")
    print()
    print("Full checklist: docs/human_oauth_checklist.md")
    print("Do not poll secrets from an agent. Do not add another consistency printer.")
    print("HUMAN ONE-PAGER PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
