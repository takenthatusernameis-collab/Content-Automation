#!/usr/bin/env python3
"""Print the exact next sequence after a private provider_video_id exists.

Fail-closed reminder so the human (or later agent) does not rediscover the
observation window, collect_feedback dispatch, and experiment steps.
Does not poll secrets, invent a video id, dispatch, or write files.
Reusable once the first video is published.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def find_video_id(packet: Path) -> str | None:
    state = packet / "upload_state.json"
    if not state.is_file():
        return None
    try:
        data = json.loads(state.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    vid = data.get("provider_video_id") or data.get("video_id")
    if isinstance(vid, str) and vid.strip() and vid != "not_set":
        return vid.strip()
    return None


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    vid = find_video_id(packet)

    print("NEXT AFTER PUBLISH (fail-closed; no invent, no poll)")
    print(f"packet: {packet.name}")
    if vid:
        print(f"provider_video_id: {vid} (privacy must stay private)")
        print()
        print("Observation window: wait at least 10 days (7 calendar + 3 Analytics lag) after uploaded_at before collect.")
        print("Then dispatch once:")
        print("  gh workflow dispatch youtube-production.yml \\")
        print("    --repo takenthatusernameis-collab/Content-Automation \\")
        print("    -f execute=false -f collect_feedback=true")
        print()
        print("After metrics exist: run tools/experiment_loop.py (compare against baseline).")
        print("Do not invent metrics. Do not re-upload the master.")
    else:
        print("NO provider_video_id yet. Videos published stay 0.")
        print("Complete the human OAuth step first:")
        print("  python3 tools/human_one_pager.py")
        print("  or docs/human_oauth_checklist.md")
        print("Then confirm the id appears in upload_state.json before any collect.")
    print()
    print("NEXT AFTER PUBLISH PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
