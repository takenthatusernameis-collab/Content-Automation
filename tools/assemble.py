#!/usr/bin/env python3
"""Fail-closed ffmpeg assembly planner.

Builds a deterministic command from timeline.plan + media_qa.inspect_media.
Never invents media. Never bumps packet status. Never calls videos.insert.
Default mode prints the recipe only. --execute is refused unless media_qa
PASS, ready_to_assemble=yes, and ffmpeg is on PATH.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from media_qa import inspect_media  # noqa: E402
from render_brief import selected_vo_drop  # noqa: E402
from timeline import END_SCREEN, plan  # noqa: E402

TARGET_W = 1920
TARGET_H = 1080
TARGET_FPS = 30
TARGET_AUDIO_HZ = 48000
EXPORT_REL = "export/master.mp4"


def ffmpeg_present() -> bool:
    return shutil.which("ffmpeg") is not None


def command_for(packet: Path, data: dict) -> list[str]:
    """Build an ffmpeg argv. Paths are packet-relative as written."""
    args = ["ffmpeg", "-y"]
    vo = data["vo_rel"]
    args += ["-i", vo]
    card_inputs = []
    for row in data["rows"]:
        if not row["card"]:
            continue
        card_inputs.append((row["card"], float(row["dur"])))
        args += ["-loop", "1", "-t", f"{row['dur']:.1f}", "-i", row["card"]]
    last_card = card_inputs[-1][0] if card_inputs else None
    if last_card:
        args += ["-loop", "1", "-t", f"{END_SCREEN:.1f}", "-i", last_card]
    n_cards = len(card_inputs)
    concat_parts = []
    for i in range(n_cards):
        idx = i + 1
        concat_parts.append(f"[{idx}:v]scale={TARGET_W}:{TARGET_H},fps={TARGET_FPS},format=yuv420p[v{i}]")
    if last_card:
        end_idx = n_cards + 1
        concat_parts.append(
            f"[{end_idx}:v]scale={TARGET_W}:{TARGET_H},fps={TARGET_FPS},format=yuv420p[vend]"
        )
    labels = "".join(f"[v{i}]" for i in range(n_cards))
    n = n_cards + (1 if last_card else 0)
    if last_card:
        labels += "[vend]"
    filter_complex = ";".join(concat_parts)
    if n:
        filter_complex += f";{labels}concat=n={n}:v=1:a=0[vout]"
    args += [
        "-filter_complex",
        filter_complex,
        "-map",
        "[vout]",
        "-map",
        "0:a",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-r",
        str(TARGET_FPS),
        "-c:a",
        "aac",
        "-ar",
        str(TARGET_AUDIO_HZ),
        "-ac",
        "2",
        "-shortest",
        "-movflags",
        "+faststart",
        EXPORT_REL,
    ]
    return args


def inspect_assemble(packet: Path) -> dict:
    data = plan(packet)
    qa = inspect_media(packet)
    cmd = command_for(packet, data) if data["rows"] else []
    ff = ffmpeg_present()
    export = packet / EXPORT_REL
    export_ok = export.is_file() and export.stat().st_size > 0

    checks = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("ready_to_assemble", bool(data["ready_to_assemble"]), "timeline gate")
    add("media_qa_pass", qa["gate"] == "PASS", qa["gate"])
    add("ffmpeg_on_path", ff, "ffmpeg" if ff else "missing ffmpeg")
    add("recipe_built", bool(cmd) and bool(data["rows"]), f"{len(data['rows'])} beats")
    add("export_not_required", True, EXPORT_REL)
    add("no_status_bump", True, "assemble never writes packet.md")

    if not data["ready_to_assemble"] or qa["gate"] != "PASS":
        gate = "HOLD_MEDIA"
        action = "DRY_RUN"
    elif not ff:
        gate = "HOLD_FFMPEG"
        action = "DRY_RUN"
    elif export_ok:
        gate = "EXPORT_EXISTS"
        action = "DRY_RUN"
    else:
        gate = "READY_TO_ENCODE"
        action = "DRY_RUN"

    return {
        "packet": packet.name,
        "drop": selected_vo_drop(packet),
        "vo_rel": data["vo_rel"],
        "vo_on_disk": data["vo_on_disk"],
        "ready_to_assemble": data["ready_to_assemble"],
        "media_qa": qa["gate"],
        "spoken": data["spoken"],
        "export_estimate": data["export"],
        "export": EXPORT_REL,
        "export_present": export_ok,
        "ffmpeg": ff,
        "command": cmd,
        "checks": checks,
        "gate": gate,
        "action": action,
        "target": f"{TARGET_W}x{TARGET_H}@{TARGET_FPS} + {TARGET_AUDIO_HZ}Hz stereo",
    }


def render_text(report: dict) -> str:
    lines = [
        f"packet: {report['packet']}",
        f"gate: {report['gate']}",
        f"action: {report['action']}",
        f"drop: {report['drop']}",
        f"vo_on_disk: {report['vo_on_disk']} ({report['vo_rel']})",
        f"ready_to_assemble: {'yes' if report['ready_to_assemble'] else 'no'}",
        f"media_qa: {report['media_qa']}",
        f"ffmpeg: {'yes' if report['ffmpeg'] else 'no'}",
        f"export: {report['export']} present={'yes' if report['export_present'] else 'no'}",
        f"target: {report['target']}",
        "assemble never invents media, never bumps status, and default mode never runs ffmpeg",
        "repo-root vo/ is not Selected VO",
    ]
    for c in report["checks"]:
        mark = "PASS" if c["ok"] else "FAIL"
        lines.append(f"- {mark} {c['name']}: {c['detail']}")
    lines.append("ffmpeg_argv:")
    lines.append(json.dumps(report["command"], ensure_ascii=False))
    return "\n".join(lines) + "\n"


def execute(packet: Path, report: dict) -> int:
    if report["gate"] != "READY_TO_ENCODE":
        print(f"execute refused: gate={report['gate']}", file=sys.stderr)
        return 2
    dest_dir = packet / "export"
    dest_dir.mkdir(exist_ok=True)
    try:
        proc = subprocess.run(
            report["command"],
            cwd=str(packet),
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        print(f"ffmpeg launch failed: {exc}", file=sys.stderr)
        return 2
    if proc.returncode != 0:
        print(proc.stderr[-2000:] if proc.stderr else "ffmpeg failed", file=sys.stderr)
        return 2
    print(packet / EXPORT_REL)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Plan (and only then optionally run) ffmpeg assembly. Default is dry-run."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Run ffmpeg only if media_qa PASS, ready_to_assemble=yes, and ffmpeg exists",
    )
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    report = inspect_assemble(path)
    sys.stdout.write(render_text(report))
    if args.execute:
        return execute(path, report)
    if report["gate"] in {"HOLD_MEDIA"}:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
