#!/usr/bin/env python3
"""Contract for caption_gate.py. Does not call YouTube and does not encode."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "caption_gate.py"


def write_wav(path: Path, seconds: float) -> None:
    rate = 8000
    frames = int(rate * seconds)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(b"\x00\x00" * frames)


def run(packet: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), str(packet)],
        capture_output=True,
        text=True,
    )


def main() -> int:
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp)
        missing = run(packet)
        if missing.returncode != 2 or "CAPTIONS_ABSENT" not in missing.stdout:
            failures.append(f"missing srt must exit 2, got {missing.returncode} {missing.stdout}")
        (packet / "captions.srt").write_text(
            "1\n00:00:00,000 --> 00:00:01,000\nShort line.\n",
            encoding="utf-8",
        )
        good = run(packet)
        if good.returncode != 0 or "PASS" not in good.stdout:
            failures.append(f"short cue must pass, got {good.returncode} {good.stdout}")
        (packet / "captions.srt").write_text(
            "1\n00:00:00,000 --> 00:00:01,000\n"
            + ("x" * 43)
            + "\n",
            encoding="utf-8",
        )
        long = run(packet)
        if long.returncode != 1 or "CAPTION_LINE_TOO_LONG" not in long.stdout:
            failures.append(f"overlong line must exit 1, got {long.returncode} {long.stdout}")
        (packet / "captions.srt").write_text(
            "1\n00:00:00,000 --> 00:00:02,000\nOne.\n\n"
            "2\n00:00:01,000 --> 00:00:03,000\nTwo.\n",
            encoding="utf-8",
        )
        overlap = run(packet)
        if overlap.returncode != 1 or "CAPTION_OVERLAP" not in overlap.stdout:
            failures.append(f"overlap must exit 1, got {overlap.returncode} {overlap.stdout}")
        vo = packet / "vo"
        vo.mkdir()
        write_wav(vo / "take-selected.wav", 1.0)
        (packet / "captions.srt").write_text(
            "1\n00:00:00,000 --> 00:00:03,000\nPast the wav.\n",
            encoding="utf-8",
        )
        past = run(packet)
        if past.returncode != 1 or "CAPTION_PAST_WAV" not in past.stdout:
            failures.append(f"cue past wav must exit 1, got {past.returncode} {past.stdout}")
    if failures:
        print("CAPTION GATE CONTRACT FAIL")
        for item in failures:
            print(item)
        return 1
    print("CAPTION GATE CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
