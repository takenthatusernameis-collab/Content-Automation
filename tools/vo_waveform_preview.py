#!/usr/bin/env python3
"""Generate a local waveform preview PNG from the selected VO WAV.

If videos/NNN-slug/vo/*-take-selected.wav (or .flac note) exists, read it with stdlib wave
and render a simple amplitude overview PNG. No invented audio. Output stays local and gitignored.
Reduces recurring human labor of opening the audio file just to confirm presence, duration,
and rough envelope on every future packet. One command produces a glanceable review image.
"""

from __future__ import annotations

import argparse
import sys
import wave
from pathlib import Path

WIDTH, HEIGHT = 1280, 360
BG = (18, 18, 22)
FG = (232, 196, 104)
MUTED = (120, 116, 110)
LINE = (58, 56, 52)


def find_selected_vo(packet: Path) -> Path | None:
    vo_dir = packet / "vo"
    if not vo_dir.is_dir():
        return None
    for pattern in ("*-take-selected.wav", "*-take-selected.flac"):
        matches = list(vo_dir.glob(pattern))
        if matches:
            return matches[0]
    # fallback any wav
    wavs = list(vo_dir.glob("*.wav"))
    return wavs[0] if wavs else None


def read_peaks(path: Path, n_bins: int = 200) -> tuple[list[float], float] | None:
    """Return (normalized peak per bin, duration_seconds) or None."""
    try:
        with wave.open(str(path), "rb") as wf:
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            if n_frames == 0 or framerate == 0:
                return None
            duration = n_frames / framerate
            raw = wf.readframes(n_frames)
            # simple 16-bit mono or first channel peak
            if sampwidth != 2:
                return None  # only handle 16-bit for now
            samples = []
            step = max(1, n_frames // n_bins)
            for i in range(0, n_frames, step):
                frame_start = i * n_channels * sampwidth
                if frame_start + sampwidth > len(raw):
                    break
                # little-endian signed 16-bit
                val = int.from_bytes(raw[frame_start : frame_start + 2], "little", signed=True)
                samples.append(abs(val) / 32768.0)
            if not samples:
                return None
            # downsample to exactly n_bins by max-pooling
            peaks = []
            bin_size = max(1, len(samples) // n_bins)
            for b in range(n_bins):
                chunk = samples[b * bin_size : (b + 1) * bin_size]
                peaks.append(max(chunk) if chunk else 0.0)
            return peaks, duration
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


def render_waveform(peaks: list[float], duration: float, title: str) -> object:
    Image, ImageDraw, _ = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, WIDTH - 1, HEIGHT - 1), outline=LINE, width=2)
    draw.text((16, 12), title[:80], font=_font(18), fill=MUTED)
    draw.text((16, HEIGHT - 28), f"{duration:.1f}s  |  local waveform preview (gitignored)", font=_font(14), fill=MUTED)

    if not peaks:
        return img
    mid = HEIGHT // 2
    max_h = (HEIGHT // 2) - 40
    x_step = (WIDTH - 40) / len(peaks)
    for i, p in enumerate(peaks):
        h = int(p * max_h)
        x = 20 + int(i * x_step)
        draw.line((x, mid - h, x, mid + h), fill=FG, width=2)
    # center line
    draw.line((20, mid, WIDTH - 20, mid), fill=LINE, width=1)
    return img


def main() -> int:
    p = argparse.ArgumentParser(description="Generate local waveform PNG from selected VO")
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
    result = read_peaks(vo)
    if result is None:
        print("could not read peaks (unsupported format or empty)", file=sys.stderr)
        return 1

    peaks, duration = result
    img = render_waveform(peaks, duration, packet.name)
    out = packet / "vo_waveform_preview.png"
    img.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print(f"duration: {duration:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
