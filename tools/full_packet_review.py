#!/usr/bin/env python3
"""One-command full packet review before the human OAuth step.

Aggregates the existing quality_prep_brief (script anti-slop, claims, cadence,
mechanism) and soft_pre_upload_report (title/tags/description length, thumbnail
size/bytes/format, VO duration, publish sections, end-screen reserve) into a
single summary. Surfaces revision signals and soft advisories so the human
needs fewer sequential commands. Does not change hard gates, invent text or
media, rewrite files, poll secrets, encode, or upload. Reduces rediscovery
labor for future packets. Reusable.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def run_tool(script: str, packet: Path) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), str(packet)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=60)
        out = ((proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")).strip()
        return proc.returncode, out
    except Exception as e:
        return 1, f"EXCEPTION {script}: {e}"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"full_packet_review: packet dir missing ({packet})")
        return 1

    print("FULL PACKET REVIEW (quality + soft pre-upload; gates unchanged)")
    print(f"packet: {packet.name}")
    print("Signals are advisory only. Hard gates live in media_qa / caption_gate / etc.")
    print("=" * 72)
    print()

    print("## QUALITY PREP BRIEF")
    print("-" * 40)
    _, qout = run_tool("quality_prep_brief.py", packet)
    print(qout or "(no output)")
    print()

    print("## SOFT PRE-UPLOAD REPORT")
    print("-" * 40)
    _, sout = run_tool("soft_pre_upload_report.py", packet)
    print(sout or "(no output)")
    print()

    print("=" * 72)
    print("Next: python3 tools/human_one_pager.py or docs/human_oauth_checklist.md")
    print("Do not poll secrets. Do not invent media. FULL PACKET REVIEW PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
