#!/usr/bin/env python3
"""Quick local publish-readiness check for Q1 (or given packet).

Confirms media is present with matching master SHA, next_action is upload-blocked,
and lists any remaining open human-work boxes, without full QA, materialize, or
secret polling. Reduces rediscovery of "is the packet ready for the human dispatch?"
once OAuth secrets exist. Does not invent data, dispatch, or write files.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def run(script: str, args: list[str] | None = None) -> str:
    cmd = [sys.executable, str(ROOT / "tools" / script)] + (args or [])
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return (proc.stdout or "") + (proc.stderr or "")


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"publish_readiness: packet dir missing ({packet})")
        return 1
    rel = packet.relative_to(ROOT) if packet.is_relative_to(ROOT) else packet
    print("PUBLISH READINESS (local only; no invent, no poll, no dispatch)")
    print(f"packet: {rel}")
    print()

    # Media fingerprint
    fp = run("media_fingerprint.py")
    print("--- media ---")
    print(fp.strip())
    media_ok = "PRESENT" in fp and "MATCH" in fp

    # Next action code
    na = run("next_action.py", [str(rel)])
    code = "unknown"
    for line in na.splitlines():
        if packet.name in line or "ready_for_vo" in line:
            parts = line.split()
            if len(parts) >= 3:
                code = parts[2]
                break
    print("--- next_action ---")
    print(f"code: {code}")
    action_ok = code == "upload-blocked"

    # Open boxes from packet.md
    packet_md = packet / "packet.md"
    open_items = []
    if packet_md.is_file():
        text = packet_md.read_text(encoding="utf-8")
        in_section = False
        for line in text.splitlines():
            if line.startswith("## Remaining human work"):
                in_section = True
                continue
            if in_section and line.startswith("## "):
                break
            if in_section and line.strip().startswith("- [ ]"):
                open_items.append(line.strip()[6:].strip())
    print("--- remaining open boxes ---")
    if open_items:
        for item in open_items:
            print(f"  - [ ] {item}")
    else:
        print("  none (all checked or section absent)")

    print()
    ready = media_ok and action_ok
    if ready:
        print("READY_FOR_HUMAN_DISPATCH: media PRESENT+MATCH and next_action=upload-blocked.")
        print("Human step remains: set three secrets then one execute=true dispatch.")
        print("See: python3 tools/human_next_action.py")
    else:
        print("NOT_READY: fix media or next_action before expecting a successful dispatch.")
        if not media_ok:
            print("  Hint: python3 tools/materialize_q1_release.py (only if MISSING)")
        if not action_ok:
            print("  Hint: run media_qa / next_action for details (do not re-run solely for confirmation)")
    print("Do not poll secrets. Privacy stays private. Preferred list remains complete.")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
