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

## Duration rule
Spoken WORDS for `explainer-6-10min` belong in 900-1500 at 150 wpm. Default validate prints WARN. `--duration` may FAIL. Do not pad sample-001. Do not make WARN the default FAIL.

## Expand rule
`expand_brief.py` writes a beat budget. It must not rewrite `script.md` or invent spoken lines.
Do not overwrite a filled `expand.md` without `--force`.
A Status `short` budget is not a draft.

## Expand-prompt rule
`expand_prompt.py` prints a paste pack. It must not write `script.md`.
Refuse `--out` when the destination is `script.md`.
On `sample-001-*` print the fixture lock banner. Do not paste the output back onto the fixture.

## Apply-script rule
`apply_script.py` dry-runs by default. `--write` is required.
Refuse `sample-001-*`.
Refuse text that looks like expand_prompt stdout.
Do not bump packet status.
`--refresh` may rewrite expand/vo_session/captions only after a successful write on a non-fixture packet.

## Status-write rule
`set_status.py` dry-runs by default. `--write` is required.
Refuse promoting `sample-001-*`.
Refuse skip-ahead.
Refuse `ready_for_vo` / `ready_for_edit` while duration WARN is present.
Refuse later statuses without Selected VO / Master export on disk.
Do not create media.
`pipeline_status.py`, `next_action.py`, and `hint.py` stay read-only.

## Hint rule
`hint.py` is read-only. Map next_action codes to copy-paste CLI.
Never print `--write` as the first command.
On `sample-001-*` print a fixture lock instead of apply_script --write.

## Board rule
`pipeline_status.py` is read-only. It must not rewrite `packet.md` status, render.md, or qa.md.
Duration WARN is not FAIL and not drift.

## Next-action rule
`next_action.py` is read-only. One recommended step per packet. Prefer gate FAIL, then drift, then duration WARN (`expand-script`), then the first real production file the human can add.

## Scaffold rule
Reuse `after_scaffold.py` and `write_empty_*`; never pass `--force` from scaffold.

## Fixture freeze
Do not overwrite `videos/sample-001-*` titles, thumbnail, or script WORDS unless the packet schema itself changed.
Do not expand sample-001 WORDS to clear duration WARN.

## Private repo
Push via GitHub file APIs. Do not retry HTTPS clone after it fails once in the run.
