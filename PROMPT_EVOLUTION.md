# PROMPT EVOLUTION

Original prompt is frozen in `ORIGINAL_MASTER_PROMPT.md`.

## Observed issues (Run 001)
- Repo started empty; prompt assumes “inspect recent progress” — first run must bootstrap memory or it will loop on empty READMEs.
- Prompt asks for many status files; that is useful. Creating extra product ideas is not.
- No instruction to treat an empty repo as “create the operating system first.”

## Observed issues (Run 002)
- NEXT.md listed three items; doing all of them is fine if they are one capability (niche + intake + writer prompt).
- Private-repo clone over HTTPS failed in the agent sandbox (`could not read Username`). Use GitHub push tools, not `git clone`, for this repo.
- Full packet QA and idea intake have different success criteria. The master prompt does not distinguish them.

## Observed issues (Run 003)
- NEXT.md item 1 was specific enough that the run did not drift.
- Generating titles from raw mechanism tokens produced unreadable lines; prefer a constrained phrase bank.
- Cannot re-run `validate_packet.py --all` inside a cloned copy of this private repo from the sandbox. Record that limitation instead of claiming a live `--all` PASS.

## Observed issues (Run 004)
- NEXT.md item 1 (`--draft` mode) was the right lever; optional editor conventions were cheap to add beside it.
- Empty-field regexes looked fine until tested on intake packets. Always test the blank-value case.
- Scope cap still holds: do not open TTS/ffmpeg because editor.md exists.

## Observed issues (Run 005)
- NEXT.md item 1 (`qa_checklist.py`) was specific. Digit scanners must ignore headings or they invent “stats” from `0:00` and `Beat 1`.
- Regenerating sample-001 `qa.md` is allowed when the checklist schema changes; titles/thumbs stay frozen.
- Do not auto-check human items just because mechanical QA passed.

## Observed issues (Run 006)
- Research intake is a reminder + scan, not a researcher. Scraping would create fake certainty.
- `\\b` after an optional `%` can drop the percent sign (`87%` -> `87`). Keep `%` inside the match.
- Filled-file guards matter as much as generators; sample-001 already had a source line.

## Observed issues (Run 010)
- Caption intake must stay text-from-script. Estimated 150 wpm times look like real SRT if written to `.srt`.
- Empty-script packets must stay `placeholder` / not-filled so scaffold can rewrite after WORDS exist.
- Path conventions for VO unblocked naming without pretending audio exists.

## Allowed changes
Recorded as proposals in `NEXT_RUN_PROMPT.md` only. Do not edit the original archive.
