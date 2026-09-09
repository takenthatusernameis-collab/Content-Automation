# STATE

Updated: 2026-09-09T18:10:00Z (Run 030)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured
- HTTPS clone from this agent sandbox still fails (private repo). Push via GitHub file API.
- Reconstruct + selftest path: `docs/agent_session.md`

## What exists now (after Run 030)
- Operating memory files
- Frozen original master prompt
- Video packet standard + scaffold CLI + packet QA (publish gate + draft gate + optional duration gate)
- Sample packet fixture `videos/sample-001-why-systems-beat-motivation/`
- Working niche locked in `docs/channel.md`
- Topic queue `docs/topic_queue.md` (five queued titles; not drafts)
- Shared queue helpers `tools/queue_lib.py` (slugify, next_id, parse, match)
- Read-only next-topic printer `tools/next_topic.py` (prints predicted `videos/NNN-slug`)
- Read-only queue board `tools/queue_status.py` (queued vs used vs folder; mark-needed / missing-folder)
- Queue closer `tools/mark_topic.py` (dry-run default; folder evidence required; fixture refuse)
- `new_packet.py` next_id treats `sample-001-*` as 001, so the next folder is `002-...`
- `new_packet.py` prints mark_topic dry-run follow-up after scaffold; does not auto-mark
- Operator path `docs/human_session.md`
- Agent path `docs/agent_session.md`
- Fixture contract selftest `tools/selftest.py` (read-only; sample-001 only)
- **Runtime verified 2026-09-09T12:22Z:** reconstructed `/tmp/ca`, `SELFTEST PASS`, exit 0, 153 words, code `expand-script`
- Idea / script / expand / title / QA / research / publish / caption / asset / render / VO / board / next-action / apply-script / set-status / hint / doctor / next-topic / mark-topic / queue-status tools
- Status writer `tools/set_status.py` (dry-run default; `--write` required; fixture and evidence gates unchanged)
- Spoken-duration band: 900-1500 words for `explainer-6-10min` at 150 wpm. Default validate WARNs; `--duration` FAILs. Sample fixture stays PASS + WARN.

## Pipeline map
| Stage        | Status      | Notes                                      |
|--------------|-------------|--------------------------------------------|
| Research     | assisted    | stub written at scaffold; human verifies   |
| Ideas        | assisted    | queue + `new_idea.py`; human still locks   |
| Scripts      | assisted    | beats + duration WARN + expand.md + paste prompt + paste-back gate |
| Narration    | assisted    | session card + path rules; no VO file / TTS|
| Assets       | assisted    | VISUAL -> planned card names; no binaries  |
| Editing      | templated   | tracks in editor.md; timing in format.md   |
| Captions     | assisted    | cue list from WORDS; not timed to a take   |
| Thumbnails   | assisted    | heuristic brief at scaffold if empty       |
| Titles       | assisted    | heuristic brief at scaffold if empty       |
| QA           | assisted    | checklist written at scaffold after titles |
| Publish meta | assisted    | `publish.md` stub; no API                  |
| Rendering    | assisted    | `render.md` presence only; no ffmpeg       |
| Oversight    | monitored   | board + next-action + hint + doctor + gated status write + fixture selftest + queue_status |
| Topic pick   | templated   | queue + next_topic + mark_topic + queue_lib + queue_status |
| Operator path| templated   | `docs/human_session.md`                    |
| Agent path   | templated   | `docs/agent_session.md`                    |
| Publishing   | blocked     | YouTube API not configured                 |
| Analytics    | unbuilt     |                                            |

## Metrics snapshot
| Metric                         | Previous     | Current        | Notes                          |
|--------------------------------|--------------|----------------|--------------------------------|
| Estimated human min / video    | 145          | 144            | queue vs folder scan is a board |
| Automated steps                | 27           | 28             | queue_status.py                |
| Remaining manual steps         | most         | most           | source check, script words, VO, card build, edit, caption align, publish |
| Videos produced by system      | 0            | 0              | sample packet is a fixture     |
| Channel niche decided          | locked (temp)| locked (temp)  | `docs/channel.md`              |
| Fixture selftest runtime       | PASS         | PASS (Run 026) | not re-run; no gated-tool edit |

## Active constraints
- Niche lock is agent-chosen until a human overrides DECISIONS.md
- Topic queue titles are working titles, not scripts
- `next_topic.py` and `queue_status.py` must stay read-only and must not call `new_packet.py`
- `mark_topic.py` is the only queue-status writer; dry-run default; no used without folder
- `new_packet.py` must not auto-`--write` mark_topic
- Do not auto-scaffold Q1 without a human instruction
- No secrets or platform APIs
- Do not invent published videos or integrations
- Do not overwrite sample-001 titles/thumbs/script WORDS
- `apply_script.py` must refuse sample-001 and expand_prompt stdout
- Default apply is dry-run; `--write` is required to replace script.md
- `set_status.py` is the only status writer; dry-run default; no sample-001 promote
- `hint.py`, `doctor.py`, `selftest.py`, `next_topic.py`, and `queue_status.py` are read-only
- Format lock is `explainer-6-10min` only; no shorts split, no ffmpeg recipe
- Default validate 2-tuple stays (errors, incompletes). Duration WARN must not become FAIL unless `--duration`.
- Do not retry HTTPS clone after one failure in a run. Reconstruct per `docs/agent_session.md`.
