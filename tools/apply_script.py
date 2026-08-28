#!/usr/bin/env python3
"""Apply a human-pasted script.md body to a non-fixture packet.

Does not invent WORDS. Does not expand the sample fixture. Does not bump
packet status. A dry-run is the default so a bad paste cannot land.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from caption_brief import WPM, fmt_ts, script_cues  # noqa: E402
from validate_packet import FORMAT_SPOKEN_WORDS, duration_note, field  # noqa: E402

FIXTURE_PREFIX = "sample-001"
PROMPT_MARKERS = (
    "script expand prompt (assembled, not a draft)",
    "fixture lock:",
    "you are expanding an existing youtube explainer script",
    "## beat budget (size hint only)",
    "## writer contract (follow)",
)


def headings(text: str) -> list[str]:
    return [m.strip() for m in re.findall(r"^##\\s+(.+)$", text, re.M)]


def heading_key(label: str) -> str:
    low = label.lower().strip()
    if low.startswith("hook"):
        return "hook"
    if "payoff" in low:
        return "payoff"
    m = re.match(r"beat\\s+(\\d+)", low)
    if m:
        return f"beat-{m.group(1)}"
    if low.startswith("cta"):
        return "cta"
    return f"other:{low}"


def looks_like_expand_prompt(text: str) -> bool:
    low = text.lower()
    return any(m in low for m in PROMPT_MARKERS)


def extract_script(text: str) -> str:
    """Take a pasted body; strip a wrapping fence if the model added one."""
    raw = text.replace("\\r\\n", "\\n").strip()
    fence = re.search(r"```(?:markdown|md)?\\n(# Script\\b.*?)```", raw, re.S)
    if fence:
        return fence.group(1).strip() + "\\n"
    if raw.startswith("# Script"):
        return raw + ("\\n" if not raw.endswith("\\n") else "")
    if re.search(r"^##\\s+Hook", raw, re.M):
        return (
            "# Script\\n\\nSpoken words only under each beat. Visual notes in italics.\\n\\n"
            + raw
            + ("\\n" if not raw.endswith("\\n") else "")
        )
    return raw + ("\\n" if raw and not raw.endswith("\\n") else "")


def spoken_total(script: str) -> int:
    return sum(int(c["words"]) for c in script_cues(script))


def is_fixture(packet: Path) -> bool:
    return packet.name.startswith(FIXTURE_PREFIX)


def check(packet: Path, incoming: str) -> list[str]:
    errors: list[str] = []
    if is_fixture(packet):
        errors.append(
            f"refusing fixture {packet.name}: do not write expanded WORDS onto sample-001"
        )
    if looks_like_expand_prompt(incoming):
        errors.append(
            "incoming text looks like expand_prompt.py stdout, not a script.md body"
        )
    current_path = packet / "script.md"
    current = current_path.read_text(encoding="utf-8") if current_path.is_file() else ""
    cur_keys = [heading_key(h) for h in headings(current)]
    new_keys = [heading_key(h) for h in headings(incoming)]
    if not new_keys:
        errors.append("incoming text has no ## headings")
    else:
        need = {"hook", "payoff", "cta"}
        have = set(new_keys)
        missing = sorted(need - have)
        if missing:
            errors.append(f"incoming script missing sections: {', '.join(missing)}")
        beats = [k for k in new_keys if k.startswith("beat-")]
        if not (4 <= len(beats) <= 7):
            errors.append(f"incoming beat count {len(beats)} not in 4–7")
        if cur_keys:
            cur_beats = [k for k in cur_keys if k.startswith("beat-")]
            if cur_beats and beats and cur_beats != beats:
                errors.append(
                    f"incoming beat ids {beats} do not match current {cur_beats}"
                )
    hook_cues = [c for c in script_cues(incoming) if heading_key(str(c["label"])) == "hook"]
    if hook_cues:
        n = int(hook_cues[0]["words"])
        if n and (n < 20 or n > 35):
            errors.append(f"hook word count {n} not in 20–35")
    return errors


def report(packet: Path, current: str, incoming: str, errors: list[str]) -> str:
    packet_text = (
        (packet / "packet.md").read_text(encoding="utf-8")
        if (packet / "packet.md").is_file()
        else ""
    )
    fmt = field(packet_text, "format") or "explainer-6-10min"
    band = FORMAT_SPOKEN_WORDS.get(fmt, (900, 1500))
    before = spoken_total(current)
    after = spoken_total(incoming)
    before_note = duration_note(fmt, before) or "in band"
    after_note = duration_note(fmt, after) or "in band"
    lines = [
        f"Packet: {packet.name}",
        f"Format: {fmt} band {band[0]}–{band[1]}",
        f"Spoken before: {before} (~{fmt_ts((before / WPM) * 60.0 if before else 0)} at {int(WPM)} wpm) {before_note}",
        f"Spoken after:  {after} (~{fmt_ts((after / WPM) * 60.0 if after else 0)} at {int(WPM)} wpm) {after_note}",
        f"Headings in: {', '.join(headings(incoming)) or '(none)'}",
    ]
    if errors:
        lines.append("Result: BLOCKED")
        lines.extend(f"  - {e}" for e in errors)
    else:
        lines.append("Result: OK to write script.md (does not bump status)")
    return "\\n".join(lines) + "\\n"


def refresh_derived(packet: Path) -> list[str]:
    """Rewrite expand / vo_session / captions from the new WORDS."""
    notes: list[str] = []
    from expand_brief import render as render_expand
    from vo_session import render as render_vo
    from caption_brief import render as render_cap

    (packet / "expand.md").write_text(render_expand(packet), encoding="utf-8")
    notes.append(f"refreshed {packet.name}/expand.md")
    (packet / "vo_session.md").write_text(render_vo(packet), encoding="utf-8")
    notes.append(f"refreshed {packet.name}/vo_session.md")
    (packet / "captions.md").write_text(render_cap(packet), encoding="utf-8")
    notes.append(f"refreshed {packet.name}/captions.md")
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Apply a pasted script.md body to a non-fixture packet. "
            "Default is dry-run. Does not invent WORDS or bump status."
        )
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument(
        "--from",
        dest="source",
        help="File with the new script body (default: stdin)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write script.md. Without this flag, print a report only.",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="After --write, refresh expand.md, vo_session.md, captions.md",
    )
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    if args.source:
        incoming_raw = Path(args.source).read_text(encoding="utf-8")
    else:
        incoming_raw = sys.stdin.read()
    incoming = extract_script(incoming_raw)
    current = (path / "script.md").read_text(encoding="utf-8") if (path / "script.md").is_file() else ""
    errors = check(path, incoming)
    sys.stdout.write(report(path, current, incoming, errors))
    if errors:
        return 1
    if not args.write:
        sys.stdout.write("Dry-run only. Pass --write to replace script.md.\\n")
        return 0

    dest = path / "script.md"
    dest.write_text(incoming, encoding="utf-8")
    print(dest)
    if args.refresh:
        for note in refresh_derived(path):
            print(note)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
