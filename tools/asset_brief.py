#!/usr/bin/env python3
"""Write assets.md card list from script.md VISUAL lines.

Suggested filenames only. Not stock shopping, not image download,
not proof that cards exist on disk.
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

PLACEHOLDER_MARKERS = (
    "(add ",
    "todo",
    "tbd",
    "placeholder",
    "after script visual",
    "write visual lines",
)
DIAGRAM_TOKENS = (
    "diagram",
    "icon",
    "vs",
    "contrast",
    "checkbox",
    "checkboxes",
    "arrow",
    "->",
    "flow",
    "board",
    "calendar",
)


def section(text: str, heading: str) -> str:
    parts = re.split(rf"^##\s+{re.escape(heading)}\s*$", text, maxsplit=1, flags=re.M)
    if len(parts) < 2:
        return ""
    rest = re.split(r"^##\s+", parts[1], maxsplit=1, flags=re.M)[0]
    return rest.strip()


def visual_text(block: str) -> str:
    m = re.search(r"VISUAL:\s*(.*?)(?:WORDS:|\Z)", block, re.S)
    blob = m.group(1) if m else ""
    blob = blob.replace("*", " ")
    blob = " ".join(blob.split())
    blob = re.sub(
        r"^(plain\s+)?text\s+card\s*:\s*",
        "",
        blob,
        flags=re.I,
    )
    blob = blob.strip(" \"'")
    return blob


def beat_prefix(heading: str) -> str:
    h = heading.strip().lower()
    if h.startswith("hook"):
        return "hook"
    if h.startswith("payoff"):
        return "payoff"
    m = re.match(r"beat\s+(\d+)", h)
    if m:
        return f"beat{m.group(1)}"
    if h.startswith("cta"):
        return "cta"
    slug = re.sub(r"[^a-z0-9]+", "-", h)
    slug = slug.strip("-")[:16] or "card"
    return slug


def slugify(text: str, limit: int = 36) -> str:
    s = text.lower()
    s = s.replace("->", " to ")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if not s:
        return "card"
    return s[:limit].strip("-") or "card"


def card_type(need: str) -> str:
    low = need.lower()
    if any(tok in low for tok in DIAGRAM_TOKENS):
        return "diagram"
    return "text-card"


def script_cards(script: str) -> list[dict[str, str]]:
    headings = re.findall(r"^##\s+(.+)$", script, re.M)
    cards: list[dict[str, str]] = []
    seen: set[str] = set()
    for heading in headings:
        block = section(script, heading)
        need = visual_text(block)
        if not need:
            continue
        prefix = beat_prefix(heading)
        fname = f"cards/{prefix}-{slugify(need)}.png"
        n = 2
        base = fname[:-4]
        while fname in seen:
            fname = f"{base}-{n}.png"
            n += 1
        seen.add(fname)
        cards.append(
            {
                "beat": heading.strip(),
                "need": need,
                "type": card_type(need),
                "file": fname,
                "source": "editor",
                "status": "planned",
            }
        )
    return cards


def assets_is_filled(text: str) -> bool:
    if not text.strip():
        return False
    low = text.lower()
    if any(p in low for p in PLACEHOLDER_MARKERS):
        if "card count: 0" in low or "(add visual" in low:
            return False
    block_parts = re.split(r"^##\s+Cards\s*$", text, maxsplit=1, flags=re.M)
    table = text
    if len(block_parts) >= 2:
        table = re.split(r"^##\s+", block_parts[1], maxsplit=1, flags=re.M)[0]
    rows = []
    for ln in table.splitlines():
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if not cells or cells[0].lower() in {"beat", "need", ""}:
            continue
        if set(cells[0]) <= {"-", ":"}:
            continue
        if any(p in ln.lower() for p in PLACEHOLDER_MARKERS):
            continue
        if len(cells[0]) >= 3:
            rows.append(ln)
    return bool(rows)


def render(packet: Path) -> str:
    script_path = packet / "script.md"
    script = script_path.read_text(encoding="utf-8") if script_path.is_file() else ""
    cards = script_cards(script)
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if not cards:
        card_body = (
            "(add visual lines after script VISUAL exists)\n"
            "| Beat | Need | Type | Suggested file | Source | Status |\n"
            "|------|------|------|----------------|--------|--------|\n"
            "|      |      |      |                |        | planned |"
        )
        status = "placeholder"
    else:
        lines = [
            "| Beat | Need | Type | Suggested file | Source | Status |",
            "|------|------|------|----------------|--------|--------|",
        ]
        for c in cards:
            need = c["need"].replace("|", "/")
            beat = c["beat"].replace("|", "/")
            lines.append(
                f"| {beat} | {need} | {c['type']} | `{c['file']}` | {c['source']} | {c['status']} |"
            )
        card_body = "\n".join(lines)
        status = "stub"

    return f"""# Assets

Status: {status}
Generated: {generated}
Card count: {len(cards)}

This file is an asset intake stub from script.md VISUAL lines. It is not a
stock search, not a download, and not proof that image files exist on disk.
Do not treat Suggested file as a committed binary.

## Cards
{card_body}

## Filename convention
- Folder: `videos/{packet.name}/cards/` (local editor exports; usually gitignored)
- Pattern: `cards/{{beat}}-{{short-slug}}.png`
- Types: `text-card` or `diagram` (heuristic from VISUAL wording)
- Rules: `docs/assets.md`

## Human
- [ ] Build each planned card in the editor (TITLES / DIAGRAM tracks)
- [ ] Keep on-card text <=5 words when it is a title card
- [ ] Do not buy stock to fill a text-card row
- [ ] Do not mark Status `ready` until the file exists locally
"""


def write_empty_assets(dest: Path) -> str:
    path = dest / "assets.md"
    existing = path.read_text(encoding="utf-8") if path.is_file() else ""
    if assets_is_filled(existing):
        return f"kept {dest.name}/assets.md (already filled)"
    path.write_text(render(dest), encoding="utf-8")
    return f"wrote {dest.name}/assets.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write assets.md card list from script VISUAL lines. No stock."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true", help="Print assets.md; do not write")
    parser.add_argument("--force", action="store_true", help="Overwrite a filled assets.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    dest = path / "assets.md"
    existing = dest.read_text(encoding="utf-8") if dest.is_file() else ""
    filled = assets_is_filled(existing)
    if filled and not args.force and not args.dry_run:
        print(f"assets.md already filled; pass --force to overwrite: {dest}", file=sys.stderr)
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
