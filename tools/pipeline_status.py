#!/usr/bin/env python3
"""Read-only production board for video packets.

Shows declared status, structural gate, disk presence, and status drift.
Does not write files, run ffmpeg, call YouTube, or invent media.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from render_brief import packet_id_slug, presence_rows, selected_vo_drop  # noqa: E402
from validate_packet import VALID_STATUS, field, validate  # noqa: E402

NEEDS_VO = {"ready_for_edit", "ready_to_publish", "published"}
NEEDS_EXPORT = {"ready_to_publish", "published"}
NEEDS_SCRIPT = {"ready_for_vo", "ready_for_edit", "ready_to_publish", "published"}


def packet_dirs(root: Path) -> list[Path]:
    videos = root / "videos"
    if not videos.is_dir():
        return []
    return sorted(
        p for p in videos.iterdir() if p.is_dir() and not p.name.startswith("_")
    )


def gate_label(path: Path) -> tuple[str, list[str], list[str]]:
    errors, incompletes = validate(path, draft=False)
    if errors:
        return "FAIL", errors, incompletes
    draft_err, draft_inc = validate(path, draft=True)
    if draft_err:
        return "FAIL", draft_err, draft_inc
    if draft_inc:
        return "DRAFT", draft_err, draft_inc
    return "PASS", [], []


def disk_summary(path: Path) -> tuple[str, int, int, dict[str, str]]:
    rows = presence_rows(path)
    present = sum(1 for r in rows if r["state"] == "present")
    missing = sum(1 for r in rows if r["state"] == "missing")
    by_role = {r["role"]: r["state"] for r in rows}
    if not rows:
        label = "none"
    elif present == 0:
        label = "all-missing"
    elif missing == 0:
        label = "all-present"
    else:
        label = "partial"
    return label, present, missing, by_role


def remaining_open(path: Path) -> int:
    text = (path / "packet.md").read_text(encoding="utf-8") if (path / "packet.md").is_file() else ""
    return len([ln for ln in text.splitlines() if ln.strip().startswith("- [ ]")])


def drift_notes(
    status: str, gate: str, by_role: dict[str, str]
) -> list[str]:
    notes: list[str] = []
    if status and status not in VALID_STATUS:
        notes.append(f"unknown-status:{status}")
        return notes
    vo = by_role.get("Selected VO", "missing")
    export = by_role.get("Master export", "missing")
    if status in NEEDS_SCRIPT and gate == "FAIL":
        notes.append("status-ahead-of-script")
    if status in NEEDS_VO and vo != "present":
        notes.append("status-ahead-of-vo")
    if status in NEEDS_EXPORT and export != "present":
        notes.append("status-ahead-of-export")
    if status == "published" and gate != "PASS":
        notes.append("published-without-pass")
    return notes


def inspect(path: Path) -> dict[str, object]:
    packet_text = (path / "packet.md").read_text(encoding="utf-8") if (path / "packet.md").is_file() else ""
    status = field(packet_text, "status") or "missing"
    title = field(packet_text, "working_title")
    gate, errors, incompletes = gate_label(path)
    disk, present, missing, by_role = disk_summary(path)
    drift = drift_notes(status, gate, by_role)
    vo_state = by_role.get("Selected VO", "missing")
    return {
        "name": path.name,
        "status": status,
        "title": title,
        "gate": gate,
        "errors": errors,
        "incompletes": incompletes,
        "disk": disk,
        "present": present,
        "missing": missing,
        "open_human": remaining_open(path),
        "drift": drift,
        "vo_state": vo_state,
        "vo_drop": selected_vo_drop(path),
    }


def format_row(row: dict[str, object]) -> str:
    drift = ",".join(row["drift"]) if row["drift"] else "—"
    disk = f"{row['disk']} {row['present']}/{row['present'] + row['missing']}"
    return (
        f"{row['name']:<42} {row['status']:<16} {row['gate']:<6} "
        f"{disk:<22} {row['open_human']:<4} {drift}"
    )


def format_report(rows: list[dict[str, object]]) -> str:
    header = (
        f"{'PACKET':<42} {'STATUS':<16} {'GATE':<6} "
        f"{'DISK':<22} {'OPEN':<4} DRIFT"
    )
    lines = [
        header,
        "-" * len(header),
    ]
    for row in rows:
        lines.append(format_row(row))
    lines.append("")
    lines.append(
        "GATE is validate_packet publish completeness. "
        "DISK is render_brief presence (present/total named paths). "
        "OPEN is unchecked Remaining human work boxes. "
        "DRIFT means packet status is ahead of script/VO/export evidence."
    )
    lines.append("This command writes nothing and creates no media.")
    lines.append(
        "Selected VO drop is videos/NNN-slug/vo/NNN-slug-take-selected.wav. "
        "Repo-root vo/ is not Selected VO. Follow docs/gate_machine.md on the gate machine."
    )
    drifted = [r for r in rows if r["drift"]]
    failed = [r for r in rows if r["gate"] == "FAIL"]
    missing_vo = [r for r in rows if r.get("vo_state") != "present"]
    lines.append(
        f"Packets: {len(rows)}  FAIL: {len(failed)}  DRIFT: {len(drifted)}  MISSING-VO: {len(missing_vo)}"
    )
    for row in rows:
        show_drop = row.get("vo_state") != "present"
        if row["errors"] or row["incompletes"] or row["drift"] or show_drop:
            lines.append(f"  {row['name']}:")
            for e in row["errors"]:
                lines.append(f"    FAIL {e}")
            for i in row["incompletes"]:
                lines.append(f"    DRAFT {i}")
            for d in row["drift"]:
                lines.append(f"    DRIFT {d}")
            if show_drop:
                if row["name"] == "002-stop-deciding-what-to-work-on-every-morning":
                    lines.append(
                        "    PUBLISH edit publish.md (delete 'No upload happened'; check Description edited and First comment approved). "
                        "Fetch q1-media-r253 q1-master-r253.mp4 only. Do not record. Do not copy r249 q1-master.mp4. Follow docs/gate_machine.md."
                    )
                else:
                    lines.append(
                        f"    DROP `{row['vo_drop']}` (repo-root vo/ is not Selected VO; follow docs/gate_machine.md)"
                    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only packet board: status, QA gate, disk presence, drift."
    )
    parser.add_argument("packet", nargs="?", help="One packet folder (default: all videos/*)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any packet has FAIL gate or status drift",
    )
    args = parser.parse_args()

    if args.packet:
        targets = [Path(args.packet).resolve()]
    else:
        targets = packet_dirs(ROOT)
        if not targets:
            print("no packets under videos/", file=sys.stderr)
            return 1

    rows = [inspect(t) for t in targets]
    sys.stdout.write(format_report(rows))
    if args.strict and any(r["gate"] == "FAIL" or r["drift"] for r in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
