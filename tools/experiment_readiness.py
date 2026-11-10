#!/usr/bin/env python3
"""Print experiment readiness status for a packet after a video id exists.

Fail-closed check of whether experiment_baseline.json is present and filled
with a numeric baseline and non-placeholder source. Also reports on the
experiment_decision.json status (absent, template, or recorded).
Suggests exact next commands (starter, notes, loop) without inventing metrics or sources.
Does not poll secrets, invent values, dispatch, or write files.
Reusable for future packets once the OAuth stall ends.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def is_placeholder_source(source: str) -> bool:
    low = source.lower()
    bad = ("template", "replace", "invented", "placeholder", "guess", "assumed", "todo")
    return any(b in low for b in bad) or not source.strip()


def check_baseline(data: dict) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, "not a dict"
    baseline = data.get("baseline")
    source = str(data.get("source", ""))
    if baseline is None or not isinstance(baseline, (int, float)):
        return False, "baseline is null or non-numeric"
    if is_placeholder_source(source):
        return False, "source is placeholder or empty"
    hyp = str(data.get("hypothesis", "")).strip()
    if not hyp or "TEMPLATE" in hyp.upper():
        return False, "hypothesis missing or template"
    return True, "filled"


def check_decision(data: dict) -> tuple[str, str]:
    """Return (status, detail). status is ABSENT/TEMPLATE/RECORDED/INVALID."""
    if not isinstance(data, dict):
        return "INVALID", "not a dict"
    decision = str(data.get("decision") or "").strip()
    if not decision or "TEMPLATE" in decision.upper() or decision.upper().startswith("TEMPLATE"):
        return "TEMPLATE", "decision still a template (requires documented review after comparison)"
    reason = str(data.get("reason") or "").strip()
    source = str(data.get("source") or "").strip()
    if decision.lower() in ("keep", "discard", "retest") and reason and not is_placeholder_source(source):
        return "RECORDED", f"decision={decision.lower()}"
    return "INCOMPLETE", "decision present but missing real reason/source or not a recorded value"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    baseline_path = packet / "experiment_baseline.json"
    decision_path = packet / "experiment_decision.json"

    print("EXPERIMENT READINESS (fail-closed; no invent)")
    print(f"packet: {packet.name}")

    # Baseline check
    if not baseline_path.is_file():
        print("experiment_baseline.json: ABSENT")
        print("Next: python3 tools/experiment_baseline_starter.py", packet)
        print("Then edit numeric baseline + documented source. Do not invent.")
        print("EXPERIMENT READINESS HOLD (no baseline file)")
        return 0

    try:
        bdata = json.loads(baseline_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"experiment_baseline.json: INVALID JSON ({e})")
        print("EXPERIMENT READINESS FAIL")
        return 1

    bok, breason = check_baseline(bdata)
    if not bok:
        print(f"experiment_baseline.json: PRESENT but incomplete ({breason})")
        print("Next: edit the file with real numeric baseline and documented source.")
        print("See docs/experiment_baseline.template.json and tools/experiment_baseline_starter.py")
        print("EXPERIMENT READINESS HOLD (incomplete baseline)")
        return 0

    print("experiment_baseline.json: FILLED (numeric baseline + real source)")

    # Decision check (only meaningful after baseline is filled)
    if not decision_path.is_file():
        print("experiment_decision.json: ABSENT")
        print("Next after a numeric comparison exists: python3 tools/experiment_decision_starter.py", packet)
        print("Then edit decision/reason/source from a documented review. Do not invent.")
        print("EXPERIMENT READINESS HOLD (baseline filled; decision file missing)")
        return 0

    try:
        ddata = json.loads(decision_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"experiment_decision.json: INVALID JSON ({e})")
        print("EXPERIMENT READINESS FAIL")
        return 1

    dstatus, ddetail = check_decision(ddata)
    print(f"experiment_decision.json: {dstatus} ({ddetail})")

    if dstatus == "RECORDED":
        print("Next: python3 tools/experiment_loop.py", packet)
        print("EXPERIMENT READINESS PASS (baseline filled + decision recorded)")
    elif dstatus == "TEMPLATE":
        print("Next: edit the decision file with a real keep/discard/retest after reviewing the comparison.")
        print("Then: python3 tools/experiment_template_validator.py", decision_path)
        print("EXPERIMENT READINESS HOLD (decision still template)")
    else:
        print("Next: complete or replace the decision file. See tools/experiment_decision_starter.py")
        print("EXPERIMENT READINESS HOLD (decision incomplete)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
