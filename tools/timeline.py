#!/usr/bin/env python3
"""Deterministic edit timeline from script.md WORDS + assets.md cards.

Clock: 150 wpm from WORDS, floor 1.5s per card hold.
Adds a 20s end-screen reserve after CTA.
Does not run ffmpeg. Does not invent media. Does not bump packet status.
Does not re-implement selected_vo_drop.
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

from card_generator import parse_cards  # noqa: E402
from render_brief import selected_vo_drop  # noqa: E402

WPM = 150.0
MIN_HOLD = 1.5
END_SCREEN = 20.0


def extract_beats(script: str) -> list[dict[str, str]]:
    beats: list[dict[str, str]] = []
    parts = re.split(r"^##[ \t]+", script, flags=re.M)
    for part in parts[1:]:
        lines = part.splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:])
        words_m = re.search(r"^WORDS:\s*\n(.*?)(?=^VISUAL:|\Z)", body, re.M | re.S)
        words = (words_m.group(1).strip() if words_m else "")
        words = re.sub(r"\s+", " ", words).strip()
        beats.append({"title": title, "words": words})
    return beats


def word_count(text: str) -> int:
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def spoken_seconds(words: int) -> float:
    if words <= 0:
        return MIN_HOLD
    return max(MIN_HOLD, round(words / WPM * 60.0, 1))


def card_key(text: str) -> str | None:
    """Stable beat key. Do not match on the bare word 'beat' — Beat 2 would steal Beat 1."""
    t = text.lower().strip()
    if re.match(r"hook\b", t):
        return "hook"
    if re.match(r"payoff\b", t):
        return "payoff"
    if re.match(r"cta\b", t):
        return "cta"
    m = re.search(r"beat\s*(\d+)", t)
    if m:
        return f"beat{m.group(1)}"
    return None


def match_card(title: str, cards: list[dict[str, str]]) -> dict[str, str] | None:
    key = card_key(title)
    if not key:
        return None
    for card in cards:
        if card_key(card.get("beat", "")) == key:
            return card
    for card in cards:
        fname = card["file"].lower()
        if f"cards/{key}-" in fname or fname.startswith(f"cards/{key}"):
            return card
    return None


def vo_present(packet: Path) -> tuple[bool, str]:
    drop = selected_vo_drop(packet)
    name = Path(drop).name
    stem = Path(name).stem
    candidates = [
        packet / "vo" / name,
        packet / "vo" / f"{stem}.flac",
        packet / "vo" / f"{stem}-v2.wav",
        packet / "vo" / f"{stem}-v2.flac",
    ]
    for p in candidates:
        if p.is_file() and p.stat().st_size > 0:
            return True, str(p.relative_to(packet))
    return False, f"vo/{name}"


def plan(packet: Path) -> dict:
    script_path = packet / "script.md"
    assets_path = packet / "assets.md"
    script = script_path.read_text(encoding="utf-8") if script_path.is_file() else ""
    assets = assets_path.read_text(encoding="utf-8") if assets_path.is_file() else ""
    beats = extract_beats(script)
    cards = parse_cards(assets)
    vo_ok, vo_rel = vo_present(packet)

    rows = []
    t = 0.0
    total_words = 0
    for beat in beats:
        wc = word_count(beat["words"])
        total_words += wc
        dur = spoken_seconds(wc)
        card = match_card(beat["title"], cards)
        card_rel = card["file"] if card else ""
        card_ok = bool(card_rel) and (packet / card_rel).is_file()
        rows.append(
            {
                "title": beat["title"],
                "words": wc,
                "start": t,
                "dur": dur,
                "card": card_rel,
                "card_on_disk": "yes" if card_ok else "no",
                "track": "DIAGRAM" if card and card["type"] == "diagram" else "TITLES",
            }
        )
        t += dur
    spoken = t
    export = spoken + END_SCREEN
    cards_ready = sum(1 for r in rows if r["card"] and r["card_on_disk"] == "yes")
    cards_planned = sum(1 for r in rows if r["card"])
    return {
        "packet": packet.name,
        "drop": selected_vo_drop(packet),
        "vo_rel": vo_rel,
        "vo_on_disk": "yes" if vo_ok else "no",
        "rows": rows,
        "spoken": spoken,
        "export": export,
        "words": total_words,
        "cards_ready": cards_ready,
        "cards_planned": cards_planned,
        "ready_to_assemble": vo_ok and cards_ready == cards_planned and cards_planned > 0,
    }


def fmt_clock(sec: float) -> str:
    m = int(sec // 60)
    s = sec - 60 * m
    return f"{m}:{s:04.1f}"


def render_markdown(data: dict) -> str:
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# Timeline",
        "",
        f"Generated: {generated}",
        f"Packet: `{data['packet']}`",
        f"Clock: {WPM:.0f} wpm WORDS estimate; card floor {MIN_HOLD}s; end-screen +{END_SCREEN:.0f}s",
        f"Selected VO DROP: `{data['drop']}`",
        f"VO on disk: {data['vo_on_disk']} (`{data['vo_rel']}`)",
        f"Spoken estimate: {fmt_clock(data['spoken'])} ({data['words']} words)",
        f"Export estimate: {fmt_clock(data['export'])} (includes end-screen reserve)",
        f"Cards mapped: {data['cards_planned']}; on disk: {data['cards_ready']}",
        f"Ready to assemble: {'yes' if data['ready_to_assemble'] else 'no'}",
        "",
        "This file is a cut list. It is not an ffmpeg recipe and not a master export.",
        "Repo-root `vo/` is not Selected VO. Do not invent media. Do not `git add -f`.",
        "",
        "| # | Beat | Start | Hold | Words | Card | On disk | Track |",
        "|---|------|-------|------|-------|------|---------|-------|",
    ]
    for i, r in enumerate(data["rows"], 1):
        card = f"`{r['card']}`" if r["card"] else "—"
        lines.append(
            f"| {i} | {r['title']} | {fmt_clock(r['start'])} | {r['dur']:.1f}s | {r['words']} | {card} | {r['card_on_disk']} | {r['track']} |"
        )
    lines.append("")
    lines.append("## Assembly gate")
    lines.append("- VO present on the packet-relative DROP path")
    lines.append("- every mapped card PNG exists locally at 1920x1080")
    lines.append("- export target remains `exports/{id}-{slug}-vN.mp4`")
    lines.append("- last 20s keep CTA readable for YouTube end-screen")
    lines.append("- `tools/timeline.py` never runs ffmpeg")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a WORDS-based edit timeline. No ffmpeg.")
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true", help="Print timeline.md; do not write")
    parser.add_argument("--write", action="store_true", help="Write packet timeline.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    if not (path / "script.md").is_file():
        print("missing script.md", file=sys.stderr)
        return 1

    data = plan(path)
    text = render_markdown(data)
    print(f"packet: {data['packet']}")
    print(f"spoken: {fmt_clock(data['spoken'])}")
    print(f"export: {fmt_clock(data['export'])}")
    print(f"vo_on_disk: {data['vo_on_disk']}")
    print(f"cards: {data['cards_ready']}/{data['cards_planned']}")
    print(f"ready_to_assemble: {'yes' if data['ready_to_assemble'] else 'no'}")
    if args.dry_run and not args.write:
        sys.stdout.write("\n" + text)
        return 0
    if args.write:
        dest = path / "timeline.md"
        dest.write_text(text, encoding="utf-8")
        print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
