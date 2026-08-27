#!/usr/bin/env python3
"""Write publish.md upload metadata stub for a video packet.

Description, tags, and first/pinned comment from idea + primary title.
No YouTube API. Does not invent a second title generator.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from title_thumb_brief import load_packet_inputs  # noqa: E402

STOP = {
    "a", "an", "the", "and", "or", "for", "to", "of", "in", "on", "is", "are",
    "it", "as", "be", "by", "your", "you", "that", "this", "with", "from",
    "how", "why", "what", "they", "their", "them", "then", "when", "because",
    "so", "not", "but", "someone", "who", "wants",
}

PLACEHOLDER_MARKERS = (
    "(add ",
    "(url",
    "todo",
    "tbd",
    "placeholder",
    "write the youtube description",
)


def field_line(text: str, name: str) -> str:
    m = re.search(rf"^-\s*{re.escape(name)}:[ \t]*([^\n]*)$", text, re.M)
    return m.group(1).strip() if m else ""


def section(text: str, heading: str) -> str:
    parts = re.split(rf"^##\s+{re.escape(heading)}\s*$", text, maxsplit=1, flags=re.M)
    if len(parts) < 2:
        return ""
    rest = re.split(r"^##\s+", parts[1], maxsplit=1, flags=re.M)[0]
    return rest.strip()


def primary_title(packet: Path) -> str:
    titles = packet / "titles.md"
    if titles.is_file():
        text = titles.read_text(encoding="utf-8")
        m = re.search(r"^Primary:[ \t]*([^\n]*)$", text, re.M)
        if m and m.group(1).strip():
            return m.group(1).strip()
    pkt = packet / "packet.md"
    if pkt.is_file():
        working = field_line(pkt.read_text(encoding="utf-8"), "working_title")
        if working:
            return working
    return packet.name


def promise_line(packet: Path) -> str:
    pkt = packet / "packet.md"
    if not pkt.is_file():
        return ""
    text = pkt.read_text(encoding="utf-8")
    block = section(text, "Promise")
    if not block:
        return ""
    line = " ".join(block.split())
    line = re.sub(r"^One sentence:\s*", "", line, flags=re.I)
    return line.strip()


def content_tokens(*blobs: str) -> list[str]:
    seen: list[str] = []
    for blob in blobs:
        for w in re.findall(r"[A-Za-z0-9']+", blob.lower()):
            if w in STOP or len(w) < 3:
                continue
            if w not in seen:
                seen.append(w)
    return seen


def tag_list(src: dict[str, str], title: str) -> list[str]:
    tokens = content_tokens(
        title, src.get("topic", ""), src.get("mechanism", ""), src.get("problem", "")
    )
    tags = [
        "focused work",
        "productivity systems",
        "work defaults",
        "start cue",
        "deep work",
        "decision fatigue",
    ]
    for tok in tokens[:8]:
        tags.append(tok)
    out: list[str] = []
    seen: set[str] = set()
    for t in tags:
        key = t.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(t)
        if len(out) >= 12:
            break
    return out


def is_placeholder_block(text: str) -> bool:
    if not text.strip():
        return True
    desc = section(text, "Description")
    title_block = section(text, "Title to upload")
    if desc and len(desc.split()) >= 12 and title_block.strip():
        if any(p in desc.lower() for p in PLACEHOLDER_MARKERS):
            return True
        return False
    return True


def publish_is_filled(text: str) -> bool:
    if not text.strip():
        return False
    return not is_placeholder_block(text)


def render(packet: Path) -> str:
    src = load_packet_inputs(packet)
    title = primary_title(packet)
    promise = promise_line(packet)
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    def lower_start(s: str) -> str:
        s = s.strip()
        if not s:
            return s
        return s[0].lower() + s[1:]

    problem = lower_start(src.get("problem") or "they stall after planning")
    mechanism = lower_start(src.get("mechanism") or "a written default that removes one daily decision")
    viewer = lower_start(src.get("viewer") or "someone who wants focused work")
    first_action = mechanism.rstrip(".")
    desc_bits = [
        f"{title}.",
        promise or f"After watching, you can replace a mood-dependent start with {first_action}.",
        f"If {problem.rstrip('.')}, this video walks the default instead of a pep talk.",
        f"Built for {viewer.rstrip('.')}.",
        "No upload happened. Human locks title, description, and tags before YouTube.",
    ]
    description = "\n\n".join(desc_bits)
    tags = tag_list(src, title)
    comment = (
        f"Assignment: install {first_action} before the next work block. "
        "Reply with the cue you wrote down. This comment is a draft pin, not posted."
    )
    return f"""# Publish

Status: stub
Generated: {generated}

This file is upload metadata, not a published video. There is no YouTube API
call here. Do not treat these fields as live channel copy.

## Title to upload
{title}

## Description
{description}

## Tags
{chr(10).join(f'- {t}' for t in tags)}

## First comment (pin candidate)
{comment}

## End screen / cards
- Last 20s reserved for YouTube end screen (see docs/editor.md)
- Do not auto-subscribe-CTA in spoken WORDS

## Human before upload
- [ ] Primary title locked (this stub used the current Primary / working_title)
- [ ] Description edited for search + honesty
- [ ] Tags trimmed
- [ ] First comment approved
- [ ] No YouTube upload from this tool
"""


def write_empty_publish(dest: Path) -> str:
    path = dest / "publish.md"
    existing = path.read_text(encoding="utf-8") if path.is_file() else ""
    if publish_is_filled(existing):
        return f"kept {dest.name}/publish.md (already filled)"
    path.write_text(render(dest), encoding="utf-8")
    return f"wrote {dest.name}/publish.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write publish.md stub (description, tags, first comment). No upload."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true", help="Print publish.md; do not write")
    parser.add_argument("--force", action="store_true", help="Overwrite a filled publish.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    dest = path / "publish.md"
    existing = dest.read_text(encoding="utf-8") if dest.is_file() else ""
    filled = publish_is_filled(existing)
    if filled and not args.force and not args.dry_run:
        print(f"publish.md already filled; pass --force to overwrite: {dest}", file=sys.stderr)
        return 1

    text = render(path)
    if args.dry_run:
        sys.stdout.write(text)
        return 0

    dest.write_text(text, encoding="utf-8")
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
