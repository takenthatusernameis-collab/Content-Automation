#!/usr/bin/env python3
"""Fail-closed validator for experiment_baseline.json.

Imports the load_baseline contract from experiment_loop.py so the rules stay single-sourced.
Prints PASS or the exact failure reason. Does not invent values, write files, call APIs, or poll secrets.
Useful after a human fills a starter skeleton and before running the full experiment_loop.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from experiment_loop import load_baseline  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate experiment_baseline.json against the ledger contract. No invent."
    )
    parser.add_argument("packet", help="Path to packet folder containing (or expected to contain) experiment_baseline.json")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    data, detail = load_baseline(path)
    if data is None:
        print(f"experiment_baseline_validate FAIL: {detail}")
        return 1
    print("experiment_baseline_validate PASS")
    print(f"hypothesis: {data['hypothesis'][:80]}...")
    print(f"change: {data['change']}")
    print(f"primary_metric: {data['primary_metric']}")
    print(f"baseline: {data['baseline']}")
    print(f"source: {data['source'][:80]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
