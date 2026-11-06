#!/usr/bin/env python3
"""Soft check for a private provider_video_id after an execute=true dispatch.

Fail-closed: reports PRESENT only when a non-empty, non-placeholder id exists in
upload_state.json. Never invents an id, never polls secrets, never dispatches,
never writes files. Prints the exact next command when an id is found.
Reusable for future packets.
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
    if isinstance(vid, str):
        vid = vid.strip()
        if vid and vid not in ("not_set", "none", "null", ""):
            return vid
    return None


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    print("HUMAN SUCCESS CHECK (soft; no invent, no poll, no dispatch)")
    print(f"packet: {packet.name}")

    vid = find_video_id(packet)
    if not vid:
        print("provider_video_id: ABSENT")
        print("Videos published stay 0.")
        print("If you just dispatched execute=true, wait for the Actions run to finish,")
        print("then re-run this check. Look in the workflow log for a private video id.")
        print("Do not invent an id. Do not re-dispatch until an id is visible here and in the log.")
        print("HUMAN SUCCESS CHECK HOLD (no id yet)")
        return 0

    print(f"provider_video_id: PRESENT ({vid})")
    print("Privacy must remain private.")
    print("Next: python3 tools/post_publish_sequence.py")
    print("HUMAN SUCCESS CHECK PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
