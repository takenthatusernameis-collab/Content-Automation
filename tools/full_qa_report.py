#!/usr/bin/env python3
"""One-command full QA report for a packet (text + metadata).

Aggregates text_qa_report.py (word band, quality, claims, mechanism align)
and metadata_qa_report.py (title, description, tags, first-comment, chapters,
thumbnail, end-screen). Prints a concise combined summary so agents can check
complete pre-promotion health without sequential tool calls.
Does not write files. Does not invent data.
Default exit 0; --strict exits 1 if any underlying report signals an issue.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

def run_report(script: str, packet: str) -> tuple[int, str]:
    """Run a QA report tool and return (returncode, output)."""
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    try:
        proc = subprocess.run(
            [sys.executable, str(path), packet],
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
        description="Aggregate text and metadata QA reports for a packet."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any underlying report detects issues.",
    )
    args = parser.parse_args()
    packet = args.packet
    if not (Path(packet) / "idea.md").is_file():
        print(f"No idea.md in {packet}")
        return 1

    print("FULL QA REPORT (text + metadata; read-only)")
    print("Signals are revision prompts, not hard failures unless --strict.")
    print("=" * 72)

    issues = 0

    # Text QA
    rc, out = run_report("text_qa_report.py", packet)
    print("\n## TEXT QA")
    print(out or "(no output)")
    if "summary_issues_detected:" in out:
        try:
            n = int(out.split("summary_issues_detected:")[-1].split()[0])
            issues += n
        except (ValueError, IndexError):
            if "issues" in out.lower() and "0" not in out.split("summary_issues_detected:")[-1]:
                issues += 1

    # Metadata QA
    rc, out = run_report("metadata_qa_report.py", packet)
    print("\n## METADATA QA")
    print(out or "(no output)")
    if "summary_issues_detected:" in out:
        try:
            n = int(out.split("summary_issues_detected:")[-1].split()[0])
            issues += n
        except (ValueError, IndexError):
            if "issues" in out.lower() and "0" not in out.split("summary_issues_detected:")[-1]:
                issues += 1

    print("\n" + "=" * 72)
    print(f"overall_summary_issues_detected: {issues}")
    print("Next: revise draft.md / publish.md / titles.md / chapters.md / assets.md for any signals,")
    print("then re-run this report. draft.md is not script.md until apply_script.py --write.")
    print("Metadata is not locked until the relevant scans pass.")
    if args.strict and issues:
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
