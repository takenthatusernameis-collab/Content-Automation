#!/usr/bin/env python3
"""One-command text QA report for a packet draft or script.

Aggregates spoken-word band (via words.py), anti-slop hits (quality_scan),
claim hedges (claim_scan), mechanism-term presence (mechanism_align_scan),
and originality signals (originality_report).
Prints a concise summary so agents can check text health before apply or promotion
without sequential tool calls. Does not write files. Does not invent data.
Default exit 0; --strict exits 1 if any scan signals an issue.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

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
    parser = argparse.ArgumentParser(description="Aggregate core text QA scans for a packet.")
    parser.add_argument("packet", help="Packet folder containing idea.md / draft.md or script.md")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any underlying scan reports an issue.")
    args = parser.parse_args()
    packet = args.packet
    if not (Path(packet) / "idea.md").is_file():
        print(f"No idea.md in {packet}")
        return 1

    print("TEXT QA REPORT (band + quality + claim + mechanism align + originality; read-only)")
    print("Signals are revision prompts, not hard failures unless --strict.")
    print("=" * 64)

    issues = 0

    # Word band
    rc, out = run_tool("words.py", packet)
    print("\n## WORD BAND")
    print(out)
    if "BELOW" in out or "ABOVE" in out or "EMPTY" in out:
        issues += 1

    # Quality
    rc, out = run_tool("quality_scan.py", packet)
    print("\n## QUALITY SCAN")
    print(out)
    if "hits" in out.lower() and "clear" not in out.lower():
        issues += 1

    # Claims
    rc, out = run_tool("claim_scan.py", packet)
    print("\n## CLAIM SCAN")
    print(out)
    if "hits" in out.lower() and "clear" not in out.lower():
        issues += 1

    # Mechanism align
    rc, out = run_tool("mechanism_align_scan.py", packet)
    print("\n## MECHANISM ALIGN")
    print(out)
    if "missing:" in out.lower() and "none" not in out.lower().split("missing:")[-1]:
        issues += 1

    # Originality
    rc, out = run_tool("originality_report.py", packet)
    print("\n## ORIGINALITY REPORT")
    print(out)
    low = out.lower()
    if any(sig in low for sig in ("signal: weak", "signal: check", "signal: review")):
        issues += 1

    print("\n" + "=" * 64)
    print(f"summary_issues_detected: {issues}")
    print("Next: revise draft.md or script.md for any signals, then re-run this report.")
    print("draft.md is not script.md until apply_script.py --write.")
    if args.strict and issues:
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
