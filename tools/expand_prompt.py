#!/usr/bin/env python3
"""Assemble a paste-ready script-expansion prompt from packet files.

Does not rewrite script.md. Does not invent WORDS. Does not write expand.md.
Stdout only. A printed prompt is not a draft and is not permission to
pad videos/sample-001-*.
Refuses a blank or template-default idea.md mechanism so scaffolded
packets cannot expand before the operator pastes a real system.

Run 090: assembled prompt prints parsed idea locks (topic, viewer,
problem, mechanism, why now, related) so the writer cannot ignore the
pasted idea.md. Refuse text names idea_brief --block / --check, not
the new_packet reprint.

Run 108: if expand.md is missing or still a placeholder stub, paste the
live Band-landing budget from expand_brief.render() instead of the stub
line "budgets will appear here". Does not write expand.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from caption_brief import WPM, fmt_ts, script_cues  # noqa: E402
from expand_brief import TARGET_BY_FORMAT, expand_is_filled  # noqa: E402
from expand_brief import render as render_expand  # noqa: E402
from validate_packet import FORMAT_SPOKEN_WORDS, duration_note, field  # noqa: E402

FIXTURE_PREFIX = "sample-001"
BLANK_MECHANISM = {
    "",
    "template-default",
    "generic",
    "(blank)",
    "tbd",
    "todo",
}


def _read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8").strip()


def _clip(text: str, limit: int = 4000) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 20].rstrip() + "\n\n[truncated]\n"


def is_fixture(packet: Path) -> bool:
    return packet.name.startswith(FIXTURE_PREFIX)


def idea_mechanism(idea_text: str) -> str:
    return (
        field(idea_text, "mechanism (the system, not the pep talk)")
        or field(idea_text, "mechanism")
        or ""
    )


def idea_mechanism_blank(idea_text: str) -> bool:
    val = idea_mechanism(idea_text).strip().lower()
    if val in BLANK_MECHANISM:
        return True
    return val.startswith("template-default")


def idea_locks(idea_text: str) -> str:
    """Parse idea.md fields into explicit writer locks."""
    topic = field(idea_text, "topic") or "(blank)"
    viewer = field(idea_text, "viewer") or "(blank)"
    problem = field(idea_text, "problem") or "(blank)"
    mechanism = idea_mechanism(idea_text) or "(blank)"
    why_now = field(idea_text, "why now") or "(blank)"
    related = field(idea_text, "related videos to avoid repeating") or "(blank)"
    return (
        "Use these fields as locks. Do not replace them with a generic weekly-planning pep talk.\n"
        f"- topic: {topic}\n"
        f"- viewer: {viewer}\n"
        f"- problem: {problem}\n"
        f"- mechanism: {mechanism}\n"
        f"- why now: {why_now}\n"
        f"- related videos to avoid repeating: {related}\n"
        "Hook and payoff must name this mechanism. Beats must show the viewer using it.\n"
        "If related is not 'none published yet', do not retell those videos."
    )


def expand_block_for(packet: Path, expand: str) -> str:
    """Prefer a filled expand.md. Otherwise paste a live empty-WORDS budget."""
    if expand_is_filled(expand):
        return expand
    try:
        return render_expand(packet).strip()
    except Exception:
        if expand:
            return expand
        return "(no expand.md — run `python3 tools/expand_brief.py PATH` first)"


def render(packet: Path, *, docs_root: Path | None = None) -> str:
    root = docs_root or packet.resolve().parents[1]
    script = _read(packet / "script.md")
    expand = _read(packet / "expand.md")
    idea = _read(packet / "idea.md")
    research = _read(packet / "research.md")
    channel = _read(root / "docs" / "channel.md")
    rules = _read(root / "docs" / "production_rules.md")
    writer = _read(root / "prompts" / "script_writer.md")
    packet_text = _read(packet / "packet.md")
    fmt = field(packet_text, "format") or "explainer-6-10min"
    cues = script_cues(script) if script else []
    total = sum(int(c["words"]) for c in cues)
    band = FORMAT_SPOKEN_WORDS.get(fmt, (900, 1500))
    lo, hi = band
    target = TARGET_BY_FORMAT.get(fmt, 1200)
    note = duration_note(fmt, total) or ""
    est = fmt_ts((total / WPM) * 60.0 if total else 0.0)
    if total <= 0:
        status = "placeholder"
    elif total < lo:
        status = "short"
    elif total > hi:
        status = "long"
    else:
        status = "in-band"

    fixture_banner = ""
    if is_fixture(packet):
        fixture_banner = (
            "FIXTURE LOCK: This packet is videos/sample-001-*. Do not write "
            "expanded WORDS back into this folder. Use the prompt only as a "
            "dry-run of the assembler. Create a new packet for a real draft.\n\n"
        )

    research_block = research if research else "(no research.md, or file empty)"
    if "unsourced" in research.lower() or "no source" in research.lower():
        research_note = (
            "Treat listed URLs as unverified pointers. Do not invent statistics."
        )
    else:
        research_note = "Use only numbers that already appear here with a source."

    expand_block = expand_block_for(packet, expand)

    return f"""# Script expand prompt (assembled, not a draft)

{fixture_banner}Packet: {packet.name}
Spoken words: {total} (~{est} at {int(WPM)} wpm)
Format: {fmt}
Band: {lo}–{hi} (target {target})
Length status: {status}
Note: {note or "in band"}

You are expanding an existing YouTube explainer script. Return a complete
`script.md` body. Do not add commentary before or after the script.

## Hard rules
- Keep every existing `##` heading text exactly.
- Hook WORDS stay 20–35 spoken words. Do not pad the hook.
- Grow short beats with a worked example or a failure mode, not slogans.
- Total spoken WORDS must land in {lo}–{hi}. Aim near {target}.
- One CTA. One assignment that takes under two minutes. No subscribe pitch.
- No unverifiable statistics. {research_note}
- No personal anecdotes. Use “you” procedures.
- VISUAL lines stay short italic stage directions.
- Do not copy the budget table into WORDS.
- Do not write files. Do not claim VO or cards exist.

## Idea locks
{idea_locks(idea)}

## Channel
{_clip(channel, 1500)}

## Idea
{_clip(idea, 1200)}

## Writer contract (follow)
{_clip(writer, 2500)}

## Production rules (script + format only; ignore tooling lists if long)
{_clip(rules, 2000)}

## Beat budget (size hint only)
{expand_block}

## Current script.md
{script or "(missing script.md)"}

## Output
Replace only WORDS / VISUAL bodies. Preserve headings. After the human
saves the result to PATH/draft.md on a *non-fixture* packet they will run:

```
python3 tools/words.py PATH
python3 tools/apply_script.py PATH --from PATH/draft.md
python3 tools/apply_script.py PATH --from PATH/draft.md --write --refresh
```
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Print a paste-ready expansion prompt from packet files. "
            "Does not write script.md. Refuses a blank idea.md mechanism."
        )
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument(
        "--out",
        help="Optional path to write the prompt (default: stdout only)",
    )
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    idea = _read(path / "idea.md")
    if idea_mechanism_blank(idea):
        print(
            "refusing expand: idea.md mechanism is blank or template-default",
            file=sys.stderr,
        )
        print(
            "Fill a blank idea.md with apply_idea.py PACKET --write, then idea_brief --check. Do not paste by hand. "
            "This command does not write idea.md or script.md.",
            file=sys.stderr,
        )
        print(f"  python3 tools/idea_brief.py {path} --block", file=sys.stderr)
        print(f"  python3 tools/idea_brief.py {path} --check", file=sys.stderr)
        return 2

    text = render(path)
    if args.out:
        out = Path(args.out)
        if out.name == "script.md":
            print("refusing to write script.md", file=sys.stderr)
            return 1
        out.write_text(text, encoding="utf-8")
        print(out)
        return 0

    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
