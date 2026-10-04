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


PIN_NAME = "studio_pin.md"


def pin_markdown(state: dict, comment: str = "") -> str | None:
    """Durable Studio note. None when there is no provider video id.

    Does not invent an id. Does not claim the comment is pinned.
    """
    video_id = str(state.get("provider_video_id") or "").strip()
    if not video_id:
        return None
    posted = state.get("comment_post") or {}
    status = str(posted.get("status") or "not_attempted")
    lines = [
        "# Studio pin",
        "",
        "pinned: false",
        "end_screen: not_set",
        "",
        "commentThreads.insert does not pin. This file is not a pin.",
        "The Data API does not set an end screen. This file is not an end screen.",
        "",
        f"video_id: {video_id}",
        f"url: https://studio.youtube.com/video/{video_id}/comments",
        f"editor_url: https://studio.youtube.com/video/{video_id}/edit",
        f"comment_post: {status}",
        "",
        "## End screen",
        "",
        "The master already reserves the last 20 seconds. Do not re-encode.",
        "In the editor, add an end screen on that reserve only.",
        "Lower-left: one video or playlist element. Lower-right: subscribe.",
        "Leave the CTA card text readable. Do not cover the center.",
        "",
    ]
    if comment:
        lines.extend(["## Comment to pin", "", comment, ""])
    else:
        lines.extend(["comment: missing", ""])
    return "\n".join(lines)


def write_pin(packet: Path, state: dict, comment: str = "") -> str:
    body = pin_markdown(state, comment)
    path = packet / PIN_NAME
    if body is None:
        return "not_written"
    path.write_text(body, encoding="utf-8")
    return "written"


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
                "end_screen: not_set",
                "end_screen_note: no provider video id; do not invent an editor URL",
            ]
        )
    lines = [
        "STUDIO_PIN",
        "status: needs_studio_pin",
        f"video_id: {video_id}",
        f"url: https://studio.youtube.com/video/{video_id}/comments",
        f"comment_post: {status}",
        "pinned: false",
        "end_screen: not_set",
        "editor_url: https://studio.youtube.com/video/{video_id}/edit".format(video_id=video_id),
        "pin_note: commentThreads.insert does not pin; Studio pin stays a remaining human step",
        "end_screen_note: Data API does not set an end screen; last 20s reserve, lower-left video or playlist, lower-right subscribe",
    ]
    if comment:
        lines.append("comment:")
        lines.append(comment)
    else:
        lines.append("comment: missing")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    write = "--write" in argv[1:]
    args = [a for a in argv[1:] if a != "--write"]
    if len(args) != 1:
        print("usage: studio_handoff.py PACKET [--write]", file=sys.stderr)
        return 2
    packet = Path(args[0])
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
    comment = pin_text(packet)
    print(render(state, comment))
    if write:
        outcome = write_pin(packet, state, comment)
        print(f"pin_file: {outcome}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
