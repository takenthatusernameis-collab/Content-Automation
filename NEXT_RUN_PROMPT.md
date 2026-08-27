# NEXT_RUN_PROMPT

Use the original master prompt unchanged, plus these targeted additions:

## Bootstrap rule
If STATE.md exists, trust it over memory. If the repo only has a README, create the memory files and one reusable production artifact before anything else.

## Scope cap
Ship at most one new reusable capability per run after foundation exists. Prefer extending `tools/` and `videos/_template/` over new top-level concepts.

## Evidence rule
If you add a script, run it against a copy of `videos/sample-001-*` fields (dry-run is enough if write would mutate the fixture) and paste the command output into RUNS.md.
Do not claim `git clone` or `validate_packet.py --all` succeeded unless you actually have a local checkout.

## Niche rule
Do not reopen niche debate unless a human changed DECISIONS.md. Specialize prompts toward `docs/channel.md`.

## Intake vs publish QA
Default `validate_packet.py` is the publish/completeness gate.
`validate_packet.py --draft` (alias `--incomplete`) is the intake gate: empty WORDS/titles/thumb are `DRAFT-INCOMPLETE` (exit 0) unless structure/identity is broken.
Do not weaken hook 20–35 or title-count rules in default mode.
Do not treat a partial hook (1–19 or 36+ words) as draft-incomplete; that is still FAIL.
Title numbered items must be on the same line as `N.`. Empty `1.` template lines are not titles.

## Checklist rule
`qa_checklist.py` may mark mechanical boxes from files. It must not mark human VO/card/export/caption boxes done and must not invent numeric quality scores.
Digit notes belong to spoken WORDS only, not headings.

## Research rule
`research_brief.py` writes a stub and a WORDS digit scan. It must not scrape pages or treat `--source` lines as verified facts.
Do not overwrite a filled `research.md` without `--force`.
Do not invent sources for `videos/sample-001-*`.

## Publish rule
`publish_brief.py` writes description/tags/first comment. It must not call YouTube or invent analytics.
Do not overwrite a filled `publish.md` without `--force`.
Do not treat `publish.md` as proof a video went live.

## Caption rule
`caption_brief.py` writes cues from script WORDS at 150 wpm. It must not run Whisper, write `captions.srt`, or treat estimates as a take.
Do not overwrite a filled `captions.md` without `--force`.

## Scaffold rule
`new_idea.py` / `new_packet.py` write generated titles/thumbs (empty titles.md only), `publish.md` (empty only), `captions.md` (empty only), `research.md`, then `qa.md` after copy unless `--no-generate`.
Reuse `after_scaffold.py`, `title_thumb_brief` renderers, `publish_brief.write_empty_publish`, and `caption_brief.write_empty_captions`; do not duplicate title banks.
Never pass `--force` to title/thumb, publish, or captions from scaffold.

## Fixture freeze
Do not overwrite `videos/sample-001-*` titles or thumbnail unless the packet schema itself changed.
`qa.md` on the fixture may be regenerated when the checklist schema changes; leave human ticks unchecked.
`research.md` on the fixture may follow the stub schema; keep it source-free.
`publish.md` on the fixture may follow the stub schema; it is not an upload.
`captions.md` on the fixture may follow the stub schema; estimated times are not a take.

## Private repo
Push via GitHub file APIs. Do not retry HTTPS clone after it fails once in the run.
