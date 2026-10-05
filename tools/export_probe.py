#!/usr/bin/env python3
"""Fail-closed stream probe for packet export/master.mp4.

Runs only when a master file is already present. Does not encode, does not
invent a file, and does not call YouTube. An ftyp box is not enough: width,
height, audio, and end-screen duration must match the format lock.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT_REL = Path("export") / "master.mp4"
TARGET_W = 1920
TARGET_H = 1080
MIN_DURATION = 20.0  # VO plus the locked 20s end screen


def probe_file(path: Path, min_duration: float = MIN_DURATION) -> dict:
    if not path.is_file():
        return {"ok": False, "code": "EXPORT_ABSENT", "detail": str(path)}
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return {"ok": False, "code": "FFPROBE_ABSENT", "detail": "ffprobe not on PATH"}
    proc = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return {
            "ok": False,
            "code": "PROBE_FAILED",
            "detail": (proc.stderr or "ffprobe failed")[-300:],
        }
    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        return {"ok": False, "code": "PROBE_FAILED", "detail": "ffprobe json unreadable"}
    streams = data.get("streams") or []
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    fmt = data.get("format") or {}
    try:
        duration = float(fmt.get("duration") or 0)
    except (TypeError, ValueError):
        duration = 0.0
    problems = []
    if video is None:
        problems.append("no video stream")
    else:
        width = int(video.get("width") or 0)
        height = int(video.get("height") or 0)
        if (width, height) != (TARGET_W, TARGET_H):
            problems.append(f"geometry {width}x{height}")
        codec = video.get("codec_name") or ""
        if codec != "h264":
            problems.append(f"video codec {codec or 'missing'}")
    if audio is None:
        problems.append("no audio stream")
    if duration + 0.05 < min_duration:
        problems.append(f"duration {duration:.2f}s < {min_duration:.0f}s")
    detail = (
        f"{TARGET_W}x{TARGET_H} h264 audio duration={duration:.2f}s"
        if not problems
        else "; ".join(problems)
    )
    return {
        "ok": not problems,
        "code": "PASS" if not problems else "EXPORT_STREAM_MISMATCH",
        "detail": detail,
        "duration": duration,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: export_probe.py PACKET", file=sys.stderr)
        return 2
    packet = Path(argv[1])
    if not packet.is_absolute():
        packet = ROOT / packet
    report = probe_file(packet / EXPORT_REL)
    print(f"{report['code']} {report['detail']}")
    if report["code"] == "PASS":
        return 0
    if report["code"] in {"EXPORT_ABSENT", "FFPROBE_ABSENT"}:
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
