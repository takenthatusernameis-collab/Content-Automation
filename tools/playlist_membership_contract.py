#!/usr/bin/env python3
"""Lock playlist membership: do not invent an id, do not insert without one."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import playlist_membership as pm


def main() -> int:
    failures: list[str] = []
    if pm.channel_playlist_id("playlist_id: not_set\n") != "":
        failures.append("not_set invented a playlist id")
    if pm.channel_playlist_id("no playlist line\n") != "":
        failures.append("missing line invented a playlist id")
    if not pm.playlist_id_ok("PLabcdefghijkl"):
        failures.append("valid-shaped id rejected")
    if pm.playlist_id_ok("not_set") or pm.playlist_id_ok("UU123"):
        failures.append("unset or non-PL id accepted")
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp)
        (packet / "upload_state.json").write_text(
            json.dumps({"provider_video_id": "abc12345678"}),
            encoding="utf-8",
        )
        unset = pm.plan(packet, "")
        if unset["status"] != "not_set" or unset["request"] is not None:
            failures.append(f"unset plan wrote a request: {unset}")
        ready = pm.plan(packet, "PLabcdefghijkl")
        if ready["status"] != "ready" or ready["request"]["snippet"]["playlistId"] != "PLabcdefghijkl":
            failures.append(f"ready plan mismatch: {ready}")
        if ready["request"]["snippet"]["resourceId"]["videoId"] != "abc12345678":
            failures.append("ready plan dropped the video id")
        if pm.plan_markdown(unset) is not None:
            failures.append("unset plan wrote a markdown file body")
        empty = Path(tmp) / "empty"
        empty.mkdir()
        no_id = pm.plan(empty, "PLabcdefghijkl")
        if no_id["status"] != "no_video_id" or no_id["request"] is not None:
            failures.append(f"missing video id still built a request: {no_id}")
        bad = pm.plan(packet, "not-a-playlist")
        if bad["status"] != "invalid_playlist_id" or pm.exit_code(bad) != 2:
            failures.append(f"invalid playlist id must exit 2: {bad}")
        if pm.exit_code(unset) != 0 or pm.exit_code(no_id) != 0:
            failures.append("unset or missing video id must stay exit 0")
        failed = {
            "status": "not_added",
            "playlist_id": "PLabcdefghijkl",
            "provider_video_id": "abc12345678",
            "membership": "not_added",
            "detail": "PLAYLIST_INSERT_FAILED",
            "request": None,
        }
        if pm.exit_code(failed) != 2 or pm.plan_markdown(failed) is None:
            failures.append("failed insert must exit 2 and write a plan")
        if "videos.insert: not_called" not in (pm.plan_markdown(failed) or ""):
            failures.append("failed insert plan called videos.insert")
        auth = dict(failed, status="auth_required", detail="YOUTUBE_AUTH_REQUIRED")
        if pm.exit_code(auth) != 2:
            failures.append("auth_required must exit 2")
        present = dict(failed, status="already_present", membership="already_present", detail="")
        if pm.exit_code(present) != 0 or pm.plan_markdown(present) is None:
            failures.append("already_present must stay exit 0 and write a plan")
    text = (Path(__file__).resolve().parents[1] / "docs" / "channel.md").read_text(encoding="utf-8")
    if "playlist_id: not_set" not in text:
        failures.append("channel.md lost playlist_id: not_set")
    workflow = (Path(__file__).resolve().parents[1] / ".github" / "workflows" / "youtube-production.yml").read_text(encoding="utf-8")
    if "tools/playlist_membership.py" not in workflow:
        failures.append("workflow does not call playlist_membership.py")
    if failures:
        print("PLAYLIST MEMBERSHIP CONTRACT FAIL")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("PLAYLIST MEMBERSHIP CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
