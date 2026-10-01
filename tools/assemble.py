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

from media_qa import inspect_media, mp4_header_ok  # noqa: E402
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
        # pad_dur is required. Bare apad never signals EOF, so -shortest hangs
        # (observed Run 251). pad_dur=END_SCREEN keeps the end card; -shortest
        # then stops if video is the shorter stream. Run 249 master was 308.40s
        # and dropped this +20s because it mapped raw audio with -shortest.
        filter_complex += (
            f";{labels}concat=n={n}:v=1:a=0[vout];"
            f"[0:a]apad=pad_dur={END_SCREEN:.0f}[aout]"
        )
    args += [
        "-filter_complex",
        filter_complex,
        "-map",
        "[vout]",
        "-map",
        "[aout]",
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
    export_ok = export.is_file() and export.stat().st_size > 0 and mp4_header_ok(export)

    checks = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("ready_to_assemble", bool(data["ready_to_assemble"]), "timeline gate")
    add("media_qa_pass", qa["gate"] == "PASS", qa["gate"])
    add("ffmpeg_on_path", ff, "ffmpeg" if ff else "missing ffmpeg")
    add("recipe_built", bool(cmd) and bool(data["rows"]), f"{len(data['rows'])} beats")
    add("export_header", export_ok or not export.exists(), EXPORT_REL)
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
        "execute encodes one card at a time so a 2GB machine is not killed by the single graph",
        "end screen is kept: audio is apadded, then -shortest stops on the video",
        "execute refuses a muxed file that lacks ftyp/moov",
        "repo-root vo/ is not Selected VO",
    ]
    for c in report["checks"]:
        mark = "PASS" if c["ok"] else "FAIL"
        lines.append(f"- {mark} {c['name']}: {c['detail']}")
    lines.append("ffmpeg_argv:")
    lines.append("do_not_copy_on_2gb: single-graph argv OOMs; use assemble.py --execute (one card at a time)")
    lines.append(json.dumps(report["command"], ensure_ascii=False))
    return "\n".join(lines) + "\n"


def _run(cmd: list[str], cwd: Path) -> int:
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), check=False, capture_output=True, text=True)
    except OSError as exc:
        print(f"ffmpeg launch failed: {exc}", file=sys.stderr)
        return 2
    if proc.returncode != 0:
        err = proc.stderr or proc.stdout or "ffmpeg failed"
        print(err[-2000:], file=sys.stderr)
        return 2
    return 0


def execute(packet: Path, report: dict) -> int:
    """Encode one card at a time, then concat.

    The printed single-graph argv is the operator recipe. Running that graph
    holds every 1080p input at once and was killed on a 2 GB machine (Run 249).
    Segmented execute keeps the same card order and durations.
    After mux, require mp4_header_ok. A killed ffmpeg can leave ftyp without
    moov (Run 249 single-graph; Run 252 sandbox mux). That file is not a master.
    """
    if report["gate"] != "READY_TO_ENCODE":
        print(f"execute refused: gate={report['gate']}", file=sys.stderr)
        return 2
    from timeline import plan

    data = plan(packet)
    rows = [r for r in data["rows"] if r.get("card")]
    if not rows:
        print("execute refused: no card rows", file=sys.stderr)
        return 2
    dest_dir = packet / "export"
    dest_dir.mkdir(exist_ok=True)
    work = dest_dir / ".segments"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    seg_paths = []
    for i, row in enumerate(rows):
        seg = work / f"seg{i:02d}.mp4"
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-t", f"{float(row['dur']):.1f}",
            "-i", row["card"],
            "-f", "lavfi", "-t", f"{float(row['dur']):.1f}", "-i", "anullsrc=r=48000:cl=stereo",
            "-vf", "scale=1920:1080,fps=30,format=yuv420p",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", "30",
            "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(seg),
        ]
        if _run(cmd, packet) != 0:
            return 2
        seg_paths.append(seg)
    # End screen holds the last card. Matches the dry-run recipe.
    end = work / "seg_end.mp4"
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-t", f"{END_SCREEN:.1f}", "-i", rows[-1]["card"],
        "-f", "lavfi", "-t", f"{END_SCREEN:.1f}", "-i", "anullsrc=r=48000:cl=stereo",
        "-vf", "scale=1920:1080,fps=30,format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", "30",
        "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(end),
    ]
    if _run(cmd, packet) != 0:
        return 2
    seg_paths.append(end)
    lst = work / "list.txt"
    lst.write_text("".join(f"file '{s.name}'\n" for s in seg_paths), encoding="utf-8")
    silent = work / "silent.mp4"
    if _run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", str(silent.name)], work) != 0:
        return 2
    drop = str((packet / "vo" / Path(report.get("drop") or "").name).resolve())
    dest = packet / EXPORT_REL
    # apad + -shortest: silence fills the end screen; output length follows video.
    mux = [
        "ffmpeg", "-y", "-i", str(silent), "-i", drop,
        "-filter_complex", f"[1:a]apad=pad_dur={END_SCREEN:.0f}[a]",
        "-map", "0:v:0", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-ar", "48000", "-ac", "2",
        "-shortest", "-movflags", "+faststart", str(dest),
    ]
    if _run(mux, packet) != 0:
        print("execute refused: mux failed; leaving export/.segments", file=sys.stderr)
        return 2
    if not dest.is_file() or dest.stat().st_size <= 0 or not mp4_header_ok(dest):
        print("execute refused: master missing ftyp/moov; leaving export/.segments", file=sys.stderr)
        return 2
    shutil.rmtree(work, ignore_errors=True)
    print(dest)
    print("execute: segmented (one card at a time); dry-run argv is the single-graph recipe")
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
