#!/usr/bin/env python3
"""Local pre-dispatch confirmation for a packet.

Checks mechanical readiness for the OAuth + execute=true step without
polling secrets, inventing media, or writing packet content.
Prints a concise READY or lists gaps.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_check(cmd: list[str]) -> tuple[int, str]:
    try:
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as exc:  # noqa: BLE001
        return 1, str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path, help="Packet directory")
    args = parser.parse_args()
    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: packet directory missing: {packet}")
        return 2

    slug = packet.name
    print(f"pre-dispatch confirm: {slug}")
    gaps: list[str] = []

    # media_qa
    code, out = run_check(["python3", "tools/media_qa.py", str(packet)])
    if code != 0 or "gate: PASS" not in out:
        gaps.append("media_qa did not PASS")
    else:
        print("- PASS media_qa")

    # export present
    export = packet / "export" / "master.mp4"
    if not export.is_file():
        gaps.append("export/master.mp4 missing")
    else:
        print("- PASS export/master.mp4 present")

    # captions.srt
    srt = packet / "captions.srt"
    if not srt.is_file() or srt.stat().st_size < 100:
        gaps.append("captions.srt missing or too small")
    else:
        print("- PASS captions.srt present")

    # publish.md basic presence
    publish = packet / "publish.md"
    if not publish.is_file():
        gaps.append("publish.md missing")
    else:
        text = publish.read_text(encoding="utf-8", errors="replace")
        if "Title to upload" not in text and "title:" not in text.lower():
            gaps.append("publish.md lacks title marker")
        else:
            print("- PASS publish.md present")

    # vo present
    vo_candidates = list((packet / "vo").glob("*-take-selected.wav")) if (packet / "vo").is_dir() else []
    if not vo_candidates:
        gaps.append("selected VO missing")
    else:
        print("- PASS selected VO present")

    print()
    if gaps:
        print("NOT READY FOR DISPATCH")
        for g in gaps:
            print(f"- GAP: {g}")
        print("Fix local gaps before setting secrets and dispatching.")
        return 1
    else:
        print("READY FOR OAUTH + DISPATCH")
        print("Local mechanical gates passed. Proceed with:")
        print("  docs/human_oauth_checklist.md quick sequence")
        print("  or python3 tools/operator_card.py")
        print("Then the three secrets and one execute=true dispatch.")
        print("Do not invent a video id. Privacy stays private.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
