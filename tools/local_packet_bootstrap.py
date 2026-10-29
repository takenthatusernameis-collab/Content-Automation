#!/usr/bin/env python3
"""One-command local packet bootstrap from idea.md.

Runs the key grounded writers in sequence to produce draft_skeleton.md,
packet_starter.md, and early_assets.md from idea.md mechanism/problem/topic
only. Reduces recurring labor of invoking three separate tools and confirming
outputs for every future packet. No invented content. Outputs stay local
(gitignored). Aligns with channel voice (assignment, not reply prompt),
format (text-card first, structure rules), and existing individual tools.
Does not edit packet content, poll secrets, or scaffold new packets.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent


def run_writer(script: str, packet: Path, force: bool) -> tuple[int, str]:
    """Run one writer tool and return (code, output)."""
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), str(packet)]
    if force:
        cmd.append("--force")
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip()
    except Exception as e:
        return 1, f"EXCEPTION {script}: {e}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap local grounded starters (draft skeleton + packet starter + early assets) from idea.md"
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing starter files")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("FAIL: idea.md missing", file=sys.stderr)
        return 2

    print("LOCAL PACKET BOOTSTRAP (one command; grounded in idea.md only; no invent)")
    print(f"Packet: {packet}")
    print()

    writers = [
        ("draft_skeleton_writer.py", "draft_skeleton.md"),
        ("packet_starter_pack.py", "packet_starter.md"),
        ("early_assets_stub.py", "early_assets.md"),
    ]

    results = []
    overall = 0
    for script, expected in writers:
        code, out = run_writer(script, packet, args.force)
        status = "OK" if code == 0 else f"FAIL({code})"
        results.append((script, expected, status, out))
        if code != 0:
            overall = max(overall, code)
        print(f"{status}: {script} → {expected}")
        if out:
            for line in out.splitlines()[:4]:
                print(f"  {line}")
        print()

    print("--- Summary ---")
    for script, expected, status, _ in results:
        print(f"{status} {expected}")
    print()
    print("Starters ready (local; estimated from packet fields only).")
    print("Next: expand draft_skeleton.md WORDS to format targets, adapt packet_starter.md, then apply_script when signals clear.")
    print("Do not invent claims. Preferred unblocked path remains human OAuth step.")
    return overall


if __name__ == "__main__":
    raise SystemExit(main())
