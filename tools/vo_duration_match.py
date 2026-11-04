#!/usr/bin/env python3
"""Soft VO duration match report for a packet.

Compares estimated spoken duration from script/draft WORDS (150 wpm)
against actual Selected VO WAV duration when present.
Prints delta and a soft note. Never fails the gate. Never runs ffmpeg.
Never invents media. Never bumps status.
"""

from __future__ import annotations

import argparse
import sys
import wave
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from render_brief import selected_vo_drop  # noqa: E402
from timeline import plan  # noqa: E402

try:
    from words import all_spoken_words, spoken_seconds, fmt_mmss  # type: ignore
except ImportError:
    # Fallback minimal if import fails
    def all_spoken_words(script: str) -> list[str]:
        return []
    def spoken_seconds(n: int) -> float:
        return (n / 150.0) * 60.0
    def fmt_mmss(seconds: float) -> str:
        whole = int(round(max(0, seconds)))
        m, s = divmod(whole, 60)
        return f"{m:02d}:{s:02d}"


def wav_seconds(path: Path) -> float | None:
    try:
        with wave.open(str(path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            if rate > 0 and frames > 0:
                return frames / float(rate)
    except Exception:
        return None
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Soft report: script estimated duration vs Selected VO WAV duration. No gate change."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    data = plan(path)
    drop = selected_vo_drop(path)
    vo_path = path / data["vo_rel"]
    vo_file = vo_path if vo_path.is_file() and vo_path.stat().st_size > 0 else None

    # Prefer draft.md then script.md for word count
    draft = path / "draft.md"
    script = path / "script.md"
    source = draft if draft.is_file() else script if script.is_file() else None
    n_words = 0
    est_s = 0.0
    if source:
        try:
            text = source.read_text(encoding="utf-8")
            n_words = len(all_spoken_words(text))
            est_s = spoken_seconds(n_words)
        except Exception:
            n_words = 0

    print("VO DURATION MATCH (soft report only)")
    print(f"packet: {path.name}")
    print(f"drop: {drop}")
    print(f"script_source: {source.name if source else 'none'}")
    print(f"spoken_words: {n_words}")
    print(f"estimated_duration: {fmt_mmss(est_s)} ({est_s:.1f}s at 150 wpm)")
    if vo_file and vo_file.suffix.lower() == ".wav":
        actual = wav_seconds(vo_file)
        if actual is not None:
            delta = actual - est_s
            print(f"actual_vo_seconds: {actual:.1f}")
            print(f"delta_seconds: {delta:+.1f} (actual - estimated)")
            if abs(delta) < 15:
                print("match: close (within 15s; soft ok)")
            elif delta > 0:
                print("match: VO longer than script estimate (soft; check pacing or silence)")
            else:
                print("match: VO shorter than script estimate (soft; check cuts or missing beats)")
        else:
            print("actual_vo_seconds: unavailable (decode failed)")
    else:
        print("actual_vo: no packet-relative Selected VO WAV")
        print("note: materialize or record first; this tool does not invent media")
    print("This command writes nothing. Soft report only. Does not change media_qa gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
