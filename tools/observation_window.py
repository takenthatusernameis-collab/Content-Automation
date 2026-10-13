#!/usr/bin/env python3
"""Compute the observation window due date for a packet after private upload.

Reads upload_state.json if present. Does not invent dates, metrics, or video ids.
Does not poll secrets, dispatch, or write files.
Useful after the first successful execute=true so agents and humans see whether
the +10 day window (7 calendar days + 3 days Analytics lag) is due without
recalculating or opening the checklist.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_uploaded_at(data: dict) -> datetime | None:
    raw = data.get("uploaded_at") or data.get("uploadedAt") or data.get("upload_time")
    if not raw or not isinstance(raw, str):
        return None
    # Accept ISO-ish strings
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(raw.replace("Z", "+0000") if "Z" in raw and fmt.endswith("%z") else raw, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 tools/observation_window.py PATH/TO/PACKET", file=sys.stderr)
        return 2
    packet = Path(sys.argv[1]).resolve()
    state_path = packet / "upload_state.json"
    if not state_path.is_file():
        print("OBSERVATION_WINDOW: not_uploaded (upload_state.json absent; expected until first successful private execute)")
        return 0
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"OBSERVATION_WINDOW: unreadable ({type(e).__name__})")
        return 1
    vid = str(data.get("provider_video_id") or "").strip()
    if not vid:
        print("OBSERVATION_WINDOW: file_exists_but_no_provider_video_id (do not invent)")
        return 0
    uploaded = parse_uploaded_at(data)
    if not uploaded:
        print(f"OBSERVATION_WINDOW: video_id={vid} but no parseable uploaded_at (do not invent dates)")
        return 0
    due = uploaded + timedelta(days=10)
    now = datetime.now(timezone.utc)
    status = "DUE" if now >= due else "WAITING"
    delta = (due - now).days
    print(f"OBSERVATION_WINDOW: {status} video_id={vid} uploaded_at={uploaded.isoformat()} due_at={due.isoformat()} (days_until={delta if delta > 0 else 0})")
    print("early collect_feedback returns OBSERVATION_WINDOW_NOT_DUE; do not dispatch collect until due")
    return 0


if __name__ == "__main__":
    sys.exit(main())
