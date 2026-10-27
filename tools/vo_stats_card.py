#!/usr/bin/env python3
"""Generate a local audio stats card PNG from the selected VO WAV.

Computes duration, approximate peak dBFS, RMS dBFS, silence ratio, and clipping flag
using only stdlib wave. Renders a glanceable 640x360 PNG. No invented audio.
Output stays local and gitignored. Reduces recurring human labor of running media_qa
or inspecting WAV headers just to confirm basic audio health on every future packet.
"""

from __future__ import annotations

import argparse
import math
import sys
import wave
from pathlib import Path

WIDTH, HEIGHT = 640, 360
BG = (18, 18, 22)
FG = (232, 196, 104)
MUTED = (120, 116, 110)
LINE = (58, 56, 52)
GOOD = (90, 180, 110)
WARN = (220, 160, 60)
BAD = (200, 80, 80)


def find_selected_vo(packet: Path) -> Path | None:
    vo_dir = packet / "vo"
    if not vo_dir.is_dir():
        return None
    for pattern in ("*-take-selected.wav", "*-take-selected.flac"):
        matches = list(vo_dir.glob(pattern))
        if matches:
            return matches[0]
    wavs = list(vo_dir.glob("*.wav"))
    return wavs[0] if wavs else None


def analyze_wav(path: Path) -> dict | None:
    try:
        with wave.open(str(path), "rb") as wf:
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            if n_frames == 0 or framerate == 0 or sampwidth != 2:
                return None
            duration = n_frames / framerate
            raw = wf.readframes(n_frames)
            # treat as mono or first channel, 16-bit signed
            samples = []
            bytes_per_frame = n_channels * sampwidth
            for i in range(0, len(raw) - sampwidth + 1, bytes_per_frame):
                val = int.from_bytes(raw[i : i + 2], "little", signed=True)
                samples.append(val / 32768.0)
            if not samples:
                return None
            peak = max(abs(s) for s in samples)
            rms = math.sqrt(sum(s * s for s in samples) / len(samples))
            # silence: abs < 0.01 (~-40dB)
            silence_count = sum(1 for s in samples if abs(s) < 0.01)
            silence_ratio = silence_count / len(samples)
            # clipping: near full scale
            clip_count = sum(1 for s in samples if abs(s) > 0.99)
            peak_db = 20 * math.log10(peak) if peak > 0 else -120
            rms_db = 20 * math.log10(rms) if rms > 0 else -120
            return {
                "duration": duration,
                "peak_db": peak_db,
                "rms_db": rms_db,
                "silence_ratio": silence_ratio,
                "clip_count": clip_count,
                "n_samples": len(samples),
                "framerate": framerate,
            }
    except Exception:
        return None


def _pil():
    from PIL import Image, ImageDraw, ImageFont
    return Image, ImageDraw, ImageFont


def _font(size: int):
    _, _, ImageFont = _pil()
    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    )
    for p in candidates:
        if Path(p).is_file():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def render_card(stats: dict, title: str) -> object:
    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, WIDTH - 1, HEIGHT - 1), outline=LINE, width=2)
    draw.text((16, 12), "VO Stats Card", font=_font(22), fill=FG)
    draw.text((16, 40), title[:50], font=_font(14), fill=MUTED)

    y = 80
    lines = [
        f"Duration:     {stats['duration']:.1f} s",
        f"Peak:         {stats['peak_db']:.1f} dBFS",
        f"RMS:          {stats['rms_db']:.1f} dBFS",
        f"Silence:      {stats['silence_ratio']*100:.1f} %",
        f"Clips:        {stats['clip_count']} samples",
        f"Rate:         {stats['framerate']} Hz",
    ]
    for line in lines:
        draw.text((24, y), line, font=_font(18), fill=FG)
        y += 32

    # simple status
    status = "OK"
    status_color = GOOD
    if stats["clip_count"] > 10:
        status = "CLIPPING"
        status_color = BAD
    elif stats["silence_ratio"] > 0.4:
        status = "HIGH SILENCE"
        status_color = WARN
    elif stats["peak_db"] > -1:
        status = "HOT"
        status_color = WARN
    elif stats["duration"] < 30:
        status = "SHORT"
        status_color = WARN

    draw.text((24, y + 10), f"Status: {status}", font=_font(20), fill=status_color)
    draw.text((16, HEIGHT - 28), "local stats card (gitignored) | no invented data", font=_font(12), fill=MUTED)
    return img


def main() -> int:
    p = argparse.ArgumentParser(description="Generate local VO stats card PNG")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    vo = find_selected_vo(packet)
    if vo is None:
        print("no selected VO found (looked for vo/*-take-selected.wav)")
        return 1

    print(f"vo: {vo.name}")
    stats = analyze_wav(vo)
    if stats is None:
        print("could not analyze (unsupported format, empty, or not 16-bit WAV)", file=sys.stderr)
        return 1

    img = render_card(stats, packet.name)
    out = packet / "vo_stats_card.png"
    img.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print(f"duration: {stats['duration']:.1f}s  peak: {stats['peak_db']:.1f}dB  rms: {stats['rms_db']:.1f}dB  silence: {stats['silence_ratio']*100:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
