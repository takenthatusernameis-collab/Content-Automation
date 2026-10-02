#!/usr/bin/env python3
"""Draft captions.srt from script WORDS placed on Selected VO speech time.

Not Whisper and not an upload. Speech intervals come from PCM RMS gaps in the
packet DROP wav. Script words are laid across that speech clock in order, then
grouped into short cues. A missing wav refuses. An existing srt refuses unless
--force. This does not check any human approval box.
"""

from __future__ import annotations

import argparse
import math
import struct
import sys
import wave
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from caption_brief import script_cues  # noqa: E402
from render_brief import selected_vo_drop  # noqa: E402

WIN_S = 0.02
MERGE_GAP_S = 0.12
MIN_SPEECH_S = 0.08
MAX_CUE_WORDS = 12
MAX_CUE_CHARS = 84
MAX_CUE_S = 5.5
MIN_BREAK_WORDS = 5


def _rms_windows(path: Path) -> tuple[int, list[float], float]:
    with wave.open(str(path), "rb") as handle:
        rate = handle.getframerate()
        channels = handle.getnchannels()
        width = handle.getsampwidth()
        frames = handle.getnframes()
        if width != 2 or channels != 1:
            raise ValueError(f"need mono s16 wav, got channels={channels} width={width}")
        raw = handle.readframes(frames)
    samples = struct.unpack("<" + str(len(raw) // 2) + "h", raw)
    win = max(1, int(rate * WIN_S))
    peak = max(abs(s) for s in samples) if samples else 0
    windows: list[float] = []
    for i in range(0, len(samples), win):
        chunk = samples[i : i + win]
        if not chunk:
            continue
        windows.append(math.sqrt(sum(v * v for v in chunk) / len(chunk)))
    return rate, windows, peak / 32768.0


def speech_intervals(path: Path) -> tuple[float, list[tuple[float, float]]]:
    _rate, windows, peak = _rms_windows(path)
    if not windows or peak <= 0:
        return 0.0, []
    thresh = max(400.0, 0.04 * peak * 32768.0)
    raw: list[tuple[float, float]] = []
    start = None
    for i, rms in enumerate(windows):
        t = i * WIN_S
        if rms >= thresh:
            if start is None:
                start = t
        elif start is not None:
            raw.append((start, t))
            start = None
    if start is not None:
        raw.append((start, len(windows) * WIN_S))
    merged: list[tuple[float, float]] = []
    for begin, end in raw:
        if merged and begin - merged[-1][1] <= MERGE_GAP_S:
            merged[-1] = (merged[-1][0], end)
        else:
            merged.append((begin, end))
    speech = [(a, b) for a, b in merged if b - a >= MIN_SPEECH_S]
    duration = len(windows) * WIN_S
    return duration, speech


def _words(script: str) -> list[str]:
    words: list[str] = []
    for cue in script_cues(script):
        text = str(cue["text"])
        words.extend(text.split())
    return words


def _speech_clock(intervals: list[tuple[float, float]]) -> list[tuple[float, float, float]]:
    """Return (wall_start, wall_end, speech_offset_at_start)."""
    clock = []
    offset = 0.0
    for begin, end in intervals:
        clock.append((begin, end, offset))
        offset += end - begin
    return clock


def wall_time(speech_t: float, clock: list[tuple[float, float, float]]) -> float:
    for begin, end, offset in clock:
        span = end - begin
        if speech_t <= offset + span:
            return begin + max(0.0, speech_t - offset)
    if not clock:
        return 0.0
    return clock[-1][1]


def assign(words: list[str], intervals: list[tuple[float, float]]) -> list[tuple[str, float, float]]:
    clock = _speech_clock(intervals)
    total = sum(end - begin for begin, end in intervals)
    if not words or total <= 0:
        return []
    step = total / len(words)
    placed = []
    for i, word in enumerate(words):
        start = wall_time(i * step, clock)
        end = wall_time((i + 1) * step, clock)
        if end <= start:
            end = start + 0.05
        placed.append((word, start, end))
    return placed


def wrap_cue(words: list[str]) -> str:
    line = " ".join(words)
    if len(line) <= 42:
        return line
    best = 1
    best_score = 10**9
    for i in range(1, len(words)):
        left = " ".join(words[:i])
        right = " ".join(words[i:])
        score = abs(len(left) - len(right)) + (0 if len(left) <= 42 and len(right) <= 42 else 100)
        if score < best_score:
            best_score = score
            best = i
    return " ".join(words[:best]) + "\n" + " ".join(words[best:])


def group(placed: list[tuple[str, float, float]]) -> list[dict]:
    cues: list[dict] = []
    buf: list[tuple[str, float, float]] = []

    def flush() -> None:
        if not buf:
            return
        words = [w for w, _, _ in buf]
        cues.append({"start": buf[0][1], "end": buf[-1][2], "text": wrap_cue(words)})
        buf.clear()

    for item in placed:
        word, _start, end = item
        trial_words = [w for w, _, _ in buf] + [word]
        trial = " ".join(trial_words)
        dur = end - (buf[0][1] if buf else item[1])
        too_long = (
            len(trial_words) > MAX_CUE_WORDS
            or len(trial) > MAX_CUE_CHARS
            or dur > MAX_CUE_S
        )
        if buf and too_long:
            flush()
        buf.append(item)
        if word.endswith((".", "!", "?")) and len(buf) >= MIN_BREAK_WORDS:
            flush()
    flush()
    return cues


def srt_ts(seconds: float) -> str:
    if seconds < 0:
        seconds = 0.0
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def render_srt(cues: list[dict]) -> str:
    lines = [
        "NOTE draft silence-proportional alignment; not ASR; not approved for upload",
    ]
    # NOTE lines are not valid SRT. Keep the warning out of the cue file and
    # return only cues. Callers print the method.
    lines = []
    for i, cue in enumerate(cues, start=1):
        lines.append(str(i))
        lines.append(f"{srt_ts(float(cue['start']))} --> {srt_ts(float(cue['end']))}")
        lines.append(str(cue["text"]))
        lines.append("")
    return "\n".join(lines)


def resolve_drop(packet: Path) -> tuple[Path, str]:
    rel = selected_vo_drop(packet)
    local = packet / "vo" / Path(rel).name
    if local.is_file():
        return local, rel
    root = Path(__file__).resolve().parents[1]
    repo = root / rel
    if repo.is_file():
        return repo, rel
    raise FileNotFoundError(f"REFUSE missing Selected VO: {rel}")


def build(packet: Path) -> tuple[str, dict]:
    drop, rel = resolve_drop(packet)
    script_path = packet / "script.md"
    if not script_path.is_file():
        raise FileNotFoundError(f"REFUSE missing script.md: {packet}")
    words = _words(script_path.read_text(encoding="utf-8"))
    if not words:
        raise ValueError("REFUSE script WORDS empty")
    duration, intervals = speech_intervals(drop)
    if not intervals:
        raise ValueError("REFUSE no speech intervals in wav")
    placed = assign(words, intervals)
    cues = group(placed)
    info = {
        "duration": round(duration, 2),
        "speech_s": round(sum(b - a for a, b in intervals), 2),
        "intervals": len(intervals),
        "words": len(words),
        "cues": len(cues),
        "method": "silence-proportional",
        "drop": rel,
    }
    return render_srt(cues), info


def main() -> int:
    parser = argparse.ArgumentParser(description="Draft captions.srt from Selected VO speech time.")
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true", help="Print SRT; do not write")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing captions.srt")
    args = parser.parse_args()
    packet = Path(args.packet).resolve()
    if not packet.is_dir():
        print(f"not a directory: {packet}", file=sys.stderr)
        return 1
    dest = packet / "captions.srt"
    if dest.is_file() and not args.force and not args.dry_run:
        print(f"REFUSE captions.srt exists; pass --force to overwrite: {dest}", file=sys.stderr)
        return 1
    try:
        text, info = build(packet)
    except (FileNotFoundError, ValueError, wave.Error) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(
        "CAPTION_DRAFT method={method} cues={cues} words={words} "
        "speech_s={speech_s} duration={duration} intervals={intervals}".format(**info)
    )
    print("not ASR; not approved; do not upload until a human spot-checks")
    if args.dry_run:
        sys.stdout.write(text)
        return 0
    dest.write_text(text, encoding="utf-8")
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
