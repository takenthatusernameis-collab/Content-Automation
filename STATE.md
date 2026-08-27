# STATE

Updated: 2026-08-27T10:15:00+03:00 (Run 002)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> **assisted scaffolding** -> automated -> monitored -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured

## What exists now (after Run 002)
- Operating memory files
- Frozen original master prompt
- Video packet standard + scaffold CLI + packet QA
- Sample packet fixture `videos/sample-001-why-systems-beat-motivation/`
- Working niche locked in `docs/channel.md`
- Idea intake CLI `tools/new_idea.py`
- Script-writer prompt `prompts/script_writer.md`

## Pipeline map
| Stage        | Status      | Notes                                      |
|--------------|-------------|--------------------------------------------|
| Research     | manual      | no research brief automation yet           |
| Ideas        | assisted    | `tools/new_idea.py` fills idea card        |
| Scripts      | templated   | beats scaffolded; writer prompt exists     |
| Narration    | blocked     | needs TTS or human VO                      |
| Assets       | manual      | no asset library                           |
| Editing      | manual      | no editor project template yet             |
| Captions     | unbuilt     |                                            |
| Thumbnails   | checklist   | no generator                               |
| Titles       | checklist   | no generator                               |
| QA           | assisted    | `tools/validate_packet.py`                 |
| Rendering    | unbuilt     |                                            |
| Publishing   | blocked     | YouTube API not configured                 |
| Analytics    | unbuilt     |                                            |

## Metrics snapshot
| Metric                         | Previous     | Current        | Notes                          |
|--------------------------------|--------------|----------------|--------------------------------|
| Estimated human min / video    | 280          | 265            | idea card + beat skeleton no longer blank |
| Automated steps                | 2            | 3              | + idea intake                  |
| Remaining manual steps         | most         | most           | script words, VO, edit, publish |
| Videos produced by system      | 0            | 0              | sample packet is a fixture     |
| Channel niche decided          | temporary    | locked (temp)  | `docs/channel.md`              |

## Active constraints
- Niche lock is agent-chosen until a human overrides DECISIONS.md
- No secrets or platform APIs
- Do not invent published videos or integrations
