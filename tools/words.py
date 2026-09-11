#!/usr/bin/env python3
"""Read-only spoken-word band check for a packet or a draft file.

Humans run this on PATH or PATH/draft.md before apply --write and
before set_status ready_for_vo. It does not write. It does not invent
WORDS. It does not treat draft.md as script.md.

Exit 0 by default even when out of band (print BELOW/ABOVE).
--strict exits 2 when out of band or when the text looks like an
expand_prompt, so a human can gate a paste without applying it.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from validate_packet import (  # noqa: E402
    FORMAT_SPOKEN_WORDS,
    WPM,
    all_spoken_words,
    duration_note,
    field,
    fmt_mmss,
    section,
    spoken_seconds,
    spoken_words,
)

PROMPT_MARKERS = (
    "script expand prompt (assembled, not a draft)",
    "fixture lock:",
    "you are expanding an existing youtube explainer script",
    "## beat budget (size hint only)",
    "## writer contract (follow)",
)


def looks_like_expand_prompt(text: str) -> bool:
    low = text.lower()
    return any(m in low for m in PROMPT_MARKERS)


def extract_script(text: str) -> str:
    raw = text.replace("\r\n", "\n").strip()
    fence = re.search(r"```(?:markdown|md)?\n(# Script\b.*?)```", raw, re.S)
    if fence:
        return fence.group(1).strip() + "\n"
    if raw.startswith("# Script"):
        return raw + ("\n" if not raw.endswith("\n") else "")
    if re.search(r"^##\s+Hook", raw, re.M):
        return (
            "# Script\n\nSpoken words only under each beat. Visual notes in italics.\n\n"
            + raw
            + ("\n" if not raw.endswith("\n") else "")
        )
    return raw + ("\n" if raw and not raw.endswith("\n") else "")


def resolve(target: Path) -> tuple[Path, str, str]:
    """Return (source_path, script_text, format_name)."""
    fmt = "explainer-6-10min"
    if target.is_dir():
        packet = target / "packet.md"
        if packet.is_file():
            fmt = field(packet.read_text(encoding="utf-8"), "format") or fmt
        draft = target / "draft.md"
        script = target / "script.md"
        if draft.is_file():
            return draft, extract_script(draft.read_text(encoding="utf-8")), fmt
        if script.is_file():
            return script, extract_script(script.read_text(encoding="utf-8")), fmt
        raise FileNotFoundError(
            f"no draft.md or script.md in {target}\n"
            "Save the off-repo expand to PATH/draft.md first.\n"
            "This command writes nothing."
        )
    if target.is_file():
        parent = target.parent
        packet = parent / "packet.md"
        if packet.is_file():
            fmt = field(packet.read_text(encoding="utf-8"), "format") or fmt
        return target, extract_script(target.read_text(encoding="utf-8")), fmt
    raise FileNotFoundError(
        f"not a file or packet folder: {target}\nThis command writes nothing."
    )


def hook_count(script: str) -> int:
    hook = section(script, "Hook (0:00–0:12)") or section(script, "Hook")
    return len(spoken_words(hook)) if hook else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Print spoken WORDS vs the locked format band. "
            "Default is read-only. Prefer PATH/draft.md when present."
        )
    )
    parser.add_argument("target", help="Packet folder or markdown file")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 2 when out of band or when the text looks like expand_prompt stdout",
    )
    args = parser.parse_args()
    target = Path(args.target)
    try:
        source, script, fmt = resolve(target)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(f"Source: {source}")
    print(f"Format: {fmt}")
    if looks_like_expand_prompt(script):
        print("Result: EXPAND PROMPT (not a draft)")
        print("Save an off-repo writer draft to PATH/draft.md. This command writes nothing.")
        return 2 if args.strict else 0

    n = len(all_spoken_words(script))
    band = FORMAT_SPOKEN_WORDS.get(fmt, (900, 1500))
    lo, hi = band
    est = fmt_mmss(spoken_seconds(n))
    note = duration_note(fmt, n)
    if n <= 0:
        label = "EMPTY"
    elif note is None:
        label = "IN BAND"
    elif n < lo:
        label = "BELOW"
    else:
        label = "ABOVE"
    print(f"Spoken: {n} words (~{est} at {int(WPM)} wpm)")
    print(f"Band: {lo}-{hi}")
    print(f"Result: {label}")
    hook_n = hook_count(script)
    if hook_n:
        hook_ok = "ok" if 20 <= hook_n <= 35 else "not 20-35"
        print(f"Hook: {hook_n} words ({hook_ok})")
    print("This command writes nothing.")
    print("draft.md is not script.md until apply_script --write.")
    if args.strict and label != "IN BAND":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
