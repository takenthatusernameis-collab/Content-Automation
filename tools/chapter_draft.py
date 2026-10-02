#!/usr/bin/env python3
"""Draft YouTube chapter timestamps from script beats and captions.srt.

Not ASR. Not an approval. Does not check publish boxes. Does not upload.
A missing srt or a script with no WORDS beats refuses.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CUE_RE = re.compile(
    r"(\d+)\s*\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s*\n(.*?)(?=\n\n|\Z)",
    re.S,
)
HEADING_RE = re.compile(r"^##\s+(.+)$", re.M)
MIN_GAP = 10.0
NEEDLE = 5


def _seconds(stamp: str) -> float:
    h, m, rest = stamp.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def _clock(seconds: float) -> str:
    total = max(0, int(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.lower())


def parse_cues(text: str) -> list[dict]:
    cues = []
    for match in CUE_RE.finditer(text.strip() + "\n"):
        body = match.group(4).strip("\n")
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        cues.append(
            {
                "index": int(match.group(1)),
                "start": match.group(2),
                "start_s": _seconds(match.group(2)),
                "text": " ".join(lines),
            }
        )
    return cues



def _heading_label(label: str) -> str:
    low = label.lower()
    if low == "hook":
        return "The reopen"
    if low.startswith("payoff"):
        return "Written default"
    if low == "cta":
        return "Tomorrow's sentence"
    return label


def _label_from_sentence(sentence: str) -> str:
    low = sentence.lower()
    if re.search(r"\bstall\b", low):
        return "The stall"
    if re.search(r"\bfailure\b", low):
        return "Failure modes"
    if re.search(r"\bworkday\b", low) or "closed loop" in low:
        return "One workday"
    if re.search(r"\bdefault\b", low):
        return "Install the default"
    words = re.findall(r"[A-Za-z0-9']+", sentence)
    drop = {"here", "is", "the", "a", "an", "it", "as", "you", "your", "not"}
    kept = [w for w in words if w.lower() not in drop]
    if not kept:
        kept = words
    phrase = " ".join(kept[:3])
    return phrase[:1].upper() + phrase[1:]


def parse_beats(script: str) -> list[dict]:
    beats = []
    parts = HEADING_RE.split(script)
    # split keeps the leading preamble at [0], then heading, body, heading, body
    if len(parts) < 3:
        return beats
    for heading, body in zip(parts[1::2], parts[2::2]):
        if "WORDS:" not in body:
            continue
        spoken = body.split("WORDS:", 1)[1]
        spoken = spoken.split("VISUAL:", 1)[0]
        tokens = _words(spoken)
        if len(tokens) < 3:
            continue
        label = heading.strip()
        label = re.sub(r"\s*\([^)]*\)\s*", " ", label).strip(" -—")
        if re.fullmatch(r"Beat\s+\d+", label, re.I) or not label:
            sentence = re.split(r"[.!?]", spoken.strip(), maxsplit=1)[0]
            label = _label_from_sentence(sentence)
        else:
            label = _heading_label(label)
        beats.append({"heading": heading.strip(), "label": label[:42], "needle": tokens[:NEEDLE]})
    return beats


def match_beats(beats: list[dict], cues: list[dict]) -> list[dict]:
    stream: list[str] = []
    spans: list[tuple[int, int]] = []
    for cue in cues:
        start = len(stream)
        stream.extend(_words(cue["text"]))
        spans.append((start, len(stream)))
    chapters = []
    cursor = 0
    for beat in beats:
        needle = beat["needle"]
        found = None
        limit = len(stream) - len(needle) + 1
        for i in range(cursor, max(cursor, limit)):
            if stream[i : i + len(needle)] == needle:
                found = i
                break
        if found is None:
            continue
        cue = cues[0]
        for cue_i, (start, end) in enumerate(spans):
            if start <= found < end:
                cue = cues[cue_i]
                break
        chapters.append(
            {
                "label": beat["label"],
                "start_s": cue["start_s"],
                "cue": cue["index"],
            }
        )
        cursor = found + len(needle)
    return chapters


def space_chapters(chapters: list[dict]) -> list[dict]:
    if not chapters:
        return []
    kept = [{"label": chapters[0]["label"], "start_s": 0.0, "cue": chapters[0]["cue"]}]
    for chapter in chapters[1:]:
        if chapter["start_s"] - kept[-1]["start_s"] < MIN_GAP:
            continue
        kept.append(chapter)
    return kept


def render(packet: Path, chapters: list[dict]) -> str:
    lines = [
        "# Chapter draft",
        "",
        "Status: draft timestamps, not an approval.",
        "Method: script WORDS matched to captions.srt cue order. Not ASR. Not uploaded.",
        "This file does not check Description edited, First comment approved, or the caption spot-check box.",
        "",
        f"Packet: `{packet.name}`",
        f"Chapters: {len(chapters)}",
        f"Minimum gap: {MIN_GAP:.0f}s (YouTube chapter rule). Closer beats are skipped, not merged.",
        "",
        "Human work: confirm the first and last line while reviewing the description. An agent must not check the description box.",
        "",
        "## YouTube lines",
        "",
    ]
    for chapter in chapters:
        lines.append(f"{_clock(chapter['start_s'])} {chapter['label']}")
    lines.extend(
        [
            "",
            "## Do not",
            "",
            "- Do not treat these times as ASR.",
            "- Do not check Description edited from an agent run.",
            "- Do not regenerate while the captions.srt checksum is unchanged.",
            "",
        ]
    )
    return "\n".join(lines)


def build(packet: Path) -> tuple[str, dict]:
    srt = packet / "captions.srt"
    script = packet / "script.md"
    if not srt.is_file():
        raise FileNotFoundError(f"REFUSE: missing {srt}")
    if not script.is_file():
        raise FileNotFoundError(f"REFUSE: missing {script}")
    cues = parse_cues(srt.read_text(encoding="utf-8"))
    if not cues:
        raise ValueError("REFUSE: captions.srt has no cues")
    beats = parse_beats(script.read_text(encoding="utf-8"))
    if len(beats) < 3:
        raise ValueError("REFUSE: script has fewer than 3 WORDS beats")
    chapters = space_chapters(match_beats(beats, cues))
    if len(chapters) < 3:
        raise ValueError("REFUSE: fewer than 3 chapters after the 10s gap rule")
    if chapters[0]["start_s"] != 0.0:
        raise ValueError("REFUSE: first chapter must be 0:00")
    text = render(packet, chapters)
    info = {
        "chapters": len(chapters),
        "approval": False,
        "lines": [f"{_clock(c['start_s'])} {c['label']}" for c in chapters],
    }
    return text, info


def main() -> int:
    parser = argparse.ArgumentParser(description="Draft YouTube chapters from script + srt. Not an approval.")
    parser.add_argument("packet", type=Path)
    parser.add_argument("--write", action="store_true", help="Write chapters.md. Does not edit publish.md.")
    args = parser.parse_args()
    packet = args.packet
    text, info = build(packet)
    if args.write:
        path = packet / "chapters.md"
        path.write_text(text, encoding="utf-8")
        print(f"WROTE {path}")
    else:
        sys.stdout.write(text)
    print(
        f"CHAPTER_DRAFT chapters={info['chapters']} approval={info['approval']}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
