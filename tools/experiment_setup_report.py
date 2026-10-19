#!/usr/bin/env python3
"""One-command experiment setup report for a packet.

Aggregates experiment_metric_suggest, experiment_guardrail_suggest, and
experiment_hypothesis_suggest into a concise combined view of change-aligned
suggestions for preparing an experiment baseline or notes.
Detects the single allowed change once (from baseline if present, else idea.md heuristic).
Does not invent numeric baselines, results, or decisions. Does not write files. Does not call APIs.
Complements the individual suggesters and starters without replacing them.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

def run_suggester(script: str, packet: str) -> tuple[int, str]:
    """Run a suggester tool and return (returncode, output)."""
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

def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the experiment setup report."""
    p = packet
    return [
        f"pick metric: choose one primary_metric from the candidates above",
        f"pick hypothesis: choose one hypothesis template from the suggestions",
        f"pick guardrails: select 3-5 relevant guardrails",
        f"baseline starter: python3 tools/experiment_baseline_starter.py {p}",
        f"notes starter: python3 tools/experiment_notes_starter.py {p}",
        f"package starter: python3 tools/experiment_package_starter.py {p}",
        f"setup report again if needed: python3 tools/experiment_setup_report.py {p}",
        f"quality scans: python3 tools/quality_scan.py {p} && python3 tools/claim_scan.py {p}",
        f"full production: python3 tools/full_production_starter.py {p}",
    ]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate experiment setup suggestions for a packet. No invented values."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()
    packet = args.packet
    path = Path(packet).resolve()
    if not path.is_dir() or not (path / "idea.md").is_file():
        print(f"No idea.md in {packet}", file=sys.stderr)
        return 1

    print("EXPERIMENT SETUP REPORT (suggestions only; no invented baseline, result, or decision)")
    print("Use these to choose one hypothesis, one metric, and guardrails, then run experiment_baseline_starter.py and edit.")
    print("=" * 72)

    # Metric suggestions
    rc, out = run_suggester("experiment_metric_suggest.py", packet)
    print("\n## METRIC SUGGESTIONS")
    print(out or "(no output)")

    # Guardrail suggestions
    rc, out = run_suggester("experiment_guardrail_suggest.py", packet)
    print("\n## GUARDRAIL SUGGESTIONS")
    print(out or "(no output)")

    # Hypothesis suggestions
    rc, out = run_suggester("experiment_hypothesis_suggest.py", packet)
    print("\n## HYPOTHESIS SUGGESTIONS")
    print(out or "(no output)")

    print("\n" + "=" * 72)
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    print("Next steps (do not invent numbers or decisions):")
    print("1. Choose one primary_metric from the candidates and one hypothesis template.")
    print("2. Select 3-5 relevant guardrails.")
    print("3. Run: python3 tools/experiment_baseline_starter.py", packet)
    print("4. Edit the printed JSON: set a real numeric baseline and a documented source (not placeholder/invented).")
    print("5. After publish + observation window + collected metrics, use experiment_decision_starter.py then edit reason/source.")
    print("experiment_loop.py rejects missing numeric baselines, placeholder sources, and multi-variable changes.")
    print("Preferred unblocked path remains human OAuth (secrets + dispatch) before any live metrics exist.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
