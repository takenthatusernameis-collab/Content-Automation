#!/usr/bin/env python3
"""Plan or add a published video to the channel playlist.

Dry-run is the default. A missing or not_set playlist id does not invent a
PL id and does not fail the upload. A missing provider video id does not
invent one. This tool does not call videos.insert.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANNEL = ROOT / "docs" / "channel.md"
UNSET = {"", "not_set", "none", "unset", "null"}


def channel_playlist_id(text: str | None = None) -> str:
    """Return the locked playlist id, or empty when the line is unset."""
    raw = text if text is not None else (CHANNEL.read_text(encoding="utf-8") if CHANNEL.is_file() else "")
    for line in raw.splitlines():
        if line.startswith("playlist_id:"):
            value = line.split(":", 1)[1].strip()
            if value.lower() in UNSET:
                return ""
            return value
    return ""


def playlist_id_ok(value: str) -> bool:
    if not value.startswith("PL") or len(value) < 13 or len(value) > 80:
        return False
    return all(ch.isalnum() or ch in "_-" for ch in value)


def video_id_from_state(packet: Path) -> str:
    path = packet / "upload_state.json"
    if not path.is_file():
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ""
    if not isinstance(data, dict):
        return ""
    return str(data.get("provider_video_id") or "").strip()


def insert_body(playlist_id: str, video_id: str) -> dict:
    return {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {"kind": "youtube#video", "videoId": video_id},
        }
    }


def plan(packet: Path, playlist_id: str | None = None) -> dict:
    chosen = channel_playlist_id() if playlist_id is None else playlist_id
    video_id = video_id_from_state(packet)
    if not chosen:
        return {
            "status": "not_set",
            "playlist_id": "",
            "provider_video_id": video_id,
            "membership": "not_added",
            "request": None,
        }
    if not playlist_id_ok(chosen):
        return {
            "status": "invalid_playlist_id",
            "playlist_id": chosen,
            "provider_video_id": video_id,
            "membership": "not_added",
            "request": None,
        }
    if not video_id:
        return {
            "status": "no_video_id",
            "playlist_id": chosen,
            "provider_video_id": "",
            "membership": "not_added",
            "request": None,
        }
    return {
        "status": "ready",
        "playlist_id": chosen,
        "provider_video_id": video_id,
        "membership": "not_added",
        "request": insert_body(chosen, video_id),
    }


def plan_markdown(row: dict) -> str | None:
    if row["status"] != "ready" and row["membership"] == "not_added":
        return None
    lines = [
        "# Playlist membership",
        "",
        f"playlist_id: {row['playlist_id']}",
        f"provider_video_id: {row['provider_video_id']}",
        f"membership: {row['membership']}",
        "videos.insert: not_called",
        "",
    ]
    return "\n".join(lines)


def render(row: dict) -> str:
    lines = [
        "PLAYLIST_MEMBERSHIP",
        f"status: {row['status']}",
        f"playlist_id: {row['playlist_id'] or 'not_set'}",
        f"provider_video_id: {row['provider_video_id'] or 'none'}",
        f"membership: {row['membership']}",
        "videos.insert: not_called",
    ]
    if row.get("request"):
        lines.append("request: playlistItems.insert")
        lines.append(json.dumps(row["request"], separators=(",", ":")))
    return "\n".join(lines)


def already_present(reason: str) -> bool:
    token = reason.lower()
    return "already" in token or "duplicate" in token


def execute(packet: Path, playlist_id: str | None = None) -> dict:
    row = plan(packet, playlist_id)
    if row["status"] != "ready":
        return row
    sys.path.insert(0, str(ROOT / "tools"))
    from youtube_api import YouTubeAPIError, api_json, refresh_access_token

    try:
        token = refresh_access_token()
    except YouTubeAPIError as exc:
        row["status"] = "auth_required" if exc.reason == "YOUTUBE_AUTH_REQUIRED" else "not_added"
        row["detail"] = exc.reason
        return row
    try:
        added = api_json(
            "POST",
            "/playlistItems",
            token=token,
            params={"part": "snippet"},
            body=row["request"],
        )
    except YouTubeAPIError as exc:
        if already_present(exc.reason) or already_present(exc.detail):
            row["status"] = "already_present"
            row["membership"] = "already_present"
            return row
        row["status"] = "not_added"
        row["detail"] = exc.reason
        return row
    item_id = str(added.get("id") or "").strip()
    row["status"] = "added" if item_id else "not_added"
    row["membership"] = "added" if item_id else "not_added"
    row["playlist_item_id"] = item_id
    return row


def write_plan(packet: Path, row: dict) -> Path | None:
    text = plan_markdown(row)
    if text is None:
        return None
    path = packet / "playlist_plan.md"
    path.write_text(text, encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    write = "--write" in args
    do_execute = "--execute" in args
    packet_arg = next((a for a in args if not a.startswith("--")), "")
    packet = Path(packet_arg) if packet_arg else ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
    if not packet.is_absolute():
        packet = ROOT / packet
    row = execute(packet) if do_execute else plan(packet)
    if write:
        write_plan(packet, row)
    print(render(row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
