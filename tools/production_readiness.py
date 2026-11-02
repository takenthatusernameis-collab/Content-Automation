#!/usr/bin/env python3
"""Single-command local production readiness aggregator.

Imports and runs media_qa.inspect_media + assemble.inspect_assemble.
Notes captions.srt, thumbnail.png presence + basic PNG dimensions (stdlib),
VO duration when a WAV is present, mapped/present card counts, script.md presence,
spoken/export estimates from timeline, publish.md / timeline.md presence,
and caption CPS stats (avg/max/min + flagged fast/slow count) via caption_speed_report.
Prints a compact summary. Never invents media, never runs ffmpeg, never bumps status,
never polls secrets, never dispatches. Exit 0 only when media_qa PASS and assemble
gate is READY_TO_ENCODE or EXPORT_EXISTS.
"""

from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from media_qa import inspect_media  # noqa: E402
from assemble import inspect_assemble  # noqa: E402
from caption_speed_report import inspect_speed  # noqa: E402


def _png_size(path: Path) -> tuple[int, int] | None:
    """Return (width, height) for a PNG or None. Stdlib only."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return int(w), int(h)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate local media/QA/assembly readiness. No ffmpeg execute, no secrets."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    media = inspect_media(path)
    assemble_rep = inspect_assemble(path)
    captions = (path / "captions.srt").is_file()
    speed = inspect_speed(path)
    thumb = path / "thumbnail.png"
    thumb_present = thumb.is_file()
    thumb_size = _png_size(thumb) if thumb_present else None
    thumb_ok = thumb_size == (1280, 720) if thumb_size else False
    script_present = (path / "script.md").is_file()
    publish_present = (path / "publish.md").is_file()
    timeline_present = (path / "timeline.md").is_file()

    vo_seconds = None
    vo = media.get("vo") or {}
    wav = vo.get("wav") or {}
    if wav.get("ok") and wav.get("seconds"):
        vo_seconds = wav["seconds"]

    cards = media.get("cards") or []
    mapped = [c for c in cards if c.get("rel")]
    present_cards = [c for c in mapped if c.get("present")]
    ok_cards = [c for c in present_cards if c.get("ok")]

    spoken_est = media.get("spoken")
    export_est = assemble_rep.get("export_estimate")

    print(f"packet: {path.name}")
    print(f"media_qa: {media['gate']}")
    print(f"assemble_gate: {assemble_rep['gate']}")
    print(f"ready_to_assemble: {'yes' if media.get('ready_to_assemble') else 'no'}")
    print(f"export_present: {'yes' if media.get('export_present') else 'no'}")
    print(f"captions_srt: {'present' if captions else 'missing'}")
    if speed.get("ok"):
        print(f"caption_cues: {speed['cues']}")
        print(f"caption_avg_cps: {speed['avg_cps']}")
        print(f"caption_max_cps: {speed['max_cps']}")
        print(f"caption_min_cps: {speed['min_cps']}")
        print(f"caption_flagged: {len(speed['flagged'])}")
    else:
        print(f"caption_speed: {speed['code']}")
    print(f"thumbnail.png: {'present' if thumb_present else 'missing'}")
    if thumb_size:
        print(f"thumbnail_size: {thumb_size[0]}x{thumb_size[1]} {'(preferred 1280x720)' if thumb_ok else '(non-standard)'}")
    else:
        print("thumbnail_size: n/a")
    print(f"script.md: {'present' if script_present else 'missing'}")
    print(f"publish.md: {'present' if publish_present else 'missing'}")
    print(f"timeline.md: {'present' if timeline_present else 'missing'}")
    if vo_seconds is not None:
        print(f"vo_duration_s: {vo_seconds}")
    else:
        print("vo_duration_s: n/a")
    print(f"spoken_estimate_s: {spoken_est if spoken_est is not None else 'n/a'}")
    print(f"export_estimate_s: {export_est if export_est is not None else 'n/a'}")
    print(f"cards: {len(ok_cards)}/{len(present_cards)} ok of {len(mapped)} mapped")
    print(f"ffmpeg_on_path: {'yes' if assemble_rep.get('ffmpeg') else 'no'}")

    hard_ok = media["gate"] == "PASS" and assemble_rep["gate"] in {"READY_TO_ENCODE", "EXPORT_EXISTS"}
    print(f"local_ready_for_human_dispatch: {'yes' if hard_ok else 'no'}")
    print("Does not execute encode, does not invent media, does not poll OAuth.")
    return 0 if hard_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
