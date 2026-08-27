# STATE

Updated: 2026-08-28T01:12:00+03:00 (Run 012)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> **assisted scaffolding** -> automated -> monitored -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured

## What exists now (after Run 012)
- Operating memory files
- Frozen original master prompt
- Video packet standard + scaffold CLI + packet QA (publish gate + draft gate)
- Sample packet fixture `videos/sample-001-why-systems-beat-motivation/`
- Working niche locked in `docs/channel.md`
- Idea intake CLI `tools/new_idea.py`
- Script-writer prompt `prompts/script_writer.md`
- Title/thumbnail brief CLI `tools/title_thumb_brief.py` (scaffold reuses its renderers)
- Editor naming/export conventions `docs/editor.md` (no ffmpeg)
- Face-free format timing + named outputs `docs/format.md` (no ffmpeg recipe)
- Narration path conventions `docs/narration.md` (no TTS vendor)
- Asset filename conventions `docs/assets.md` (no stock API)
- QA checklist writer `tools/qa_checklist.py` (mechanical + human ticks)
- Research intake stub CLI `tools/research_brief.py` (source list + unsourced-stat reminder; no scrape)
- Publish metadata stub CLI `tools/publish_brief.py` (description / tags / first comment; no upload)
- Caption intake stub CLI `tools/caption_brief.py` (cues from script WORDS at 150 wpm; no Whisper)
- Asset intake stub CLI `tools/asset_brief.py` (card list from script VISUAL; no download)
- Scaffold post-step `tools/after_scaffold.py` writes titles/thumbs (if empty), `publish.md` (if empty), `captions.md` (if empty), `assets.md` (if empty), `research.md`, then `qa.md` unless `--no-generate`
- Title-list parser treats empty `1.` / `2.` template lines as untitled

## Pipeline map
| Stage        | Status      | Notes                                      |
|--------------|-------------|--------------------------------------------|
| Research     | assisted    | stub written at scaffold; human verifies   |
| Ideas        | assisted    | `tools/new_idea.py` fills idea card        |
| Scripts      | templated   | beats scaffolded; writer prompt exists     |
| Narration    | templated   | path rules only; no VO file / TTS          |
| Assets       | assisted    | VISUAL -> planned card names; no binaries  |
| Editing      | templated   | tracks in editor.md; timing in format.md   |
| Captions     | assisted    | cue list from WORDS; not timed to a take   |
| Thumbnails   | assisted    | heuristic brief at scaffold if empty       |
| Titles       | assisted    | heuristic brief at scaffold if empty       |
| QA           | assisted    | checklist written at scaffold after titles |
| Publish meta | assisted    | `publish.md` stub; no API                  |
| Rendering    | named only  | export path locked; no ffmpeg recipe       |
| Publishing   | blocked     | YouTube API not configured                 |
| Analytics    | unbuilt     |                                            |

## Metrics snapshot
| Metric                         | Previous     | Current        | Notes                          |
|--------------------------------|--------------|----------------|--------------------------------|
| Estimated human min / video    | 210          | 205            | format holds stop re-deciding  |
| Automated steps                | 12           | 12             | docs-only this run             |
| Remaining manual steps         | most         | most           | source check, script words, VO, card build, edit, caption align, publish |
| Videos produced by system      | 0            | 0              | sample packet is a fixture     |
| Channel niche decided          | locked (temp)| locked (temp)  | `docs/channel.md`              |

## Active constraints
- Niche lock is agent-chosen until a human overrides DECISIONS.md
- No secrets or platform APIs
- Do not invent published videos or integrations
- Do not overwrite sample-001 titles/thumbs unless the packet schema changes
- sample-001 `qa.md` may be regenerated when the checklist schema changes; human ticks stay empty on the fixture
- sample-001 `research.md` follows the stub schema; do not invent external sources for the fixture
- sample-001 `publish.md` is a schema fixture; do not treat it as a live upload
- sample-001 `captions.md` is a schema fixture; estimated times are not a take
- sample-001 `assets.md` is a schema fixture; planned filenames are not files on disk
- New packets should use default scaffold generate; `--no-generate` is the opt-out
- Title/thumb generate-on-scaffold is empty-file only (`write_empty_title_brief`); never `--force` sample-001
- Publish generate-on-scaffold is empty-file only (`write_empty_publish`); never upload
- Caption generate-on-scaffold is empty-file only (`write_empty_captions`); never Whisper
- Asset generate-on-scaffold is empty-file only (`write_empty_assets`); never stock download
- Format lock is `explainer-6-10min` only; no shorts split, no ffmpeg recipe
