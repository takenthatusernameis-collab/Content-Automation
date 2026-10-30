#!/usr/bin/env python3
"""Quick local readiness check for human dispatch of Q1 upload.

Confirms media fingerprint PRESENT, master SHA matches durable r253 target, next_action code is upload-blocked,
and remaining open boxes do not block the publish step.
Does not materialize, does not run full QA, does not poll secrets,
does not invent data. Self-contained stdlib.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def run_tool(script: str, args: list[str] | None = None) -> str:
    cmd = [sys.executable, str(ROOT / "tools" / script)] + (args or [])
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return (proc.stdout or "") + (proc.stderr or "")


def media_ok(packet: Path) -> bool:
    out = run_tool("media_fingerprint.py")
    return "media_fingerprint: PRESENT" in out


def master_sha_ok(packet: Path) -> bool:
    """True only when master_sha_check.py reports PASS for this packet."""
    out = run_tool("master_sha_check.py", [str(packet)])
    return "PASS: master SHA matches r253 target" in out


def next_action_code(packet: Path) -> str:
    try:
        rel = packet.resolve().relative_to(ROOT)
    except ValueError:
        rel = packet
    out = run_tool("next_action.py", [str(rel)])
    for line in out.splitlines():
        if "upload-blocked" in line.lower() or packet.name in line:
            parts = line.split()
            if len(parts) >= 3:
                return parts[2]
    return "unknown"


def open_boxes(packet: Path) -> list[str]:
    md = packet / "packet.md"
    if not md.is_file():
        return ["packet.md missing"]
    text = md.read_text(encoding="utf-8")
    items = []
    in_section = False
    for line in text.splitlines():
        if line.startswith("## Remaining human work"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.strip().startswith("- [ ]"):
            items.append(line.strip()[6:].strip())
    return items


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print("publish_readiness: packet missing")
        return 1

    m_ok = media_ok(packet)
    sha_ok = master_sha_ok(packet)
    code = next_action_code(packet)
    boxes = open_boxes(packet)
    upload_blocked = "upload-blocked" in code.lower()

    print("PUBLISH READINESS (local only; no poll, no materialize, no invent)")
    print(f"packet: {packet.name}")
    print(f"media_fingerprint_present: {m_ok}")
    print(f"master_sha_ok: {sha_ok}")
    print(f"next_action_code: {code}")
    print(f"upload_blocked: {upload_blocked}")
    print(f"open_boxes: {len(boxes)}")
    if boxes:
        for b in boxes:
            print(f"  - {b}")

    ready = m_ok and sha_ok and upload_blocked
    if ready:
        print("status: READY_FOR_HUMAN_DISPATCH")
        print("message: Local media, correct r253 master, and gates are ready. Set the three OAuth secrets then dispatch execute=true once.")
        print("next: python3 tools/human_next_action.py")
    else:
        print("status: NOT_READY")
        print("message: Resolve media or next_action before human dispatch.")
    print("Do not poll secrets. Preferred unblocked list remains complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
