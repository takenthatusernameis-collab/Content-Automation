#!/usr/bin/env python3
"""Generate a local packet status dashboard PNG.

Reads key files and presence signals from the packet folder and renders
a single glanceable 1280x720 status card: title, file presence, word count,
simple readiness flags. No invented claims, no external services, no secret polling.
Output: packet/packet_status_card.png (gitignored).
Reduces recurring human labor of opening multiple files and running several
status tools just to get an at-a-glance packet health picture on every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 720
BG = (18, 18, 22)
FG = (245, 243, 238)
ACCENT = (232, 196, 104)
MUTED = (140, 136, 130)
LINE = (58, 56, 52)
GOOD = (90, 180, 110)
WARN = (220, 160, 60)
BAD = (200, 80, 80)


def extract_title(publish_text: str) -> str:
    match = re.search(
        r"^##\s+Title to upload\s*\n(.+?)(?:\n##|\n\n|\Z)",
        publish_text,
        re.M | re.S,
    )
    if match:
        title = match.group(1).strip()
        if title:
            return title
    lines = publish_text.splitlines()
    for i, line in enumerate(lines):
        if "title to upload" in line.lower():
            for next_line in lines[i + 1 :]:
                stripped = next_line.strip()
                if stripped and not stripped.startswith("#"):
                    return stripped
    return "Untitled"


def count_words(script_text: str) -> int:
    # rough spoken word estimate: lines that look like content after WORDS marker or just non-header
    body = script_text
    if "WORDS" in body:
        body = body.split("WORDS", 1)[-1]
    words = re.findall(r"\b[\w']+\b", body)
    return len(words)


def check_presence(packet: Path) -> dict:
    return {
        "script.md": (packet / "script.md").is_file(),
        "publish.md": (packet / "publish.md").is_file(),
        "idea.md": (packet / "idea.md").is_file(),
        "vo": any((packet / "vo").glob("*-take-selected.*")) if (packet / "vo").is_dir() else False,
        "cards": any((packet / "cards").glob("*.png")) if (packet / "cards").is_dir() else False,
        "export": (packet / "export" / "master.mp4").is_file() or any((packet / "export").glob("*.mp4")) if (packet / "export").is_dir() else False,
        "captions.srt": (packet / "captions.srt").is_file(),
        "thumbnail.png": (packet / "thumbnail.png").is_file(),
    }


def _font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    candidates = (
        f"/usr/share/fonts/truetype/dejavu/{name}",
        f"/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    )
    for p in candidates:
        if Path(p).is_file():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def render_card(title: str, presence: dict, word_count: int, packet_name: str) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, WIDTH - 1, HEIGHT - 1), outline=LINE, width=3)
    draw.text((24, 16), "Packet Status Card", font=_font(28, bold=True), fill=ACCENT)
    draw.text((24, 52), packet_name[:70], font=_font(16), fill=MUTED)

    # Title
    draw.text((24, 90), "Title:", font=_font(18, bold=True), fill=FG)
    title_font = _font(22)
    # simple wrap
    words = title.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=title_font) < WIDTH - 80:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    y = 120
    for line in lines[:3]:
        draw.text((40, y), line, font=title_font, fill=FG)
        y += 30

    # Presence grid
    y = 230
    draw.text((24, y), "Presence:", font=_font(18, bold=True), fill=FG)
    y += 36
    items = list(presence.items())
    for i, (name, present) in enumerate(items):
        col = i % 2
        row = i // 2
        x = 40 + col * 400
        yy = y + row * 32
        color = GOOD if present else BAD
        mark = "YES" if present else "NO"
        draw.text((x, yy), f"{name:16} {mark}", font=_font(16), fill=color)

    # Word count and simple flags
    y = 500
    draw.text((24, y), f"Spoken words (approx): {word_count}", font=_font(18), fill=FG)
    y += 32
    flags = []
    if presence["script.md"] and presence["publish.md"]:
        flags.append(("text complete", GOOD))
    else:
        flags.append(("text incomplete", WARN))
    if presence["vo"]:
        flags.append(("VO present", GOOD))
    else:
        flags.append(("VO missing", BAD))
    if presence["export"]:
        flags.append(("export present", GOOD))
    else:
        flags.append(("export missing", MUTED))
    for label, color in flags:
        draw.text((40, y), label, font=_font(16), fill=color)
        y += 28

    draw.text((24, HEIGHT - 32), "local status card (gitignored) | no invented data | not a completion gate", font=_font(12), fill=MUTED)
    return img


def main() -> int:
    p = argparse.ArgumentParser(description="Generate local packet status dashboard PNG")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    publish = packet / "publish.md"
    title = "Untitled"
    if publish.is_file():
        title = extract_title(publish.read_text(encoding="utf-8"))
    print(f"title: {title}")

    script = packet / "script.md"
    word_count = 0
    if script.is_file():
        word_count = count_words(script.read_text(encoding="utf-8"))
    print(f"words: {word_count}")

    presence = check_presence(packet)
    for k, v in presence.items():
        print(f"  {k}: {'yes' if v else 'no'}")

    img = render_card(title, presence, word_count, packet.name)
    out = packet / "packet_status_card.png"
    img.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print("Packet status card ready (gitignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
