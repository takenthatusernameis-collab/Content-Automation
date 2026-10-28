#!/usr/bin/env python3
"""Generate all local text drafts for a packet in one command.

Runs the existing deterministic draft generators (chapters, description,
metadata pack, publish.md draft, visual plan) and reports which succeeded.
No invented content. Outputs stay local and gitignored.

Reduces recurring human labor of remembering and invoking each draft tool
separately on every future packet. One command produces the full set of
paste-ready drafts.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

DRAFTS = [
    ("chapters", "tools/chapters_from_script.py"),
    ("description", "tools/full_description_draft.py"),
    ("metadata", "tools/metadata_pack.py"),
    ("publish", "tools/publish_md_draft.py"),
    ("visual_plan", "tools/visual_plan_draft.py"),
]


def run_one(script: Path, packet: Path, force: bool) -> tuple[bool, str]:
    cmd = [sys.executable, str(script), str(packet)]
    if force:
        cmd.append("--force")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=20,
        )
        ok = result.returncode == 0
        out = (result.stdout or result.stderr or "").strip()
        msg = out.splitlines()[-1] if out else ("ok" if ok else "failed")
        return ok, msg
    except Exception as e:
        return False, str(e)


def main() -> int:
    p = argparse.ArgumentParser(description="Generate all local text drafts for a packet")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    p.add_argument("--force", action="store_true", help="Pass --force to each draft tool")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    repo_root = Path(__file__).resolve().parent.parent
    print(f"packet: {packet.name}")
    print("generating drafts...")

    results = []
    for name, rel in DRAFTS:
        script = repo_root / rel
        if not script.is_file():
            results.append((name, False, "script missing"))
            continue
        ok, msg = run_one(script, packet, args.force)
        results.append((name, ok, msg))
        status = "OK" if ok else "FAIL"
        print(f"  {status:4} {name:16} {msg}")

    ok_count = sum(1 for _, ok, _ in results if ok)
    print(f"\n{ok_count}/{len(results)} drafts generated (text files gitignored)")
    return 0 if ok_count > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
