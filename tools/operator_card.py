#!/usr/bin/env python3
"""Print the one remaining human publish step. Does not poll secrets.

Runs 368-382 kept wiring recovery edges while videos published stayed 0.
The unpublished video is still the three GitHub Actions secrets. This card
reuses the oauth_setup dispatch line so the human step cannot drift from the
recipe. It does not call YouTube or GitHub and does not add a recovery edge.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from oauth_setup import SECRET_NAMES, recipe  # noqa: E402

HANDOFF = ROOT / "HANDOFF.md"
MASTER_SHA = "4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546"
DISPATCH = (
    "gh workflow dispatch youtube-production.yml "
    "--repo takenthatusernameis-collab/Content-Automation "
    "-f execute=true -f collect_feedback=false"
)
FORBIDDEN_COMMANDS = (
    "gh secret list",
    "gh api",
)


def dispatch_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("gh workflow dispatch youtube-production.yml"):
            return stripped
    return ""


def console_steps(setup_recipe: str) -> str:
    """Numbered console steps from oauth_setup.recipe, so the card cannot drift."""
    lines = []
    for line in setup_recipe.splitlines():
        stripped = line.strip()
        if stripped.startswith("Scope string"):
            break
        if stripped[:1].isdigit() and ". " in stripped[:4]:
            lines.append(stripped)
        elif lines and (
            stripped.startswith("or the full scope")
            or stripped.startswith("youtube.upload alone")
            or stripped.startswith("The first command")
            or stripped.startswith("The browser")
            or stripped.startswith("The second reads")
            or stripped.startswith("After a provider")
            or stripped.startswith("Do not pass")
            or stripped.startswith("Do not dispatch either")
            or stripped.startswith("https://")
            or stripped.startswith("python3 tools/oauth_exchange.py")
            or stripped.startswith("gh secret set ")
            or stripped.startswith("gh workflow dispatch ")
        ):
            lines.append("   " + stripped)
    return "\n".join(lines)


def card_text() -> str:
    steps = console_steps(recipe())
    return f"""OPERATOR CARD (no secret poll, no provider write)

Videos published stay 0 until a human stores three GitHub Actions secrets.
Do not add a recovery edge, scanner, exchange parser, or Q2 scaffold to clear that.
This card reprints the oauth_setup console steps. Do not reconstruct them from NEXT.

Human step:
{steps}

Upload file, if the release is still present:
  q1-media-r253 q1-master-r253.mp4
  sha256 {MASTER_SHA}
Do not re-encode. Do not install the r249 truncated master.

Common pitfalls (read once):
- Scope must include youtube.force-ssl (or full youtube) plus yt-analytics.readonly. youtube.upload alone fails later caption steps.
- Paste secrets into `gh secret set` prompts, never into the command line or any repo file.
- Do not commit the token file or any client secret.
- After secrets are set, dispatch exactly once with execute=true and collect_feedback=false. Wait for a video id before any collect.
- Confirm the master is the r253 sha above; the r249 master is truncated and refused.

Do not run gh secret list. Do not run gh api. Do not dispatch execute again.
"""


def problems(handoff: str, setup_recipe: str, card: str) -> list[str]:
    issues = []
    if MASTER_SHA not in handoff:
        issues.append("HANDOFF missing documented master sha")
    if dispatch_line(setup_recipe) != DISPATCH:
        issues.append("oauth_setup dispatch drifted from operator card")
    if DISPATCH not in card:
        issues.append("card missing dispatch")
    for name in SECRET_NAMES:
        if name not in card:
            issues.append(f"card missing {name}")
    for phrase in ("Desktop app", "YouTube Data API v3", "oauth_exchange.py", "test user"):
        if phrase not in card:
            issues.append(f"card missing console step {phrase}")
    if console_steps(setup_recipe) not in card:
        issues.append("card console steps drifted from oauth_setup recipe")
    for command in FORBIDDEN_COMMANDS:
        if command in card and f"Do not run {command}" not in card:
            issues.append(f"card runs {command}")
    if "subprocess" in card or "videos.insert" in card:
        issues.append("card must not name an insert or a subprocess")
    return issues


def main() -> int:
    handoff = HANDOFF.read_text(encoding="utf-8") if HANDOFF.is_file() else ""
    setup = recipe()
    card = card_text()
    issues = problems(handoff, setup, card)
    if issues:
        print("OPERATOR CARD FAIL")
        for item in issues:
            print(item)
        return 1
    sys.stdout.write(card)
    print("OPERATOR CARD PASS")
    print("human_step=three_actions_secrets dispatch=once master_sha=documented")
    print("no secret poll")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
