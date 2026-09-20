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

from next_action import recommend, selected_vo_path  # noqa: E402
from pipeline_status import inspect, packet_dirs  # noqa: E402
from set_status import check as status_check, is_fixture  # noqa: E402
from validate_packet import packet_duration_warning  # noqa: E402


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def draft_from(path: Path, p: str) -> str:
    """Prefer PATH/draft.md when that file already exists. Never invent WORDS."""
    if (path / "draft.md").is_file():
        return f"{p}/draft.md"
    return f"{p}/draft.md"


def commands_for(path: Path, row: dict[str, object], code: str) -> list[str]:
    """Zero or more copy-paste commands. Never includes --write by default."""
    p = rel(path)
    draft = draft_from(path, p)
    if code == "skip":
        return []
    if code == "fix-gate":
        return [f"python3 tools/validate_packet.py {p}"]
    if code == "fix-status":
        return [f"python3 tools/set_status.py {p} --to draft"]
    if code == "fill-idea":
        return [
            f"python3 tools/idea_brief.py {p}",
            f"python3 tools/idea_brief.py {p} --block",
            "# paste that --block body into idea.md by hand; idea_brief writes nothing",
            f"python3 tools/idea_brief.py {p} --check",
            "# --check exit 2: paste still blank or mismatched; reprint --block",
            "# --check exit 0 PASTE READY: then expand off-repo; do not treat stdout as script.md",
        ]
    if code in {"write-script", "expand-script"}:
        cmds = [
            f"python3 tools/expand_prompt.py {p}",
            f"# save the off-repo draft to {draft}; do not treat expand_prompt stdout as script.md",
            "# empty first draft Target: hook 28 / payoff 60 / beats 220x4 / CTA 50 / land ~1010; do not invent filler",
            f"python3 tools/words.py {p}",
            "# read Result + Delta + Hook Delta + Beats + Thin + Grow or Cut; IN BAND is not apply --write",
        ]
        if is_fixture(path):
            cmds.append(
                "# fixture lock: do not apply_script --write onto this packet"
            )
        else:
            cmds.append(
                f"python3 tools/apply_script.py {p} --from {draft}"
            )
            cmds.append(
                f"# after dry-run OK and words.py IN BAND: python3 tools/apply_script.py {p} --from {draft} --write --refresh"
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
        vo = selected_vo_path(path)
        cmds.append(f"# DROP path: {vo}")
        cmds.append("# follow docs/gate_machine.md on the gate machine")
        cmds.append("# record, cp an existing generated file, or one optional TTS one-liner on that page")
        cmds.append("# do not invent the file in git; repo-root vo/ is not Selected VO; do not git add -f")
        cmds.append("# do not wrap those TTS one-liners into tools/")
        return cmds
    if code == "build-cards":
        return [
            f"python3 tools/card_generator.py {p} --write-manifest",
            "# requires Pillow; writes gitignored 1920x1080 PNGs under cards/",
            "# do not git add -f pngs; --mark-ready only after inspect-only reports all yes",
        ]
    if code == "edit":
        return [
            f"python3 tools/timeline.py {p} --write",
            f"python3 tools/media_qa.py {p}",
            f"python3 tools/assemble.py {p}",
            "# assemble stays dry-run until READY_TO_ENCODE; do not write a dummy export/master.mp4",
            f"python3 tools/render_brief.py {p} --dry-run",
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
