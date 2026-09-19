#!/usr/bin/env python3
"""Fail-closed media QA for a video packet.

Checks Selected VO presence/header, card PNG dimensions when files exist,
and timeline assembly readiness. Never invents a pass. Never runs ffmpeg.
Never bumps packet status. Never re-implements selected_vo_drop.
"""

from __future__ import annotations

import argparse
import struct
import sys
import wave
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from render_brief import selected_vo_drop  # noqa: E402
from timeline import plan  # noqa: E402

TARGET_W = 1920
TARGET_H = 1080


def _png_size(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return int(w), int(h)


def _wav_info(path: Path) -> dict:
    info = {"ok": False, "frames": 0, "rate": 0, "channels": 0, "width": 0, "seconds": 0.0, "error": ""}
    try:
        with wave.open(str(path), "rb") as wf:
            info["frames"] = wf.getnframes()
            info["rate"] = wf.getframerate()
            info["channels"] = wf.getnchannels()
            info["width"] = wf.getsampwidth()
            if info["rate"] > 0:
                info["seconds"] = round(info["frames"] / float(info["rate"]), 2)
            info["ok"] = info["frames"] > 0 and info["rate"] > 0 and info["channels"] > 0
    except Exception as exc:  # noqa: BLE001 — fail closed on any decode issue
        info["error"] = str(exc)
    return info


def inspect_media(packet: Path) -> dict:
    data = plan(packet)
    drop = selected_vo_drop(packet)
    vo_path = packet / data["vo_rel"]
    vo_file = vo_path if vo_path.is_file() and vo_path.stat().st_size > 0 else None

    vo = {
        "drop": drop,
        "rel": data["vo_rel"],
        "present": data["vo_on_disk"] == "yes",
        "kind": vo_file.suffix.lower() if vo_file else "",
        "bytes": vo_file.stat().st_size if vo_file else 0,
        "wav": None,
    }
    if vo_file and vo_file.suffix.lower() == ".wav":
        vo["wav"] = _wav_info(vo_file)

    cards = []
    for row in data["rows"]:
        rel = row["card"]
        item = {
            "beat": row["title"],
            "rel": rel,
            "present": row["card_on_disk"] == "yes",
            "size": None,
            "ok": False,
        }
        if rel and item["present"]:
            size = _png_size(packet / rel)
            item["size"] = size
            item["ok"] = size == (TARGET_W, TARGET_H)
        cards.append(item)

    checks = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("selected_vo_present", vo["present"], vo["rel"])
    if vo["wav"] is None:
        if vo["present"] and vo["kind"] == ".flac":
            add("vo_decodable", True, "flac present; header decode not implemented (presence only)")
        elif vo["present"]:
            add("vo_decodable", False, f"unsupported or missing header for {vo['kind'] or 'unknown'}")
        else:
            add("vo_decodable", False, "no packet-relative Selected VO")
    else:
        w = vo["wav"]
        add("vo_decodable", bool(w["ok"]), w["error"] or f"{w['seconds']}s {w['rate']}Hz {w['channels']}ch")
        add("vo_nonempty", bool(w["ok"] and w["seconds"] > 0.2), f"{w['seconds']}s")

    mapped = [c for c in cards if c["rel"]]
    present = [c for c in mapped if c["present"]]
    sized = [c for c in present if c["ok"]]
    add("cards_mapped", bool(mapped), f"{len(mapped)} mapped")
    add("cards_present", bool(mapped) and len(present) == len(mapped), f"{len(present)}/{len(mapped)}")
    add(
        "cards_1920x1080",
        bool(present) and len(sized) == len(present),
        f"{len(sized)}/{len(present)} correct size",
    )
    add("ready_to_assemble", bool(data["ready_to_assemble"]), "timeline gate")
    add("no_export_claimed", True, "media_qa does not treat a named export as a master")

    hard = [c for c in checks if c["name"] in {"selected_vo_present", "vo_decodable", "cards_present", "cards_1920x1080", "ready_to_assemble"}]
    gate = "PASS" if hard and all(c["ok"] for c in hard) else "FAIL"
    return {
        "packet": packet.name,
        "drop": drop,
        "vo": vo,
        "cards": cards,
        "checks": checks,
        "gate": gate,
        "spoken": data["spoken"],
        "export": data["export"],
        "ready_to_assemble": data["ready_to_assemble"],
    }


def render_text(report: dict) -> str:
    lines = [
        f"packet: {report['packet']}",
        f"gate: {report['gate']}",
        f"drop: {report['drop']}",
        f"ready_to_assemble: {'yes' if report['ready_to_assemble'] else 'no'}",
        "repo-root vo/ is not Selected VO",
        "media_qa never runs ffmpeg and never bumps status",
    ]
    for c in report["checks"]:
        mark = "PASS" if c["ok"] else "FAIL"
        lines.append(f"- {mark} {c['name']}: {c['detail']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed media QA. No ffmpeg. No status bump.")
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    report = inspect_media(path)
    sys.stdout.write(render_text(report))
    return 0 if report["gate"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
