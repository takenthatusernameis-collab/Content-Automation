#!/usr/bin/env python3
"""Generate a local preview PNG of key claims from script.md.

Extracts digit tokens and common hedge phrases from spoken WORDS and renders
them as a readable list card PNG. Output: packet/claims_preview.png (gitignored).
No invented content, no external services. Reduces recurring human labor of
running claim_scan and opening the script just to review factual claims on
every future packet. One command produces a glanceable claims image.
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
WARN = (220, 140, 80)

# Minimal hedge patterns (subset; full list lives in phrase_utils)
HEDGES = [
    r"\bmany studies show\b",
    r"\bresearch has shown\b",
    r"\bit is known that\b",
    r"\bwidely known that\b",
    r"\bstatistics show\b",
    r"\bdata indicates\b",
    r"\bas research shows\b",
    r"\bstudies have shown\b",
    r"\bresearchers found\b",
    r"\baccording to a survey\b",
    r"\bdata reveals\b",
    r"\bexperts agree\b",
    r"\bstudies suggest\b",
    r"\baccording to experts\b",
    r"\bresearch suggests\b",
    r"\bevidence shows\b",
    r"\bit has been shown\b",
    r"\bscientists say\b",
    r"\ba study found\b",
    r"\bsurveys indicate\b",
]

DIGIT_RE = re.compile(r"\b\d+(?:\.\d+)?%?\b")


def spoken_words(script: str) -> str:
    """Extract concatenated WORDS: blocks."""
    blocks = re.findall(r"^WORDS:\s*\n(.*?)(?=\n\n|\n##|\nVISUAL:|\Z)", script, re.M | re.S)
    return "\n".join(b.strip() for b in blocks if b.strip())


def extract_claims(script_text: str) -> list[str]:
    """Return list of claim strings (digits + hedges)."""
    body = spoken_words(script_text)
    if not body:
        return []
    claims = []
    # Digits
    for m in DIGIT_RE.finditer(body):
        token = m.group(0)
        # Context snippet
        start = max(0, m.start() - 30)
        end = min(len(body), m.end() + 30)
        ctx = body[start:end].replace("\n", " ").strip()
        claims.append(f"DIGIT: {token}  …{ctx}…")
    # Hedges
    for pat in HEDGES:
        for m in re.finditer(pat, body, re.I):
            phrase = m.group(0)
            start = max(0, m.start() - 20)
            end = min(len(body), m.end() + 20)
            ctx = body[start:end].replace("\n", " ").strip()
            claims.append(f"HEDGE: {phrase}  …{ctx}…")
    # Dedup preserving order
    seen = set()
    unique = []
    for c in claims:
        key = c.split("  ")[0]
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique[:12]  # max 12 lines


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


def main() -> int:
    p = argparse.ArgumentParser(description="Generate local claims preview PNG")
    p.add_argument("packet", type=Path, help="Path to video packet folder")
    args = p.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"ERROR: not a directory: {packet}", file=sys.stderr)
        return 1

    script = packet / "script.md"
    if not script.is_file():
        print("ERROR: script.md missing", file=sys.stderr)
        return 1

    claims = extract_claims(script.read_text(encoding="utf-8"))
    print(f"claims found: {len(claims)}")

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((20, 20, WIDTH - 20, HEIGHT - 20), outline=LINE, width=3)
    draw.text((40, 40), "CLAIMS PREVIEW", font=_font(22, bold=True), fill=ACCENT)
    draw.text((40, 75), "Digits and hedges from spoken WORDS (revision signals)", font=_font(16), fill=MUTED)

    font = _font(18)
    y = 120
    if not claims:
        draw.text((50, y), "No digit tokens or hedge phrases detected.", font=font, fill=FG)
    else:
        for i, claim in enumerate(claims):
            color = WARN if claim.startswith("HEDGE") else FG
            # Truncate long lines
            line = claim[:90] + ("…" if len(claim) > 90 else "")
            draw.text((50, y), line, font=font, fill=color)
            y += 36
            if y > HEIGHT - 80:
                break

    draw.text((40, HEIGHT - 50), "From script.md WORDS — gitignored preview. Cross-check research.md sources.", font=_font(16), fill=MUTED)

    out = packet / "claims_preview.png"
    img.save(out, "PNG")
    print(f"wrote: {out}")
    print(f"size: {out.stat().st_size} bytes")
    print("Claims preview ready (gitignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
