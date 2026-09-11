#!/usr/bin/env python3
"""Read-only spoken-word band check for a packet or a draft file.

Humans run this on PATH or PATH/draft.md before apply --write and
before set_status ready_for_vo. It does not write. It does not invent
WORDS. It does not treat draft.md as script.md.

Exit 0 by default even when out of band (print BELOW/ABOVE).
--strict exits 2 when out of band or when the text looks like an
expand_prompt, so a human can gate a paste without applying it.

When BELOW/ABOVE it prints the exact word delta to the locked band
so the next expand pass has a number instead of a guess.
Hook WORDS print a separate 20-35 delta. --strict still keys off
the total band only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

WPM = 150
FORMAT_SPOKEN_WORDS = {"explainer-6-10min": (900, 1500)}
HOOK_BAND = (20, 35)


def _field(text: str, name: str) -> str:
    m = re.search(rf"^-\s*{re.escape(name)}:[ \t]*([^\n]*)$", text, re.M)
    return (m.group(1).strip() if m else "")


def _section(text: str, heading: str) -> str:
    parts = re.split(rf"^##\s+{re.escape(heading)}\s*$", text, maxsplit=1, flags=re.M)
    if len(parts) < 2:
        return ""
    rest = re.split(r"^##\s+", parts[1], maxsplit=1, flags=re.M)[0]
    return rest.strip()


def _spoken_words(block: str) -> list[str]:
    m = re.search(r"WORDS:\s*(.*?)(?:VISUAL:|\Z)", block, re.S)
    blob = m.group(1) if m else block
    blob = re.sub(r"\*[^*]+\*", " ", blob)
    return re.findall(r"[A-Za-z0-9']+", blob)


def _all_spoken_words(script: str) -> list[str]:
    words: list[str] = []
    for m in re.finditer(r"^##\s+(.+)$", script, re.M):
        words.extend(_spoken_words(_section(script, m.group(1).strip())))
    return words


def _spoken_seconds(n_words: int, wpm: float = WPM) -> float:
    if n_words <= 0:
        return 0.0
    return (n_words / wpm) * 60.0


def _fmt_mmss(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    whole = int(round(seconds))
    m, s = divmod(whole, 60)
    return f"{m:02d}:{s:02d}"


def _duration_note(fmt: str, n_words: int) -> str | None:
    if n_words <= 0:
        return None
    band = FORMAT_SPOKEN_WORDS.get(fmt)
    if not band:
        return None
    lo, hi = band
    if lo <= n_words <= hi:
        return None
    est = _fmt_mmss(_spoken_seconds(n_words))
    if n_words < lo:
        return (
            f"spoken {n_words} words (~{est} at {int(WPM)} wpm) "
            f"below {fmt} band {lo}\u2013{hi}"
        )
    return (
        f"spoken {n_words} words (~{est} at {int(WPM)} wpm) "
        f"above {fmt} band {lo}\u2013{hi}"
    )


try:
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
except ImportError:
    all_spoken_words = _all_spoken_words
    duration_note = _duration_note
    field = _field
    fmt_mmss = _fmt_mmss
    section = _section
    spoken_seconds = _spoken_seconds
    spoken_words = _spoken_words

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
    hook = section(script, "Hook (0:00\u20130:12)") or section(script, "Hook")
    return len(spoken_words(hook)) if hook else 0


def delta_line(n: int, lo: int, hi: int, label: str) -> str | None:
    if label == "BELOW":
        need = lo - n
        return f"Delta: add {need} spoken words to reach {lo} (do not pad filler)"
    if label == "ABOVE":
        cut = n - hi
        return f"Delta: cut {cut} spoken words to reach {hi}"
    if label == "IN BAND":
        headroom = hi - n
        floor = n - lo
        return f"Delta: {floor} above floor, {headroom} below ceiling"
    if label == "EMPTY":
        return f"Delta: add {lo}-{hi} spoken words; file has none"
    return None


def hook_delta_line(n: int, lo: int = HOOK_BAND[0], hi: int = HOOK_BAND[1]) -> str:
    if n <= 0:
        return f"Hook Delta: add {lo}-{hi} spoken words; hook is empty"
    if n < lo:
        return f"Hook Delta: add {lo - n} spoken words to reach {lo} (do not pad filler)"
    if n > hi:
        return f"Hook Delta: cut {n - hi} spoken words to reach {hi}"
    return f"Hook Delta: {n - lo} above floor, {hi - n} below ceiling"


def next_line(label: str, source: Path) -> str:
    packet = source.parent if source.is_file() else source
    if label == "IN BAND":
        return (
            f"Next: python3 tools/apply_script.py {packet} --from {packet}/draft.md"
            "  # dry-run first; IN BAND is not --write"
        )
    if label in {"BELOW", "ABOVE", "EMPTY"}:
        return (
            "Next: expand off-repo again using the Delta line; "
            f"overwrite {packet}/draft.md; re-run words.py. Do not apply --write yet."
        )
    return "Next: save a real draft to PATH/draft.md. This command writes nothing."


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
    extra = delta_line(n, lo, hi, label)
    if extra:
        print(extra)
    hook_n = hook_count(script)
    hook_lo, hook_hi = HOOK_BAND
    if hook_n:
        hook_ok = "ok" if hook_lo <= hook_n <= hook_hi else f"not {hook_lo}-{hook_hi}"
        print(f"Hook: {hook_n} words ({hook_ok})")
    else:
        print(f"Hook: 0 words (not {hook_lo}-{hook_hi})")
    print(hook_delta_line(hook_n))
    print(next_line(label, source))
    print("This command writes nothing.")
    print("draft.md is not script.md until apply_script --write.")
    if args.strict and label != "IN BAND":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
