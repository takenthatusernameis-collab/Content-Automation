#!/usr/bin/env python3
"""Explicit packet status change. Dry-run default. Never invents media.

pipeline_status.py and next_action.py stay read-only. This is the only
tool allowed to rewrite the status line in packet.md, and only with --write.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from next_action import selected_vo_path  # noqa: E402
from pipeline_status import disk_summary, inspect  # noqa: E402
from validate_packet import VALID_STATUS, field, packet_duration_warning  # noqa: E402

FIXTURE_PREFIX = "sample-001"
ORDER = (
    "draft",
    "ready_for_vo",
    "ready_for_edit",
    "ready_to_publish",
    "published",
)
# abandoned is a side exit, not a step in ORDER.


def is_fixture(packet: Path) -> bool:
    return packet.name.startswith(FIXTURE_PREFIX)


def set_field_line(text: str, name: str, value: str) -> str:
    pat = re.compile(rf"^(-\s*{re.escape(name)}:)[ \t]*([^\n]*)$", re.M)
    if pat.search(text):
        return pat.sub(r"\1 " + value, text, count=1)
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    inserted = False
    for ln in lines:
        out.append(ln)
        if not inserted and re.match(r"^-\s*working_title:", ln):
            out.append(f"- {name}: {value}\n")
            inserted = True
    if not inserted:
        out.append(f"- {name}: {value}\n")
    return "".join(out)


def check(packet: Path, target: str) -> list[str]:
    errors: list[str] = []
    if target not in VALID_STATUS:
        errors.append(f"invalid target status: {target!r}")
        return errors

    row = inspect(packet)
    current = str(row["status"])
    gate = str(row["gate"])
    errors_gate = list(row["errors"])

    if is_fixture(packet) and target not in {"draft", "abandoned"}:
        errors.append(
            f"refusing fixture {packet.name}: keep sample-001 at draft "
            "(or abandon). Do not promote the QA target."
        )

    if current == target:
        errors.append(f"already {target}")
        return errors

    if target != "abandoned" and current not in {"abandoned", "missing"}:
        if current in ORDER and target in ORDER:
            ci = ORDER.index(current)
            ti = ORDER.index(target)
            if ti > ci + 1:
                errors.append(
                    f"refusing skip {current} -> {target}; move one step at a time"
                )

    if target == "ready_for_vo":
        if gate == "FAIL":
            errors.append(
                f"refusing ready_for_vo: publish gate FAIL ({errors_gate[0] if errors_gate else 'unknown'})"
            )
        dur = packet_duration_warning(packet)
        if dur:
            errors.append(f"refusing ready_for_vo while duration WARN: {dur}")
        from quality_scan import scan_path

        found = scan_path(packet)
        if found:
            detail = ", ".join(phrase for phrase, _count in found)
            errors.append(f"refusing ready_for_vo: quality_scan hits ({detail})")
        from claim_scan import scan_path as claim_scan_path

        claim_hits = claim_scan_path(packet)
        if claim_hits:
            detail = ", ".join(f"{kind}:{token}" for kind, token in claim_hits)
            errors.append(f"refusing ready_for_vo: claim_scan hits ({detail})")
        from title_scan import scan_path as title_scan_path

        title_hits = title_scan_path(packet)
        if title_hits:
            detail = ", ".join(f"{kind}:{token}" for kind, token in title_hits)
            errors.append(f"refusing ready_for_vo: title_scan hits ({detail})")

    if target == "ready_for_edit":
        _label, _p, _m, by_role = disk_summary(packet)
        if by_role.get("Selected VO") != "present":
            vo = selected_vo_path(packet)
            errors.append(
                f"refusing ready_for_edit: Selected VO missing on disk "
                f"(need `{vo}`; repo-root vo/ is not Selected VO)"
            )
        if gate == "FAIL":
            errors.append("refusing ready_for_edit: publish gate FAIL")
        dur = packet_duration_warning(packet)
        if dur:
            errors.append(f"refusing ready_for_edit while duration WARN: {dur}")

    if target in {"ready_to_publish", "published"}:
        _label, _p, _m, by_role = disk_summary(packet)
        if by_role.get("Selected VO") != "present":
            vo = selected_vo_path(packet)
            errors.append(
                f"refusing {target}: Selected VO missing on disk "
                f"(need `{vo}`; repo-root vo/ is not Selected VO)"
            )
        if by_role.get("Master export") != "present":
            errors.append(f"refusing {target}: Master export missing on disk")
        if gate != "PASS":
            errors.append(f"refusing {target}: gate is {gate}, need PASS")

    return errors


def report(packet: Path, current: str, target: str, errors: list[str]) -> str:
    row = inspect(packet)
    lines = [
        f"Packet: {packet.name}",
        f"Status now: {current}",
        f"Status want: {target}",
        f"Gate: {row['gate']}",
        f"Disk: {row['disk']} {row['present']}/{int(row['present']) + int(row['missing'])}",
        f"Drift: {','.join(row['drift']) if row['drift'] else '—'}",
    ]
    dur = packet_duration_warning(packet)
    if dur:
        lines.append(f"Duration WARN: {dur}")
    if errors:
        lines.append("Result: BLOCKED")
        lines.extend(f"  - {e}" for e in errors)
    else:
        lines.append("Result: OK to write status (does not create media)")
    return "\n".join(lines) + "\n"


def apply_status(text: str, target: str, today: str) -> str:
    text = set_field_line(text, "status", target)
    text = set_field_line(text, "updated", today)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Set packet.md status with evidence checks. "
            "Default is dry-run. Does not create VO/export or bump sample-001."
        )
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--to", dest="target", required=True, help="Target status")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the status line. Without this flag, print a report only.",
    )
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    packet_path = path / "packet.md"
    if not packet_path.is_file():
        print(f"missing packet.md: {packet_path}", file=sys.stderr)
        return 1

    text = packet_path.read_text(encoding="utf-8")
    current = field(text, "status") or "missing"
    errors = check(path, args.target)
    sys.stdout.write(report(path, current, args.target, errors))
    if errors:
        return 1
    if not args.write:
        sys.stdout.write("Dry-run only. Pass --write to change packet.md status.\n")
        return 0

    today = dt.date.today().isoformat()
    packet_path.write_text(apply_status(text, args.target, today), encoding="utf-8")
    print(packet_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
