#!/usr/bin/env python3
"""Generate a short local verification checklist for the installed default.

Extracts mechanism/problem from idea.md and emits concrete same-day checks
the viewer can use to confirm the default is in place. No invented content.
Output stays local (gitignored). Reduces recurring human labor of writing
verification language for every future packet while staying operational.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract as idea_extract  # noqa: E402


def build_checks(mech: str, problem: str) -> list[str]:
    """Return 3-4 operational verification checks grounded in extracted fields only."""
    checks: list[str] = []
    if mech:
        checks.append(f"The written default is visible where the stall starts: {mech}.")
    if problem:
        checks.append(f"The stall named in the idea ({problem}) no longer requires reopening the whole list.")
    checks.append("The first concrete action of the default was completed in the same session.")
    if mech or problem:
        checks.append("When the stall returns, the default is pointed at instead of a new decision.")
    return checks[:4]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local install_verifier.md from idea.md")
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("FAIL: idea.md missing", file=sys.stderr)
        return 2

    out_path = packet / "install_verifier.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    checks = build_checks(mech, problem)

    lines = [
        "# Install Verifier (local)",
        "",
        "Generated locally from idea.md mechanism/problem only.",
        "Short checklist the viewer (or producer) can use to confirm the default is installed the same day.",
        "Channel promise: one small default the viewer can install and verify the same day.",
        "Not a rewrite. Review and paste relevant lines into the description or end-screen if useful.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        "## Verification checks",
        "",
    ]
    for i, check in enumerate(checks, 1):
        lines.append(f"{i}. {check}")
    lines.extend([
        "",
        "---",
        "Use only the checks that match the actual install. Do not invent additional defaults or locations.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"checks: {len(checks)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print("Install verifier ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
