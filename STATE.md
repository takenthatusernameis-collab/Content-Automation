# STATE

Updated: 2026-08-27T14:15:00+03:00 (Run 005)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> **assisted scaffolding** -> automated -> monitored -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured

## What exists now (after Run 005)
- Operating memory files
- Frozen original master prompt
- Video packet standard + scaffold CLI + packet QA (publish gate + draft gate)
- Sample packet fixture `videos/sample-001-why-systems-beat-motivation/`
- Working niche locked in `docs/channel.md`
- Idea intake CLI `tools/new_idea.py`
- Script-writer prompt `prompts/script_writer.md`
- Title/thumbnail brief CLI `tools/title_thumb_brief.py`
- Editor naming/export conventions `docs/editor.md` (no ffmpeg)
- QA checklist writer `tools/qa_checklist.py` (mechanical + human ticks)

## Pipeline map
| Stage        | Status      | Notes                                      |
|--------------|-------------|--------------------------------------------|
| Research     | manual      | no research brief automation yet           |
| Ideas        | assisted    | `tools/new_idea.py` fills idea card        |
| Scripts      | templated   | beats scaffolded; writer prompt exists     |
| Narration    | blocked     | needs TTS or human VO                      |
| Assets       | manual      | no asset library                           |
| Editing      | templated   | track/export names in `docs/editor.md`     |
| Captions     | unbuilt     |                                            |
| Thumbnails   | assisted    | heuristic brief; no image generator        |
| Titles       | assisted    | heuristic brief; human still picks Primary |
| QA           | assisted    | publish gate + draft gate + checklist writer |
| Rendering    | unbuilt     |                                            |
| Publishing   | blocked     | YouTube API not configured                 |
| Analytics    | unbuilt     |                                            |

## Metrics snapshot
| Metric                         | Previous     | Current        | Notes                          |
|--------------------------------|--------------|----------------|--------------------------------|
| Estimated human min / video    | 245          | 240            | checklist no longer rewritten by hand |
| Automated steps                | 5            | 6              | + qa.md writer                 |
| Remaining manual steps         | most         | most           | script words, VO, edit, publish |
| Videos produced by system      | 0            | 0              | sample packet is a fixture     |
| Channel niche decided          | locked (temp)| locked (temp)  | `docs/channel.md`              |

## Active constraints
- Niche lock is agent-chosen until a human overrides DECISIONS.md
- No secrets or platform APIs
- Do not invent published videos or integrations
- Do not overwrite sample-001 titles/thumbs unless the packet schema changes
- sample-001 `qa.md` may be regenerated when the checklist schema changes; human ticks stay empty on the fixture
