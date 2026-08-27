# PROMPT EVOLUTION

Original prompt is frozen in `ORIGINAL_MASTER_PROMPT.md`.

## Observed issues (Run 010)
- Caption intake must stay text-from-script. Estimated 150 wpm times look like real SRT if written to `.srt`.
- Empty-script packets must stay `placeholder` / not-filled so scaffold can rewrite after WORDS exist.
- Path conventions for VO unblocked naming without pretending audio exists.

## Observed issues (Run 011)
- Asset intake must stay names-from-VISUAL. A `cards/*.png` commit reads as ready media.
- Strip “plain text card:” prefixes before slugify or filenames get noisy.
- Old two-column sample tables still count as filled; schema upgrades of the fixture are explicit, not scaffold `--force`.

## Observed issues (Run 012)
- Format lock belongs in docs, not in a new CLI, while no VO or cards exist.
- Named export paths are the same contract class as planned card names: a plan, not a file.
- ffmpeg recipe would be novelty; it cannot be verified without media on disk.

## Allowed changes
Recorded as proposals in `NEXT_RUN_PROMPT.md` only. Do not edit the original archive.
