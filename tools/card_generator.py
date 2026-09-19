#!/usr/bin/env python3
"""Generate local 1920x1080 text/diagram cards from packet assets.md.

Does not commit binaries. Does not download stock. Does not bump packet status.
Does not mark a row ready unless --mark-ready and the PNG exists on disk.

Output lives under videos/NNN-slug/cards/ (gitignored).
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

WIDTH, HEIGHT = 1920, 1080
BG = (18, 18, 22)
FG = (245, 243, 238)
MUTED = (168, 164, 155)
ACCENT = (232, 196, 104)
RULE = (58, 56, 52)
LEFT = (36, 42, 58)
RIGHT = (42, 34, 28)


def parse_cards(text: str) -> list[dict[str, str]]:
    cards: list[dict[str, str]] = []
    block_parts = re.split(r"^##\\s+Cards\\s*$", text, maxsplit=1, flags=re.M)
    table = text if len(block_parts) < 2 else re.split(r"^##\\s+", block_parts[1], maxsplit=1, flags=re.M)[0]
    for ln in table.splitlines():
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) < 6:
            continue
        beat, need, typ, file_cell, source, status = cells[:6]
        if beat.lower() in {"beat", ""}:
            continue
        if set(beat) <= {"-", ":"}:
            continue
        fname = file_cell.strip("`").strip()
        if not fname.startswith("cards/"):
            continue
        cards.append(
            {
                "beat": beat,
                "need": need,
                "type": typ.lower(),
                "file": fname,
                "source": source,
                "status": status.lower(),
            }
        )
    return cards


def title_words(need: str, limit: int = 5) -> str:
    cleaned = re.sub(r"`+", "", need)
    cleaned = cleaned.replace("VISUAL:", "")
    cleaned = re.sub(r"\\s+", " ", cleaned).strip()
    if ":" in cleaned:
        tail = cleaned.split(":", 1)[1].strip()
        if tail:
            cleaned = tail
    words = cleaned.split()
    if len(words) <= limit:
        return cleaned
    return " ".join(words[:limit])


def beat_label(beat: str) -> str:
    raw = beat.split("—")[0].split("(")[0].strip()
    return raw.upper() or "CARD"


def _pil():
    from PIL import Image, ImageDraw, ImageFont

    return Image, ImageDraw, ImageFont


def _font(size: int):
    _, _, ImageFont = _pil()
    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    )
    for path in candidates:
        if Path(path).is_file():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def _wrap(draw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    cur = words[0]
    for w in words[1:]:
        trial = f"{cur} {w}"
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def _center(draw, lines: list[str], font, y: int, fill: tuple[int, int, int]) -> None:
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((WIDTH - w) / 2, y), line, font=font, fill=fill)
        bbox = font.getbbox(line or "X")
        y += (bbox[3] - bbox[1]) + 18


def render_text_card(card: dict[str, str]):
    Image, ImageDraw, _ImageFont = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((80, 80, WIDTH - 80, HEIGHT - 80), outline=RULE, width=3)
    label_font = _font(28)
    title_font = _font(72)
    note_font = _font(28)
    draw.text((110, 110), beat_label(card["beat"]), font=label_font, fill=ACCENT)
    title = title_words(card["need"], 6)
    lines = _wrap(draw, title, title_font, WIDTH - 280)
    _center(draw, lines, title_font, 420, FG)
    note = card["need"]
    if len(note) > 90:
        note = note[:87] + "…"
    note_lines = _wrap(draw, note, note_font, WIDTH - 320)
    _center(draw, note_lines[:2], note_font, 860, MUTED)
    return img


def render_diagram(card: dict[str, str]):
    Image, ImageDraw, _ImageFont = _pil()
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((80, 80, WIDTH - 80, HEIGHT - 80), outline=RULE, width=3)
    label_font = _font(28)
    panel_font = _font(48)
    vs_font = _font(36)
    draw.text((110, 110), beat_label(card["beat"]), font=label_font, fill=ACCENT)
    draw.rounded_rectangle((140, 280, 860, 820), radius=18, fill=LEFT, outline=RULE, width=2)
    draw.rounded_rectangle((1060, 280, 1780, 820), radius=18, fill=RIGHT, outline=RULE, width=2)
    left, right = "OPEN LIST", "ONE CARD"
    need = card["need"]
    if " vs " in need.lower():
        parts = re.split(r"\\s+vs\\s+", need, maxsplit=1, flags=re.I)
        left = title_words(parts[0], 4).upper()
        right = title_words(parts[1], 4).upper()
    for text, box in ((left, (140, 280, 860, 820)), (right, (1060, 280, 1780, 820))):
        lines = _wrap(draw, text, panel_font, box[2] - box[0] - 80)
        y = 480
        for line in lines[:3]:
            w = draw.textlength(line, font=panel_font)
            cx = (box[0] + box[2] - w) / 2
            draw.text((cx, y), line, font=panel_font, fill=FG)
            y += 64
    vw = draw.textlength("VS", font=vs_font)
    draw.text(((WIDTH - vw) / 2, 520), "VS", font=vs_font, fill=ACCENT)
    return img


def render_card(card: dict[str, str]):
    if card["type"] == "diagram":
        return render_diagram(card)
    return render_text_card(card)


def inspect_png(path: Path) -> dict[str, str]:
    info = {"path": str(path), "bytes": str(path.stat().st_size), "ok": "no"}
    try:
        Image, _ImageDraw, _ImageFont = _pil()
        with Image.open(path) as im:
            info["size"] = f"{im.size[0]}x{im.size[1]}"
            info["mode"] = im.mode
            if im.size == (WIDTH, HEIGHT) and path.stat().st_size > 0:
                info["ok"] = "yes"
    except OSError as exc:
        info["error"] = str(exc)
    return info


def write_cards(packet: Path, dry_run: bool = False) -> list[dict[str, str]]:
    assets = packet / "assets.md"
    if not assets.is_file():
        raise FileNotFoundError(f"missing assets.md: {assets}")
    cards = parse_cards(assets.read_text(encoding="utf-8"))
    out_dir = packet / "cards"
    results: list[dict[str, str]] = []
    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)
    for card in cards:
        dest = packet / card["file"]
        if dry_run:
            results.append({**card, "wrote": "dry-run", "ok": ""})
            continue
        img = render_card(card)
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(dest, format="PNG")
        info = inspect_png(dest)
        results.append({**card, "wrote": str(dest), "ok": info["ok"], "size": info.get("size", "")})
    return results


def render_manifest(packet: Path, rows: list[dict[str, str]]) -> str:
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# Card manifest",
        "",
        f"updated: {generated}",
        f"packet: `{packet.name}`",
        "generator: tools/card_generator.py",
        "binaries: local only; do not commit",
        "",
        "| Beat | File | Type | On disk | Size |",
        "|------|------|------|---------|------|",
    ]
    for r in rows:
        on = "yes" if r.get("ok") == "yes" else ("dry-run" if r.get("wrote") == "dry-run" else "no")
        lines.append(
            f"| {r['beat']} | `{r['file']}` | {r['type']} | {on} | {r.get('size', '')} |"
        )
    lines.append("")
    lines.append("Status rows in assets.md stay `planned` unless `--mark-ready` runs after files exist.")
    lines.append("")
    return "\n".join(lines)


def mark_ready(assets_text: str, ready_files: set[str]) -> str:
    out: list[str] = []
    for ln in assets_text.splitlines():
        if ln.startswith("|"):
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if len(cells) >= 6:
                fname = cells[3].strip("`")
                if fname in ready_files and cells[5].lower() == "planned":
                    cells[5] = "ready"
                    ln = "| " + " | ".join(cells) + " |"
        out.append(ln)
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local 1920x1080 cards from assets.md")
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--inspect-only", action="store_true", help="Inspect existing PNGs; write nothing")
    parser.add_argument("--mark-ready", action="store_true", help="Set assets.md Status ready when PNG exists")
    parser.add_argument("--write-manifest", action="store_true", help="Write card_manifest.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    assets = path / "assets.md"
    if not assets.is_file():
        print("missing assets.md", file=sys.stderr)
        return 1

    cards = parse_cards(assets.read_text(encoding="utf-8"))
    print(f"packet: {path.name}")
    print(f"planned: {len(cards)}")

    if args.inspect_only:
        ok = 0
        for c in cards:
            dest = path / c["file"]
            if dest.is_file():
                info = inspect_png(dest)
                print(f"{c['file']}: {info['ok']} {info.get('size', '')}")
                if info["ok"] == "yes":
                    ok += 1
            else:
                print(f"{c['file']}: missing")
        print(f"ready_on_disk: {ok}/{len(cards)}")
        return 0 if ok == len(cards) and cards else 1

    rows = write_cards(path, dry_run=args.dry_run)
    for r in rows:
        print(f"{r['file']}: {r.get('ok') or r.get('wrote')}")

    if args.write_manifest and not args.dry_run:
        manifest = render_manifest(path, rows)
        dest = path / "card_manifest.md"
        dest.write_text(manifest, encoding="utf-8")
        print(dest)

    if args.mark_ready and not args.dry_run:
        ready = {r["file"] for r in rows if r.get("ok") == "yes"}
        assets.write_text(mark_ready(assets.read_text(encoding="utf-8"), ready), encoding="utf-8")
        print(f"marked ready: {len(ready)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
