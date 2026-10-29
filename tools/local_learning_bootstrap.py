#!/usr/bin/env python3
"""One-command local learning bootstrap for experiment skeletons.

Runs the key grounded experiment starters in sequence to produce
experiment_baseline.json, experiment_decision.json, and related notes
from idea.md and existing packet state only. Reduces recurring labor of
invoking separate tools and confirming outputs for every future packet
once a video is published and metrics arrive. No invented content,
metrics, decisions, or baselines. Outputs stay local. Aligns with
fail-closed experiment rules and no-invent rule.

Does not edit packet content, poll secrets, dispatch, or invent data.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent


def run_starter(script: str, packet: Path, force: bool, extra_args: list[str] | None = None) -> tuple[int, str]:
    """Run one starter tool and return (code, output)."""
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), str(packet)]
    if extra_args:
        cmd.extend(extra_args)
    if force:
        # Most starters use --write; force implies we want the file
        if "--write" not in cmd:
            cmd.append("--write")
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
        description="Bootstrap local experiment skeletons from idea.md (baseline + decision + notes; no invent)"
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--force", action="store_true", help="Write/overwrite skeleton files")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("FAIL: idea.md missing (required for grounded skeletons)", file=sys.stderr)
        return 2

    print("LOCAL LEARNING BOOTSTRAP (one command; grounded in idea.md + packet state; no invent)")
    print(f"Packet: {packet}")
    print()

    # Starters that produce fillable skeletons without inventing numbers or decisions
    starters = [
        ("experiment_baseline_starter.py", ["--write"] if args.force else []),
        ("experiment_decision_starter.py", ["--write"] if args.force else []),
        ("experiment_notes_starter.py", ["--write"] if args.force else []),
    ]

    results = []
    all_ok = True
    for script, extra in starters:
        code, out = run_starter(script, packet, args.force, extra)
        status = "OK" if code == 0 else "FAIL"
        if code != 0:
            all_ok = False
        results.append((script, status, code, out[:200]))
        print(f"{status} {script} (exit {code})")
        if out and code != 0:
            print(f"  {out[:300]}")

    print()
    if all_ok:
        print("READY: learning skeletons available (baseline null, decision pending).")
        print("Next (after publish + metrics): edit the skeletons with real documented values, then experiment_loop.py.")
        return 0
    else:
        print("GAP: one or more starters failed. Check output above.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
