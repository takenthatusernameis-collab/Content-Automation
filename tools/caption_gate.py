#!/usr/bin/env python3
"""Fail closed on a present captions.srt that captions.insert would still accept.

Does not rewrite captions. Does not call YouTube. Does not encode.
A missing captions.srt exits 2 so a non-Q1 dry-run can continue.
A present file with an empty cue, an overlap, a reversed cue, a line over
42 characters, or a cue that ends after the selected wav exits 1.
"""

from __future__ import annotations

import argparse
import re
import sys
import wave
from pathlib import Path

MAX_LINE = 42
WAV_SLACK_S = 1.0
CUE_RE = re.compile(
    r"(\d+)\s*\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s*\n(.*?)(?=\n\n|\Z)",
    re.S,
)


def _seconds(stamp: str) -> float:
    h, m, rest = stamp.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def wav_duration(path: Path) -> float | None:
    try:
        with wave.open(str(path), "rb") as handle:
            rate = handle.getframerate()
            if rate <= 0:
                return None
            return handle.getnframes() / float(rate)
    except (wave.Error, OSError):
        return None


def selected_wav(packet: Path) -> Path | None:
    folder = packet / "vo"
    if not folder.is_dir():
        return None
    found = sorted(folder.glob("*take-selected.wav"))
    return found[0] if found else None


def inspect_captions(packet: Path) -> dict:
    path = packet / "captions.srt"
    if not path.is_file():
        return {"ok": False, "code": "CAPTIONS_ABSENT", "detail": str(path), "cues": 0}
    text = path.read_text(encoding="utf-8")
    cues = []
    for match in CUE_RE.finditer(text.strip() + "\n"):
        body = match.group(4).strip("\n")
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        cues.append(
            {
                "index": int(match.group(1)),
                "start": _seconds(match.group(2)),
                "end": _seconds(match.group(3)),
                "lines": lines,
            }
        )
    if not cues:
        return {"ok": False, "code": "CAPTIONS_UNPARSEABLE", "detail": path.name, "cues": 0}
    prev_end = -1.0
    for cue in cues:
        if cue["end"] <= cue["start"]:
            return {
                "ok": False,
                "code": "CAPTION_REVERSED",
                "detail": f"cue {cue['index']}",
                "cues": len(cues),
            }
        if not cue["lines"]:
            return {
                "ok": False,
                "code": "CAPTION_EMPTY",
                "detail": f"cue {cue['index']}",
                "cues": len(cues),
            }
        for line in cue["lines"]:
            if len(line) > MAX_LINE:
                return {
                    "ok": False,
                    "code": "CAPTION_LINE_TOO_LONG",
                    "detail": f"cue {cue['index']} {len(line)}>{MAX_LINE}",
                    "cues": len(cues),
                }
        if cue["start"] < prev_end - 0.001:
            return {
                "ok": False,
                "code": "CAPTION_OVERLAP",
                "detail": f"cue {cue['index']}",
                "cues": len(cues),
            }
        prev_end = cue["end"]
    wav = selected_wav(packet)
    if wav is not None:
        duration = wav_duration(wav)
        if duration is None:
            return {
                "ok": False,
                "code": "CAPTION_WAV_UNREADABLE",
                "detail": wav.name,
                "cues": len(cues),
            }
        if cues[-1]["end"] > duration + WAV_SLACK_S:
            return {
                "ok": False,
                "code": "CAPTION_PAST_WAV",
                "detail": f"{cues[-1]['end']:.3f}>{duration + WAV_SLACK_S:.3f}",
                "cues": len(cues),
            }
    return {"ok": True, "code": "PASS", "detail": f"{len(cues)} cues", "cues": len(cues)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail closed on a bad captions.srt.")
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    report = inspect_captions(args.packet)
    print("CAPTION_GATE")
    print(f"code: {report['code']}")
    print(f"detail: {report['detail']}")
    print(f"cues: {report['cues']}")
    if report["ok"]:
        return 0
    if report["code"] == "CAPTIONS_ABSENT":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
