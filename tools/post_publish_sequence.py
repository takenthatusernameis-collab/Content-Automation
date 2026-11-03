#!/usr/bin/env python3
"""Print the ordered post-publish sequence once a private provider_video_id exists.

Fail-closed single-command reminder of:
- 7-day observation window
- collect_feedback dispatch
- experiment_baseline completeness check
- experiment_loop
- Studio pin + end screen (Data API cannot finish)
- optional playlist membership confirmation
Does not poll secrets, invent a video id or metrics, dispatch, or write files.
Reusable for future packets after the first publish.
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


def is_placeholder_source(source: str) -> bool:
    low = source.lower()
    bad = ("template", "replace", "invented", "placeholder", "guess", "assumed", "todo")
    return any(b in low for b in bad) or not source.strip()


def check_baseline(data: dict) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, "not a dict"
    baseline = data.get("baseline")
    source = str(data.get("source", ""))
    if baseline is None or not isinstance(baseline, (int, float)):
        return False, "baseline is null or non-numeric"
    if is_placeholder_source(source):
        return False, "source is placeholder or empty"
    hyp = str(data.get("hypothesis", "")).strip()
    if not hyp or "TEMPLATE" in hyp.upper():
        return False, "hypothesis missing or template"
    return True, "filled"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    vid = find_video_id(packet)

    print("POST PUBLISH SEQUENCE (fail-closed; no invent, no poll)")
    print(f"packet: {packet.name}")

    if not vid:
        print("NO provider_video_id yet. Videos published stay 0.")
        print("Complete the human OAuth step first:")
        print("  python3 tools/human_one_pager.py")
        print("  or docs/human_oauth_checklist.md")
        print("Then confirm the id appears in upload_state.json.")
        print("POST PUBLISH SEQUENCE HOLD (no id)")
        return 0

    print(f"provider_video_id: {vid} (privacy must stay private)")
    print()
    print("1. Observation window: wait at least 7 days after uploaded_at before collect.")
    print("   Then dispatch once:")
    print("   gh workflow dispatch youtube-production.yml \\")
    print("     --repo takenthatusernameis-collab/Content-Automation \\")
    print("     -f execute=false -f collect_feedback=true")
    print()
    print("2. After metrics exist, check experiment baseline:")
    baseline_path = packet / "experiment_baseline.json"
    if not baseline_path.is_file():
        print("   experiment_baseline.json: ABSENT")
        print("   Next: python3 tools/experiment_baseline_starter.py", packet)
        print("   Then edit numeric baseline + documented source. Do not invent.")
    else:
        try:
            data = json.loads(baseline_path.read_text(encoding="utf-8"))
            ok, reason = check_baseline(data)
            if ok:
                print("   experiment_baseline.json: FILLED")
            else:
                print(f"   experiment_baseline.json: PRESENT but incomplete ({reason})")
                print("   Next: edit with real numeric baseline and documented source.")
        except (OSError, json.JSONDecodeError):
            print("   experiment_baseline.json: INVALID")
    print()
    print("3. Once baseline is filled and metrics collected:")
    print("   python3 tools/experiment_loop.py", packet)
    print()
    print("4. Studio pin and end screen (Data API cannot finish these):")
    print("   python3 tools/studio_handoff.py", packet)
    print("   Open the printed Studio comments URL and pin the first comment.")
    print("   In the editor URL, set end screen on the reserved last 20 seconds only.")
    print("   Do not re-encode the master. Do not cover the center CTA card.")
    print()
    print("5. Playlist membership (optional; does not block publish):")
    print("   python3 tools/playlist_membership.py", packet)
    print("   If docs/channel.md playlist_id is set, the workflow already attempted insert.")
    print("   Confirm in Studio if the video is not yet in the playlist. Do not invent a PL id.")
    print()
    print("Do not invent metrics. Do not re-upload the master.")
    print("POST PUBLISH SEQUENCE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
