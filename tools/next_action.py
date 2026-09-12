#!/usr/bin/env python3
"""Read-only next human action for video packets.

Uses the same inspect data as pipeline_status.py.
Does not write files, bump status, run ffmpeg, or invent media.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from expand_prompt import idea_mechanism_blank  # noqa: E402
from pipeline_status import inspect, packet_dirs  # noqa: E402
from render_brief import packet_id_slug, planned_cards  # noqa: E402
from validate_packet import packet_duration_warning  # noqa: E402


def first_open(path: Path) -> str:
    packet = path / "packet.md"
    if not packet.is_file():
        return ""
    for ln in packet.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if s.startswith("- [ ]"):
            return s[5:].strip()
    return ""


def idea_text(path: Path) -> str:
    idea = path / "idea.md"
    if not idea.is_file():
        return ""
    return idea.read_text(encoding="utf-8")


def recommend(path: Path, row: dict[str, object]) -> tuple[str, str]:
    """Return (code, sentence). One action. Never mutates."""
    status = str(row["status"])
    vid, slug = packet_id_slug(path)
    vo_name = f"vo/{vid}-{slug}-take-selected.wav"
    export_name = f"exports/{vid}-{slug}-v1.mp4"
    open_item = first_open(path)

    if status == "abandoned":
        return "skip", "Packet is abandoned. No production action."

    errors = list(row["errors"])
    if errors:
        return "fix-gate", f"Fix packet FAIL before anything else: {errors[0]}"

    drift = list(row["drift"])
    if any(d.startswith("unknown-status") for d in drift):
        return (
            "fix-status",
            f"Status {status!r} is not a valid packet status. Set a known value in packet.md.",
        )
    if "status-ahead-of-script" in drift:
        return (
            "write-script",
            "Status is ahead of a passing script. Fill WORDS (hook 20–35, CTA) or lower status to draft.",
        )
    if "status-ahead-of-vo" in drift:
        return (
            "record-vo",
            f"Status is ahead of Selected VO. Put a take at `{vo_name}` or lower status. Do not invent the file.",
        )
    if "status-ahead-of-export" in drift:
        return (
            "export",
            f"Status is ahead of Master export. Export `{export_name}` after edit, or lower status.",
        )
    if "published-without-pass" in drift:
        return "fix-gate", "Status is published but the packet gate is not PASS. Fix the gate first."

    if idea_mechanism_blank(idea_text(path)):
        return (
            "fill-idea",
            "idea.md mechanism is blank or template-default. Run idea_brief --block, paste by hand, then idea_brief --check. Do not treat that paste as spoken WORDS.",
        )

    incompletes = list(row["incompletes"])
    if incompletes:
        first = incompletes[0]
        low = first.lower()
        if "hook" in low or "cta" in low:
            return "write-script", f"Write spoken WORDS next: {first}"
        if "title" in low:
            return "lock-titles", f"Fill titles.md next: {first}"
        if "thumbnail" in low:
            return "lock-thumb", f"Fill thumbnail on-image text next: {first}"
        return "complete-draft", f"Finish draft intake: {first}"

    # Structural PASS can still be far under the locked runtime.
    # Recording a 1-minute take for explainer-6-10min wastes the VO session.
    dur = packet_duration_warning(path)
    if dur and status in {"draft", "ready_for_vo"}:
        return (
            "expand-script",
            f"Do not record yet. {dur}. Expand beats in script.md; do not pad the sample fixture.",
        )

    if status in {"draft", "ready_for_vo"}:
        return (
            "record-vo",
            f"Script gate is PASS. Record the selected take at `{vo_name}` before raising status.",
        )

    if status == "ready_for_edit":
        missing_cards = [
            c for c in planned_cards(path) if not (path / c).is_file()
        ]
        if missing_cards:
            return (
                "build-cards",
                f"Build the first planned card `{missing_cards[0]}` (local file; do not download stock from this tool).",
            )
        return (
            "edit",
            f"Selected VO is present. Edit against docs/editor.md and docs/format.md, then export `{export_name}`.",
        )

    if status == "ready_to_publish":
        return (
            "upload-blocked",
            "Export is present. YouTube OAuth is not configured (BLOCKED.md). Review publish.md; do not call the API.",
        )

    if status == "published":
        return (
            "analytics-unbuilt",
            "Marked published. Analytics is unbuilt. Do not invent performance numbers.",
        )

    if open_item:
        return "open-item", f"Next unchecked human box: {open_item}"
    return "none", "No next action derived. Inspect packet.md by hand."


def format_report(items: list[tuple[Path, dict[str, object], tuple[str, str]]]) -> str:
    header = f"{'PACKET':<42} {'STATUS':<16} {'CODE':<18} NEXT"
    lines = [header, "-" * 110]
    for path, row, (code, text) in items:
        lines.append(f"{path.name:<42} {str(row['status']):<16} {code:<18} {text}")
    lines.append("")
    lines.append(
        "This command writes nothing. It does not bump status, create media, or call YouTube."
    )
    lines.append(f"Packets: {len(items)}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only next human action per packet. No writes."
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

    items = []
    for t in targets:
        row = inspect(t)
        items.append((t, row, recommend(t, row)))
    sys.stdout.write(format_report(items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
