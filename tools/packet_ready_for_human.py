#!/usr/bin/env python3
"""One-command local packet readiness for the human OAuth step.

Orchestrates the key local gates (Selected VO presence, media_qa, pre_dispatch_confirm,
export_probe when master exists) and prints a clear READY FOR HUMAN OAUTH or GAP list.
Also reprints the exact next human commands so no rediscovery is required.
Reduces sequential checking labor for every future packet. No secrets polled,
no dispatch, no packet content edits, no media invented or committed.
Fail-closed on missing packet or missing idea.md.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent

SELECTED_VO_GLOB = "*-take-selected.wav"


def run_tool(script: str, packet: Path, extra: list[str] | None = None) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), str(packet)]
    if extra:
        cmd.extend(extra)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip()
    except Exception as e:
        return 1, f"EXCEPTION {script}: {e}"


def selected_vo_present(packet: Path) -> bool:
    vo_dir = packet / "vo"
    if not vo_dir.is_dir():
        return False
    return any(vo_dir.glob(SELECTED_VO_GLOB))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="One-command local readiness check before human OAuth + dispatch (no invent, no secrets)"
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: not a directory: {packet}", file=sys.stderr)
        return 1

    idea = packet / "idea.md"
    if not idea.is_file():
        print("FAIL: idea.md missing", file=sys.stderr)
        return 2

    print("PACKET READY FOR HUMAN (one command; local gates only; no secrets, no invent)")
    print(f"Packet: {packet}")
    print()

    gaps = []

    # 1. Selected VO
    if selected_vo_present(packet):
        print("OK  Selected VO present")
    else:
        print("GAP Selected VO missing (run materialize_q1_release.py if Q1, or drop take)")
        gaps.append("selected_vo")

    # 2. media_qa
    code, out = run_tool("media_qa.py", packet)
    if code == 0 and "PASS" in out.upper():
        print("OK  media_qa PASS")
    else:
        print(f"GAP media_qa (exit {code})")
        if out:
            print(f"  {out[:250]}")
        gaps.append("media_qa")

    # 3. pre_dispatch_confirm
    code, out = run_tool("pre_dispatch_confirm.py", packet)
    if code == 0 and "READY" in out.upper():
        print("OK  pre_dispatch_confirm READY")
    else:
        print(f"GAP pre_dispatch_confirm (exit {code})")
        if out:
            print(f"  {out[:250]}")
        gaps.append("pre_dispatch")

    # 4. export_probe if master exists
    master = packet / "export" / "master.mp4"
    if master.is_file():
        code, out = run_tool("export_probe.py", packet)
        if code == 0:
            print("OK  export_probe PASS")
        else:
            print(f"GAP export_probe (exit {code})")
            if out:
                print(f"  {out[:250]}")
            gaps.append("export_probe")
    else:
        print("NOTE export/master.mp4 absent (expected if not yet assembled; not a hard gap for readiness)")

    print()
    if not gaps:
        print("READY FOR HUMAN OAUTH + SINGLE DISPATCH")
        print()
        print("Exact next human steps (copy-paste):")
        print("  python3 tools/oauth_exchange.py")
        print("  python3 tools/oauth_exchange.py --exchange --out /tmp/youtube-refresh-token")
        print("  gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation")
        print("  gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation")
        print("  gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation")
        print("  gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false")
        print()
        print("Scopes must include youtube.upload + youtube.force-ssl + yt-analytics.readonly.")
        print("Do not dispatch again until a private video id appears. Privacy stays private.")
        return 0
    else:
        print(f"GAPS: {', '.join(gaps)}")
        print("Fix the gaps above before the human OAuth step. Do not invent media.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
