#!/usr/bin/env python3
"""Fail-closed completion gate.

A packet is not complete because markdown exists. This printer answers
whether evidence exists for media, export, publish, feedback, and a
non-invented experiment result.

Never invents a wav, master, video ID, metrics, or keep/discard.
Never calls ffmpeg or YouTube APIs.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from assemble import inspect_assemble  # noqa: E402
from experiment_loop import inspect_experiment  # noqa: E402
from media_qa import inspect_media, mp4_header_ok  # noqa: E402
from render_brief import selected_vo_drop  # noqa: E402
from youtube_feedback import collected_metrics, inspect_feedback, load_upload_state, provider_video_id  # noqa: E402


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _check_ok(report: dict, name: str) -> bool:
    for c in report.get("checks") or []:
        if c.get("name") == name:
            return bool(c.get("ok"))
    return False


def inspect_complete(
    packet: Path,
    env: dict[str, str] | None = None,
    now: datetime | None = None,
) -> dict:
    media = inspect_media(packet)
    assemble = inspect_assemble(packet)
    feedback = inspect_feedback(packet, env=env, now=now)
    experiment = inspect_experiment(packet, env=env, now=now)
    upload = load_upload_state(packet)
    video_id = provider_video_id(upload)
    export_path = packet / "export" / "master.mp4"
    export_present = export_path.is_file() and export_path.stat().st_size > 0 and mp4_header_ok(export_path)

    vo_present = _check_ok(media, "selected_vo_present")
    cards_ok = _check_ok(media, "cards_present") or _check_ok(media, "all_cards_present")
    ready = bool(media.get("ready_to_assemble") or assemble.get("ready_to_assemble"))
    metrics, metrics_detail = collected_metrics(packet, video_id)
    result = (experiment.get("record") or {}).get("result")

    checks = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("selected_vo_present", vo_present, selected_vo_drop(packet))
    add("cards_present", cards_ok, "planned cards are not completed cards")
    add("ready_to_assemble", ready, "timeline/media_qa must both be ready")
    add("master_export_present", export_present, str(export_path))
    add("provider_video_id_present", bool(video_id), video_id or "no provider_video_id")
    add("metrics_present", metrics is not None, metrics_detail)
    add("experiment_result_present", result is not None, "pending is not a keep/discard")
    add("no_invented_completion", True, "COMPLETE requires every evidence row")

    if not vo_present or not cards_ok or not ready:
        gate = "INCOMPLETE_MEDIA"
        action = "HOLD_MEDIA"
    elif not export_present:
        gate = "INCOMPLETE_EXPORT"
        action = "HOLD_ENCODE"
    elif not video_id:
        gate = "INCOMPLETE_PUBLISH"
        action = "HOLD_UNPUBLISHED"
    elif metrics is None:
        gate = "INCOMPLETE_FEEDBACK"
        action = "HOLD_NO_EVIDENCE"
    elif result is None:
        gate = "INCOMPLETE_LEARNING"
        action = "HOLD_NO_RESULT"
    else:
        gate = "COMPLETE"
        action = "NONE"

    return {
        "packet": packet.name,
        "drop": selected_vo_drop(packet),
        "media_gate": media.get("gate"),
        "assemble_gate": assemble.get("gate"),
        "feedback_gate": feedback.get("gate"),
        "experiment_gate": experiment.get("gate"),
        "provider_video_id": video_id,
        "metrics": metrics,
        "experiment_result": result,
        "export": str(export_path),
        "checks": checks,
        "gate": gate,
        "action": action,
        "generated": _fmt(now or _now()),
    }


def render_text(report: dict) -> str:
    lines = [
        f"packet: {report['packet']}",
        f"gate: {report['gate']}",
        f"action: {report['action']}",
        f"drop: {report['drop']}",
        f"media_gate: {report['media_gate']}",
        f"assemble_gate: {report['assemble_gate']}",
        f"feedback_gate: {report['feedback_gate']}",
        f"experiment_gate: {report['experiment_gate']}",
        f"provider_video_id: {report['provider_video_id'] or 'none'}",
        f"export: {report['export']}",
        "complete.py never invents media, uploads, metrics, or experiment results",
        "markdown-only packets stay INCOMPLETE_*",
    ]
    for c in report["checks"]:
        mark = "PASS" if c["ok"] else "FAIL"
        lines.append(f"- {mark} {c['name']}: {c['detail']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed completion gate. No writes. No APIs."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    report = inspect_complete(path)
    sys.stdout.write(render_text(report))
    if report["gate"] == "COMPLETE":
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
