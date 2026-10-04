#!/usr/bin/env python3
"""Print the one Studio step the Data API cannot finish.

commentThreads.insert posts a comment. It does not pin it. After a provider
video id exists, the operator still opens Studio and pins that comment.
This printer does not call YouTube. It does not invent a video id. It does
not claim the comment is pinned.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def pin_text(packet: Path) -> str:
    publish = packet / "publish.md"
    if not publish.is_file():
        return ""
    text = publish.read_text(encoding="utf-8")
    marker = "First comment (pin candidate)"
    if marker not in text:
        return ""
    body = text.split(marker, 1)[1]
    # Section ends at the next markdown heading.
    lines = []
    for line in body.splitlines():
        if line.startswith("#") and lines:
            break
        lines.append(line)
    return "\n".join(lines).strip()


def render(state: dict, comment: str = "") -> str:
    video_id = str(state.get("provider_video_id") or "").strip()
    posted = state.get("comment_post") or {}
    status = str(posted.get("status") or "not_attempted")
    if not video_id:
        return "\n".join(
            [
                "STUDIO_PIN",
                "status: no_video_id",
                "pinned: false",
                "pin_note: commentThreads.insert does not pin; no provider video id yet",
            ]
        )
    lines = [
        "STUDIO_PIN",
        "status: needs_studio_pin",
        f"video_id: {video_id}",
        f"url: https://studio.youtube.com/video/{video_id}/comments",
        f"comment_post: {status}",
        "pinned: false",
        "pin_note: commentThreads.insert does not pin; Studio pin stays the remaining human step",
    ]
    if comment:
        lines.append("comment:")
        lines.append(comment)
    else:
        lines.append("comment: missing")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: studio_handoff.py PACKET", file=sys.stderr)
        return 2
    packet = Path(argv[1])
    state_path = packet / "upload_state.json"
    if not state_path.is_file():
        print("STUDIO_PIN")
        print("status: no_upload_state")
        print("pinned: false")
        return 0
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("STUDIO_PIN", file=sys.stderr)
        print("status: upload_state_unreadable", file=sys.stderr)
        return 2
    if not isinstance(state, dict):
        print("status: upload_state_unreadable", file=sys.stderr)
        return 2
    print(render(state, pin_text(packet)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
