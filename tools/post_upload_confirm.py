#!/usr/bin/env python3
"""Confirm post-upload signals from packet upload_state.json.

After a successful execute=true, agents and humans need a single command to
see whether the private provider video id is present, privacy is private, and
uploaded_at is parseable — without inventing ids or re-opening checklists.

Does not poll secrets, dispatch, write files, or invent data.
Reusable for every future packet once a private upload has occurred.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from upload_date import parse_uploaded_at as parse_uploaded_dt



def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 tools/post_upload_confirm.py PATH/TO/PACKET", file=sys.stderr)
        return 2
    packet = Path(sys.argv[1]).resolve()
    state_path = packet / "upload_state.json"
    if not state_path.is_file():
        print("POST_UPLOAD_CONFIRM: not_uploaded (upload_state.json absent; expected until first successful private execute)")
        print("Do not invent a provider_video_id. Do not re-dispatch execute until id is visible in Actions log AND this file.")
        return 0
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"POST_UPLOAD_CONFIRM: unreadable ({type(e).__name__})")
        return 1

    vid = str(data.get("provider_video_id") or "").strip()
    privacy = str(
        data.get("privacyStatus") or data.get("privacy_status") or data.get("privacy") or ""
    ).strip().lower()
    uploaded_dt = parse_uploaded_dt(data)
    uploaded = uploaded_dt.isoformat() if uploaded_dt else None

    missing = []
    if not vid:
        missing.append("provider_video_id")
    if privacy not in ("private", "unlisted"):  # private is required for first upload; unlisted is unusual but not invent
        if not privacy:
            missing.append("privacyStatus")
        # keep privacy value for report even if unexpected
    if not uploaded:
        missing.append("uploaded_at")

    if missing:
        print(
            f"POST_UPLOAD_CONFIRM: INCOMPLETE missing={','.join(missing)} "
            f"video_id={vid or 'none'} privacy={privacy or 'none'} uploaded_at={uploaded or 'none'}"
        )
        print("Do not invent missing fields. Confirm in Actions log. Do not re-dispatch execute until complete.")
        return 0

    print(
        f"POST_UPLOAD_CONFIRM: CONFIRMED video_id={vid} privacy={privacy} uploaded_at={uploaded}"
    )
    print(
        "Privacy must stay private until reviewed. Use observation_window.py for the +10d collect window. "
        "Do not re-dispatch execute."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
