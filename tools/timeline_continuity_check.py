#!/usr/bin/env python3
"""Timeline continuity consistency check.

Read-only. Uses timeline.plan() so starts, durations, spoken, and export stay identical to the planner.
Verifies continuous sequential coverage (each next start == previous start + dur, within epsilon),
sum of section durations equals spoken estimate, and export equals spoken + 20s end-screen reserve.
Complements structure_order_consistency (order), section_pacing_consistency (duration bands),
and section_budget_consistency (word bands). Surfaces planning arithmetic drift before assembly.
Does not invent media, run ffmpeg, poll secrets, bump status, or write files.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from timeline import plan, END_SCREEN  # noqa: E402

EPSILON = 0.05  # seconds tolerance for float rounding


def inspect(packet: Path) -> dict:
    data = plan(packet)
    rows = data.get("rows") or []
    spoken = float(data.get("spoken") or 0.0)
    export = float(data.get("export") or 0.0)
    if not rows or spoken <= 0:
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "no timeline rows or zero spoken",
            "continuous": False,
            "sum_matches_spoken": False,
            "export_matches": False,
            "gaps": [],
            "overlaps": [],
        }

    gaps = []
    overlaps = []
    continuous = True
    prev_end = 0.0
    for i, row in enumerate(rows):
        start = float(row.get("start") or 0.0)
        dur = float(row.get("dur") or 0.0)
        expected_start = prev_end
        if abs(start - expected_start) > EPSILON:
            continuous = False
            if start > expected_start:
                gaps.append(f"after row {i}: gap {start - expected_start:.2f}s")
            else:
                overlaps.append(f"at row {i+1}: overlap {expected_start - start:.2f}s")
        prev_end = start + dur

    sum_durs = sum(float(r.get("dur") or 0.0) for r in rows)
    sum_matches_spoken = abs(sum_durs - spoken) <= EPSILON
    export_matches = abs(export - (spoken + END_SCREEN)) <= EPSILON

    issues = []
    if not continuous:
        issues.append("discontinuous")
    if not sum_matches_spoken:
        issues.append(f"sum_durs={sum_durs:.1f} != spoken={spoken:.1f}")
    if not export_matches:
        issues.append(f"export={export:.1f} != spoken+{END_SCREEN}={spoken + END_SCREEN:.1f}")

    warn = bool(issues)
    return {
        "ok": not warn,
        "code": "WARN" if warn else "OK",
        "detail": "; ".join(issues) if issues else "continuous; sum matches spoken; export matches reserve",
        "continuous": continuous,
        "sum_matches_spoken": sum_matches_spoken,
        "export_matches": export_matches,
        "gaps": gaps,
        "overlaps": overlaps,
        "sum_durs": round(sum_durs, 1),
        "spoken_s": spoken,
        "export_s": export,
        "row_count": len(rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check timeline continuity, duration sum, and export reserve arithmetic. No writes."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    rep = inspect(path)
    print(f"packet: {path.name}")
    print(f"rows: {rep.get('row_count')}")
    print(f"sum_durs: {rep.get('sum_durs')}")
    print(f"spoken_s: {rep.get('spoken_s')}")
    print(f"export_s: {rep.get('export_s')}")
    print(f"continuous: {rep.get('continuous')}")
    print(f"sum_matches_spoken: {rep.get('sum_matches_spoken')}")
    print(f"export_matches: {rep.get('export_matches')}")
    if rep.get("gaps"):
        print(f"gaps: {'; '.join(rep['gaps'])}")
    if rep.get("overlaps"):
        print(f"overlaps: {'; '.join(rep['overlaps'])}")
    print(f"consistency: {rep['code']} ({rep['detail']})")
    print("Does not execute encode, invent media, or poll OAuth.")
    return 0 if rep["code"] != "NO_DATA" else 2


if __name__ == "__main__":
    raise SystemExit(main())
