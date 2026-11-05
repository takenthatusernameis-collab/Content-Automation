#!/usr/bin/env python3
"""Scaffold a starter experiment_baseline.json from the template into a packet.

Copies docs/experiment_baseline.template.json to <packet>/experiment_baseline.json
if the destination does not already exist. Prints clear human instructions.
Does not invent values, overwrite existing files, call APIs, or poll secrets.
Useful after first publish so the learning loop has a ready skeleton.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs" / "experiment_baseline.template.json"
DEST_NAME = "experiment_baseline.json"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold experiment_baseline.json from template. No invent, no overwrite."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    packet = Path(args.packet).resolve()
    if not packet.is_dir():
        print(f"not a directory: {packet}", file=sys.stderr)
        return 1
    if not TEMPLATE.is_file():
        print(f"template missing: {TEMPLATE}", file=sys.stderr)
        return 1
    dest = packet / DEST_NAME
    if dest.is_file():
        print(f"experiment_baseline_scaffold SKIP: {dest} already exists (do not overwrite)")
        print("Fill the existing file then run: python3 tools/experiment_baseline_validate.py <packet>")
        return 0
    shutil.copy2(TEMPLATE, dest)
    print(f"experiment_baseline_scaffold WROTE: {dest}")
    print("TEMPLATE ONLY. Replace hypothesis, change, primary_metric, baseline (numeric), source with real documented values.")
    print("Do not invent metrics. See docs/experiment_baseline.template.json and tools/experiment_loop.py load_baseline.")
    print("After filling: python3 tools/experiment_baseline_validate.py <packet>")
    print("Then: python3 tools/experiment_loop.py <packet>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
