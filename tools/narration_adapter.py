#!/usr/bin/env python3
"""Narration adapter: extract spoken WORDS, inspect a take, write provenance.

Does not synthesize audio. Does not upload. Does not bump packet status.
Does not treat repo-root vo/ as Selected VO.

Generated takes must be labeled generated. Human takes must be labeled human.
A missing take is reported; it is never invented.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import wave
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from render_brief import selected_vo_drop  # noqa: E402

WORDS_RE = re.compile(r"(?im)^WORDS:\s*(.*?)(?=^VISUAL:|^## |\Z)")


def extract_words(script_text: str) -> str:
    chunks: list[str] = []
    for m in WORDS_RE.finditer(script_text):
        body = m.group(1).strip()
        if body:
            chunks.append(re.sub(r"\s+", " ", body))
    return "\n\n".join(chunks)


def candidate_takes(packet: Path) -> list[Path]:
    drop = selected_vo_drop(packet)
    name = Path(drop).name
    stem = name.rsplit(".", 1)[0]
    folder = packet / "vo"
    names = [
        f"{stem}.wav",
        f"{stem}.flac",
        f"{stem}.mp3",
        f"{stem}-v2.wav",
        f"{stem}-v2.flac",
        f"{stem}-v2.mp3",
    ]
    return [folder / n for n in names]


def find_take(packet: Path) -> Path | None:
    for p in candidate_takes(packet):
        if p.is_file() and p.stat().st_size > 0:
            return p
    return None


def inspect_wav(path: Path) -> dict[str, str]:
    info: dict[str, str] = {
        "path": str(path),
        "bytes": str(path.stat().st_size),
        "decodable": "unknown",
        "channels": "",
        "sample_rate": "",
        "duration_s": "",
    }
    if path.suffix.lower() != ".wav":
        info["decodable"] = "unverified-non-wav"
        return info
    try:
        with wave.open(str(path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate() or 1
            info["channels"] = str(wf.getnchannels())
            info["sample_rate"] = str(wf.getframerate())
            info["duration_s"] = f"{frames / rate:.3f}"
            info["decodable"] = "yes" if frames > 0 else "empty"
    except wave.Error as exc:
        info["decodable"] = f"no ({exc})"
    except OSError as exc:
        info["decodable"] = f"no ({exc})"
    return info


def read_origin(packet: Path) -> str:
    path = packet / "vo_origin.md"
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return ""


def origin_kind(text: str) -> str:
    m = re.search(r"(?im)^kind:\s*(\S+)", text)
    return (m.group(1) if m else "unspecified").lower()


def report(packet: Path) -> dict[str, str]:
    script = packet / "script.md"
    words = extract_words(script.read_text(encoding="utf-8")) if script.is_file() else ""
    take = find_take(packet)
    origin = read_origin(packet)
    kind = origin_kind(origin) if origin else ("missing" if take is None else "unspecified")
    out: dict[str, str] = {
        "packet": packet.name,
        "drop": selected_vo_drop(packet),
        "words": str(len(words.split())) if words else "0",
        "take": str(take) if take else "",
        "kind": kind,
    }
    if take is not None:
        out.update(inspect_wav(take))
    return out


def render_origin(packet: Path, kind: str, note: str) -> str:
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    drop = selected_vo_drop(packet)
    take = find_take(packet)
    kind = kind.strip().lower()
    if kind not in {"human", "generated", "missing"}:
        kind = "unspecified"
    return f"""# VO origin

kind: {kind}
updated: {generated}
packet: `{packet.name}`
drop: `{drop}`
on_disk: {take.name if take else "none"}

This sidecar is commit-safe text. Audio stays gitignored.
kind=generated means the take is machine speech and must not be described as a human recording.
kind=human means an operator supplied the selected take.
kind=missing means no packet-relative take is on this machine.

{note.strip()}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect narration take and write vo_origin.md")
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--print-words", action="store_true", help="Print extracted WORDS only")
    parser.add_argument(
        "--write-origin",
        choices=("human", "generated", "missing"),
        help="Write vo_origin.md with this kind",
    )
    parser.add_argument("--note", default="", help="Free-text note stored in vo_origin.md")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    if args.print_words:
        script = path / "script.md"
        if not script.is_file():
            print("missing script.md", file=sys.stderr)
            return 1
        sys.stdout.write(extract_words(script.read_text(encoding="utf-8")))
        sys.stdout.write("\n")
        return 0

    row = report(path)
    print(f"packet: {row['packet']}")
    print(f"drop: {row['drop']}")
    print(f"words: {row['words']}")
    print(f"take: {row['take'] or 'missing'}")
    print(f"kind: {row['kind']}")
    if row.get("decodable"):
        print(f"decodable: {row['decodable']}")
        print(f"duration_s: {row.get('duration_s', '')}")

    if args.write_origin:
        text = render_origin(path, args.write_origin, args.note)
        dest = path / "vo_origin.md"
        if args.dry_run:
            sys.stdout.write(text)
            return 0
        dest.write_text(text, encoding="utf-8")
        print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
