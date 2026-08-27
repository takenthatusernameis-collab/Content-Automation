# STATE

Updated: 2026-08-27T21:10:00+03:00 (Run 008)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> **assisted scaffolding** -> automated -> monitored -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured

## What exists now (after Run 008)
- Operating memory files
- Frozen original master prompt
- Video packet standard + scaffold CLI + packet QA (publish gate + draft gate)
- Sample packet fixture `videos/sample-001-why-systems-beat-motivation/`
- Working niche locked in `docs/channel.md`
- Idea intake CLI `tools/new_idea.py`
- Script-writer prompt `prompts/script_writer.md`
- Title/thumbnail brief CLI `tools/title_thumb_brief.py` (scaffold reuses its renderers)
- Editor naming/export conventions `docs/editor.md` (no ffmpeg)
- QA checklist writer `tools/qa_checklist.py` (mechanical + human ticks)
- Research intake stub CLI `tools/research_brief.py` (source list + unsourced-stat reminder; no scrape)
- Scaffold post-step `tools/after_scaffold.py` writes titles/thumbs (if empty), `research.md`, then `qa.md` unless `--no-generate`
- Title-list parser treats empty `1.` / `2.` template lines as untitled

## Pipeline map
| Stage        | Status      | Notes                                      |
|--------------|-------------|--------------------------------------------|
| Research     | assisted    | stub written at scaffold; human verifies   |
| Ideas        | assisted    | `tools/new_idea.py` fills idea card        |
| Scripts      | templated   | beats scaffolded; writer prompt exists     |
| Narration    | blocked     | needs TTS or human VO                      |
| Assets       | manual      | no asset library                           |
| Editing      | templated   | track/export names in `docs/editor.md`     |
| Captions     | unbuilt     |                                            |
| Thumbnails   | assisted    | heuristic brief at scaffold if empty       |
| Titles       | assisted    | heuristic brief at scaffold if empty       |
| QA           | assisted    | checklist written at scaffold after titles |
| Rendering    | unbuilt     |                                            |
| Publishing   | blocked     | YouTube API not configured                 |
| Analytics    | unbuilt     |                                            |

## Metrics snapshot
| Metric                         | Previous     | Current        | Notes                          |
|--------------------------------|--------------|----------------|--------------------------------|
| Estimated human min / video    | 230          | 225            | no second command for title/thumb stub |
| Automated steps                | 8            | 9              | + empty-only title/thumb on scaffold |
| Remaining manual steps         | most         | most           | source check, script words, VO, edit, publish |
| Videos produced by system      | 0            | 0              | sample packet is a fixture     |
| Channel niche decided          | locked (temp)| locked (temp)  | `docs/channel.md`              |

## Active constraints
- Niche lock is agent-chosen until a human overrides DECISIONS.md
- No secrets or platform APIs
- Do not invent published videos or integrations
- Do not overwrite sample-001 titles/thumbs unless the packet schema changes
- sample-001 `qa.md` may be regenerated when the checklist schema changes; human ticks stay empty on the fixture
- sample-001 `research.md` follows the stub schema; do not invent external sources for the fixture
- New packets should use default scaffold generate; `--no-generate` is the opt-out
- Title/thumb generate-on-scaffold is empty-file only (`write_empty_title_brief`); never `--force` sample-001
