#!/usr/bin/env python3
"""One-command metadata QA report for a packet.

Aggregates title_scan, description_scan, tags_scan, first_comment_scan,
chapters_scan, thumbnail_scan, and end_screen_scan. Prints a concise summary
so agents can check publish-phase metadata health before promotion without
sequential tool calls. Does not write files. Does not invent data.
Default exit 0; --strict exits 1 if any scan signals an issue.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

SCANNERS = [
    ("title_scan.py", "TITLE SCAN"),
    ("description_scan.py", "DESCRIPTION SCAN"),
    ("tags_scan.py", "TAGS SCAN"),
    ("first_comment_scan.py", "FIRST COMMENT SCAN"),
    ("chapters_scan.py", "CHAPTERS SCAN"),
    ("thumbnail_scan.py", "THUMBNAIL SCAN"),
    ("end_screen_scan.py", "END SCREEN SCAN"),
]


def run_tool(script: str, packet: str, extra: list[str] | None = None) -> tuple[int, str]:
    """Run a tool and return (returncode, stdout+stderr)."""
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), packet]
    if extra:
        cmd.extend(extra)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip()
    except Exception as e:
        return 1, f"EXCEPTION {script}: {e}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate core metadata QA scans for a packet.")
    parser.add_argument("packet", help="Packet folder containing publish.md / titles.md / chapters.md / etc.")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any underlying scan reports an issue.")
    args = parser.parse_args()
    packet = args.packet
    if not (Path(packet) / "idea.md").is_file():
        print(f"No idea.md in {packet}")
        return 1

    print("METADATA QA REPORT (title + description + tags + first-comment + chapters + thumbnail + end-screen; read-only)")
    print("Signals are revision prompts, not hard failures unless --strict.")
    print("=" * 72)

    issues = 0

    for script, header in SCANNERS:
        rc, out = run_tool(script, packet)
        print(f"\n## {header}")
        print(out or "(no output)")
        # Detect issue signals: most scanners print "clear" when clean; non-clear or hits indicate revision.
        low = out.lower()
        if "clear" not in low and out and "missing" not in low:
            issues += 1
        elif "hits" in low or "weak" in low or "shout" in low or "malformed" in low:
            issues += 1

    print("\n" + "=" * 72)
    print(f"summary_issues_detected: {issues}")
    print("Next: revise the corresponding publish.md / titles.md / chapters.md sections for any signals, then re-run this report.")
    print("Metadata is not locked until the relevant scans pass and apply or promotion steps complete.")
    if args.strict and issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
