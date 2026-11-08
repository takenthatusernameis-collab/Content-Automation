#!/usr/bin/env python3
"""Validate an experiment_baseline.json or experiment_decision.json against the load rules.

Reduces future human error when filling the templates after the first publish.
Does not invent values. Does not write files. Soft only.
Usage:
  python3 tools/experiment_template_validator.py path/to/experiment_baseline.json
  python3 tools/experiment_template_validator.py path/to/experiment_decision.json [--comparison-metric NAME]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from experiment_loop import (  # noqa: E402
    ALLOWED_CHANGES,
    REJECTED_SOURCES,
    RECORDED_DECISIONS,
)


def validate_baseline(data: dict) -> list[str]:
    errors = []
    hypothesis = str(data.get("hypothesis") or "").strip()
    change = str(data.get("change") or "").strip()
    metric = str(data.get("primary_metric") or "").strip()
    source = str(data.get("source") or "").strip()
    baseline = data.get("baseline")
    if not hypothesis:
        errors.append("missing or empty hypothesis")
    if not metric:
        errors.append("missing or empty primary_metric")
    if not source:
        errors.append("missing or empty source")
    if change not in ALLOWED_CHANGES:
        errors.append(f"change {change!r} not in {sorted(ALLOWED_CHANGES)}")
    if source.lower() in REJECTED_SOURCES:
        errors.append("source looks invented/placeholder/guess")
    if baseline is None or baseline == "":
        errors.append("baseline value missing (must be numeric for a real file)")
    elif not isinstance(baseline, (int, float)) and not (
        isinstance(baseline, str) and baseline.strip().replace(".", "", 1).isdigit()
    ):
        errors.append("baseline value is not numeric")
    if data.get("_template"):
        errors.append("still marked as template; replace placeholder values before use")
    return errors


def validate_decision(data: dict, comparison_metric: str | None = None) -> list[str]:
    errors = []
    decision = str(data.get("decision") or "").strip().lower()
    reason = str(data.get("reason") or "").strip()
    source = str(data.get("source") or "").strip()
    if decision not in RECORDED_DECISIONS:
        errors.append(f"decision must be one of {sorted(RECORDED_DECISIONS)}")
    if not reason:
        errors.append("missing or empty reason")
    if not source:
        errors.append("missing or empty source")
    if source.lower() in REJECTED_SOURCES:
        errors.append("source looks invented/placeholder/guess")
    metric = str(data.get("primary_metric") or "").strip()
    if comparison_metric and metric and metric != comparison_metric:
        errors.append(f"primary_metric {metric!r} does not match comparison {comparison_metric!r}")
    if data.get("_template"):
        errors.append("still marked as template; replace placeholder values before use")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate experiment baseline or decision JSON against load rules.")
    parser.add_argument("path", help="Path to experiment_baseline.json or experiment_decision.json")
    parser.add_argument("--comparison-metric", default="", help="Optional primary_metric from a comparison for decision validation")
    args = parser.parse_args()
    path = Path(args.path)
    if not path.is_file():
        print(f"FAIL: file not found: {path}")
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL: not valid JSON: {e}")
        return 1
    if not isinstance(data, dict):
        print("FAIL: must be a JSON object")
        return 1
    name = path.name.lower()
    if "baseline" in name:
        errors = validate_baseline(data)
        kind = "baseline"
    elif "decision" in name:
        errors = validate_decision(data, args.comparison_metric or None)
        kind = "decision"
    else:
        print("FAIL: filename must contain 'baseline' or 'decision'")
        return 1
    if errors:
        print(f"FAIL: {kind} validation errors:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PASS: {kind} passes load rules (numeric baseline / explicit decision required for real use)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
