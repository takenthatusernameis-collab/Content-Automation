#!/usr/bin/env python3
"""Read-only copy-paste command for the next packet step.

Turns next_action.py's one-line recommendation into a concrete CLI.
Does not write files, bump status, create media, or call YouTube.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from next_action import recommend  # noqa: E402
from pipeline_status import inspect, packet_dirs  # noqa: E402
from set_status import check as status_check, is_fixture  # noqa: E402
from validate_packet import packet_duration_warning  # noqa: E402


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def commands_for(path: Path, row: dict[str, object], code: str) -> list[str]:
    """Zero or more copy-paste commands. Never includes --write by default."""
    p = rel(path)
    if code == "skip":
        return []
    if code == "fix-gate":
        return [f"python3 tools/validate_packet.py {p}"]
    if code == "fix-status":
        return [f"python3 tools/set_status.py {p} --to draft"]
    if code == "fill-idea":
        return [
            "# paste topic/problem/mechanism into idea.md from the new_packet reprint",
            "# expand_prompt exits 2 until that paste exists; it does not write idea.md",
            f"python3 tools/doctor.py {p}",
        ]
    if code in {"write-script", "expand-script"}:
        cmds = [f"python3 tools/expand_prompt.py {p}"]
        if is_fixture(path):
            cmds.append(
                "# fixture lock: do not apply_script --write onto this packet"
            )
        else:
            cmds.append(
                f"python3 tools/apply_script.py {p} --from FILE"
            )
            cmds.append(
                f"# after dry-run OK: python3 tools/apply_script.py {p} --from FILE --write --refresh"
            )
        return cmds
    if code in {"lock-titles", "lock-thumb"}:
        return [f"python3 tools/title_thumb_brief.py {p} --dry-run"]
    if code == "complete-draft":
        return [f"python3 tools/validate_packet.py --draft {p}"]
    if code == "record-vo":
        cmds: list[str] = []
        if str(row["status"]) == "draft" and not is_fixture(path):
            blocked = status_check(path, "ready_for_vo")
            cmds.append(f"python3 tools/set_status.py {p} --to ready_for_vo")
            if blocked:
                cmds.append("# set_status blocked: " + blocked[0])
            else:
                cmds.append(
                    f"# after dry-run OK: python3 tools/set_status.py {p} --to ready_for_vo --write"
                )
        cmds.append("# then record the selected take at the named vo/ path (do not invent the file)")
        return cmds
    if code == "build-cards":
        return ["# create the named cards/*.png locally; do not download stock from tools"]
    if code == "edit":
        return [
            f"python3 tools/render_brief.py {p} --dry-run",
            "# export the named mp4 after edit; do not write an ffmpeg recipe here",
        ]
    if code == "export":
        return [f"python3 tools/render_brief.py {p} --dry-run"]
    if code == "upload-blocked":
        return ["# YouTube OAuth is not configured. Review publish.md. Do not call the API."]
    if code == "analytics-unbuilt":
        return ["# analytics is unbuilt; do not invent numbers"]
    if code == "open-item":
        return [f"python3 tools/next_action.py {p}"]
    return []


def format_item(path: Path, row: dict[str, object], rec: tuple[str, str]) -> str:
    code, why = rec
    cmds = commands_for(path, row, code)
    dur = packet_duration_warning(path)
    lines = [
        f"Packet: {path.name}",
        f"Status: {row['status']}",
        f"Gate: {row['gate']}",
        f"Code: {code}",
        f"Why: {why}",
    ]
    if dur:
        lines.append(f"Duration WARN: {dur}")
    lines.append("Command:")
    if cmds:
        lines.extend(f"  {c}" for c in cmds)
    else:
        lines.append("  (none)")
    lines.append("This command writes nothing.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only copy-paste CLI for the next packet step. "
            "Does not write files or bump status."
        )
    )
    parser.add_argument("packet", nargs="?", help="One packet folder (default: all videos/*)")
    args = parser.parse_args()

    if args.packet:
        targets = [Path(args.packet).resolve()]
    else:
        targets = packet_dirs(ROOT)
        if not targets:
            print("no packets under videos/", file=sys.stderr)
            return 1

    blocks = []
    for t in targets:
        row = inspect(t)
        rec = recommend(t, row)
        blocks.append(format_item(t, row, rec))
    sys.stdout.write("\n".join(blocks))
    if len(targets) > 1:
        sys.stdout.write(f"Packets: {len(targets)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
