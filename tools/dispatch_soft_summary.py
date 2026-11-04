#!/usr/bin/env python3
"""Soft dispatch readiness summary for a packet.

Aggregates key soft signals (duration match hint, master SHA reminder,
metadata glance) into one printable page for the human before OAuth/dispatch.
Does not change hard gates, invent media, run ffmpeg, poll secrets, or write files.
Reusable across packets. Complements human_one_pager.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from render_brief import selected_vo_drop  # noqa: E402
from timeline import plan  # noqa: E402

try:
    from words import all_spoken_words, spoken_seconds, fmt_mmss  # type: ignore
except ImportError:
    def all_spoken_words(script: str) -> list[str]:
        return []
    def spoken_seconds(n: int) -> float:
        return (n / 150.0) * 60.0
    def fmt_mmss(seconds: float) -> str:
        whole = int(round(max(0, seconds)))
        m, s = divmod(whole, 60)
        return f"{m:02d}:{s:02d}"

EXPECTED_MASTER_SHA = "4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546"
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"


def wav_seconds(path: Path) -> float | None:
    try:
        import wave
        with wave.open(str(path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            if rate > 0 and frames > 0:
                return frames / float(rate)
    except Exception:
        return None
    return None


def extract_section(text: str, header: str) -> str:
    lines = text.splitlines()
    capture = False
    collected = []
    for line in lines:
        if line.strip() == header:
            capture = True
            continue
        if capture and line.startswith("## ") and line.strip() != header:
            break
        if capture:
            collected.append(line)
    return "\n".join(collected).strip()


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"not a directory: {packet}", file=sys.stderr)
        return 1

    print("DISPATCH SOFT SUMMARY (soft only; gates unchanged)")
    print(f"Packet: {packet.name}")
    print()

    # Metadata glance
    publish = packet / "publish.md"
    title = "(missing)"
    if publish.is_file():
        text = publish.read_text(encoding="utf-8")
        title_lines = extract_section(text, "## Title to upload").splitlines()
        title = title_lines[0].strip() if title_lines else "(missing)"
    print(f"TITLE: {title}")
    print(f"MASTER SHA (r253 only): {EXPECTED_MASTER_SHA}")
    print()

    # Soft duration
    data = plan(packet)
    vo_path = packet / data["vo_rel"]
    vo_file = vo_path if vo_path.is_file() and vo_path.stat().st_size > 0 else None
    draft = packet / "draft.md"
    script = packet / "script.md"
    source = draft if draft.is_file() else script if script.is_file() else None
    n_words = 0
    est_s = 0.0
    if source:
        try:
            text = source.read_text(encoding="utf-8")
            n_words = len(all_spoken_words(text))
            est_s = spoken_seconds(n_words)
        except Exception:
            pass
    print(f"Spoken words (est): {n_words}")
    print(f"Estimated duration: {fmt_mmss(est_s)}")
    if vo_file:
        actual = wav_seconds(vo_file)
        if actual:
            delta = actual - est_s
            print(f"Actual VO duration: {fmt_mmss(actual)} (delta {delta:+.1f}s)")
            if abs(delta) > 15:
                print("NOTE: large delta; consider trim or script adjust (soft)")
        else:
            print("Actual VO: present but unreadable")
    else:
        print("Actual VO: not present (soft)")
    print()
    print("For full soft recipes (resample, gain, bit-depth, trim):")
    print(f"  python3 tools/media_qa.py {packet}")
    print(f"  python3 tools/vo_duration_match.py {packet}")
    print()
    print("Human next: docs/human_oauth_checklist.md or python3 tools/human_one_pager.py")
    print("DISPATCH SOFT SUMMARY PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
