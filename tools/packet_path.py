#!/usr/bin/env python3
"""Fail closed on a production packet path before media or upload work.

The workflow dispatch input is a string. A typo, a template, or a folder
that has not been scaffolded must not reach materialize or youtube_upload.
This tool does not create a packet and does not write state.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Q1 = "videos/002-stop-deciding-what-to-work-on-every-morning"
REFUSED_SLUGS = {".", "..", "_template"}


def normalize(raw: str) -> str:
    return raw.strip().replace("\\", "/").rstrip("/")


def refuse_reason(packet: str, *, root: Path = ROOT) -> str | None:
    if not packet:
        return "empty"
    if packet != Q1:
        parts = packet.split("/")
        if (
            len(parts) != 2
            or parts[0] != "videos"
            or not parts[1]
            or parts[1] in REFUSED_SLUGS
            or ".." in parts[1]
            or parts[1].startswith(".")
        ):
            return "outside_videos"
    folder = root / packet
    if not folder.is_dir():
        return "missing_folder"
    return None


def main() -> int:
    packet = normalize(os.environ.get("PACKET", ""))
    reason = refuse_reason(packet)
    if reason:
        print(f"REFUSE: packet {reason} {packet!r}", file=sys.stderr)
        return 2
    print(f"PACKET {packet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
