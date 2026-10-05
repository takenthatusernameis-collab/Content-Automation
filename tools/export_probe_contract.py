#!/usr/bin/env python3
"""Lock the export stream probe. Does not touch Q1 media or YouTube."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from export_probe import probe_file  # noqa: E402


def encode(path: Path, size: str, seconds: float) -> None:
    proc = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c=black:s={size}:d={seconds}",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=48000:cl=stereo",
            "-shortest",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-t",
            str(seconds),
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"fixture encode failed: {proc.stderr[-400:]}")


def main() -> int:
    missing = probe_file(Path("/tmp/export-probe-missing-master.mp4"))
    if missing["code"] != "EXPORT_ABSENT":
        print(f"missing master must be EXPORT_ABSENT, got {missing}")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        good = Path(tmp) / "good.mp4"
        bad = Path(tmp) / "bad.mp4"
        encode(good, "1920x1080", 1.2)
        encode(bad, "320x240", 1.2)
        ok = probe_file(good, min_duration=1.0)
        if not ok["ok"]:
            print(f"good master must PASS, got {ok}")
            return 1
        short = probe_file(good, min_duration=20.0)
        if short["code"] != "EXPORT_STREAM_MISMATCH":
            print(f"short master must mismatch, got {short}")
            return 1
        geom = probe_file(bad, min_duration=1.0)
        if geom["ok"] or "geometry" not in geom["detail"]:
            print(f"small master must fail geometry, got {geom}")
            return 1
    print("EXPORT PROBE CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
