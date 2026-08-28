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

## Asset rule
`asset_brief.py` writes planned cards from script VISUAL lines. It must not download stock, write PNG/JPG binaries, or mark Status `ready`.
Do not overwrite a filled `assets.md` without `--force`.
A suggested filename is not a file on disk.

## Caption rule
`caption_brief.py` writes cues from script WORDS at 150 wpm. It must not run Whisper, write `captions.srt`, or treat estimates as a take.

## Publish rule
`publish_brief.py` writes description/tags/first comment. It must not call YouTube or invent analytics.

## Format rule
`docs/format.md` is the timing lock for `explainer-6-10min`. Do not add an ffmpeg recipe or a second format unless DECISIONS.md says so.
A named path (`exports/NNN-slug-vN.mp4`) is not proof the file exists.

## Render rule
`render_brief.py` writes exists-vs-missing rows for named format outputs. It must not run ffmpeg, write wav/png/mp4, or treat `all-missing` as failure.
Do not overwrite a filled `render.md` without `--force`.
Do not commit fake media to flip rows to `present`.

## Board rule
`pipeline_status.py` is read-only. It must not rewrite `packet.md` status, render.md, or qa.md.
`--strict` is for FAIL or drift only. `draft` + PASS + all-missing is a valid fixture state, not drift.

## Next-action rule
`next_action.py` is read-only. It must not rewrite `packet.md` status or create media.
One recommended step per packet. Prefer gate FAIL, then drift, then the first real production file the human can add.

## Scaffold rule
`new_idea.py` / `new_packet.py` write generated titles/thumbs (empty titles.md only), `publish.md` (empty only), `captions.md` (empty only), `assets.md` (empty only), `render.md` (empty only), `research.md`, then `qa.md` after copy unless `--no-generate`.
Reuse `after_scaffold.py` and `render_brief.write_empty_render`; never pass `--force` from scaffold.

## Fixture freeze
Do not overwrite `videos/sample-001-*` titles or thumbnail unless the packet schema itself changed.
`assets.md` and `render.md` on the fixture may follow the stub schema; planned filenames are not binaries.

## Private repo
Push via GitHub file APIs. Do not retry HTTPS clone after it fails once in the run.
