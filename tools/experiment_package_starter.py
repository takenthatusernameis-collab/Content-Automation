#!/usr/bin/env python3
"""One-command full experiment package starter for a packet.

Aggregates experiment_setup_report (metric/guardrail/hypothesis suggestions)
plus the three skeleton printers (baseline JSON, decision JSON, notes Markdown)
into a single concise view so agents can obtain the complete documentation
starting point without sequential tool calls.
Does not invent numeric baselines, results, or decisions. Does not write files
unless individual starters are called with --write separately. Does not call APIs.
Complements the individual tools without replacing them.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

def run_tool(script: str, packet: str, extra: list[str] | None = None) -> tuple[int, str]:
    """Run a tool and return (returncode, output)."""
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), packet]
    if extra:
        cmd.extend(extra)
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

def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the experiment package starter."""
    p = packet
    return [
        f"choose values: select one hypothesis, one primary_metric, and 3-5 guardrails from the SETUP SUGGESTIONS above",
        f"edit baseline: set a real numeric baseline and documented source in the BASELINE SKELETON, then python3 tools/experiment_baseline_starter.py {p} --write",
        f"notes skeleton: paste the NOTES SKELETON into experiment_notes.md and fill sections after real evidence",
        f"decision later: after publish + 10 day observation window (7 calendar + 3 Analytics lag) + collected metrics, edit the DECISION SKELETON then python3 tools/experiment_decision_starter.py {p} --write",
        f"full production if needed: python3 tools/full_production_starter.py {p}",
        f"quality scans: python3 tools/quality_scan.py {p} && python3 tools/claim_scan.py {p}",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate full experiment package starters and suggestions. No invented values."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    packet = args.packet
    path = Path(packet).resolve()
    if not path.is_dir() or not (path / "idea.md").is_file():
        print(f"No idea.md in {packet}", file=sys.stderr)
        return 1

    print("EXPERIMENT PACKAGE STARTER (suggestions + skeletons only; no invented baseline, result, or decision)")
    print("Use the suggestions to choose values, then edit the printed skeletons before writing.")
    print("=" * 72)

    # Setup suggestions first
    rc, out = run_tool("experiment_setup_report.py", packet)
    print("\n## SETUP SUGGESTIONS (metric / guardrail / hypothesis)")
    print(out or "(no output)")

    # Baseline skeleton
    rc, out = run_tool("experiment_baseline_starter.py", packet)
    print("\n## BASELINE SKELETON (JSON; edit numeric baseline + documented source)")
    print(out or "(no output)")

    # Decision skeleton
    rc, out = run_tool("experiment_decision_starter.py", packet)
    print("\n## DECISION SKELETON (JSON; fill after comparison; decision stays pending)")
    print(out or "(no output)")

    # Notes skeleton
    rc, out = run_tool("experiment_notes_starter.py", packet)
    print("\n## NOTES SKELETON (Markdown; fill sections after real evidence)")
    print(out or "(no output)")

    print("\n" + "=" * 72)
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    print("Next steps (do not invent numbers or decisions):")
    print("1. Choose one hypothesis, one primary_metric, and 3-5 guardrails from the suggestions above.")
    print("2. Edit the printed baseline JSON: set a real numeric baseline and a documented source.")
    print("3. Optionally write with: python3 tools/experiment_baseline_starter.py", packet, "--write")
    print("4. After publish + 10 day observation window (7 calendar + 3 Analytics lag) + collected metrics, edit the decision skeleton then write it.")
    print("5. Fill the notes Markdown with the chosen hypothesis/metric/guardrails and real values.")
    print("experiment_loop.py rejects missing numeric baselines, placeholder sources, and multi-variable changes.")
    print("Preferred unblocked path remains human OAuth (secrets + dispatch) before any live metrics exist.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
