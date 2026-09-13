# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-09-09 Run 027 | ~148 estimate | 25 | topic queue + read-only next_topic.py |
| 2026-09-11 Run 079 | ~95 estimate | 70 | prove_locks.py one command |
| 2026-09-13 Run 104 | ~70 estimate | 84 | writer prompts name per-segment spoken-word allocation |
| 2026-09-13 Run 110 | ~64 estimate | 84 | hint/doctor expand-script Command names Target |
| 2026-09-13 Run 111 | ~60 estimate | 84 | Q1 packet folder + idea.md paste (other agent) |
| 2026-09-13 Run 112 | ~52 estimate | 84 | Q1 draft.md first WORDS (manual 941); apply still pending |
| 2026-09-13 Run 113 | ~46 estimate | 84 | Q1 words count 952 IN BAND; script.md applied; status still draft |
| 2026-09-13 Run 114 | ~40 estimate | 84 | titles/thumb heuristic + validate PASS + status ready_for_vo |
| 2026-09-13 Run 115 | ~36 estimate | 84 | vo_session ready-to-record + captions stub; still no selected take |
| 2026-09-13 Run 116 | ~32 estimate | 84 | assets.md 7 planned cards + publish.md stub; VO still human |
| 2026-09-13 Run 117 | ~30 estimate | 84 | tags trimmed + qa mechanical + render presence; VO still human |
| 2026-09-13 Run 118 | ~29 estimate | 84 | after-VO commands on operator page; VO still human |
| 2026-09-13 Run 119 | ~28 estimate | 84 | after-edit card commands on operator page; VO still human |
| 2026-09-13 Run 120 | ~27 estimate | 84 | after-presence publish edit on operator page; VO still human |
| 2026-09-13 Run 121 | ~26 estimate | 84 | Selected VO path locked packet-relative; VO still human |
| 2026-09-13 Run 122 | ~25 estimate | 84 | gitignore local VO/cards/exports; VO still human |
| 2026-09-13 Run 123 | ~25 estimate | 84 | BLOCKED.md VO path matches gates; VO still human |
| 2026-09-13 Run 124 | ~24 estimate | 84 | README names live packet + take path first; VO still human |
| 2026-09-13 Run 125 | ~23 estimate | 84 | agent_session names live job before reconstruct; VO still human |
| 2026-09-13 Run 126 | ~22 estimate | 84 | human_session names live job before doctor/scaffold; VO still human |
| 2026-09-13 Run 127 | ~21 estimate | 84 | production_rules handoff names live job before doctor/queue; VO still human |
| 2026-09-13 Run 128 | ~20 estimate | 84 | next_action/hint record-vo name packet-relative take; VO still human |
| 2026-09-13 Run 129 | ~19 estimate | 84 | set_status missing-VO refuse names packet-relative take; VO still human |

These numbers are **estimates**, not stopwatch data.

## Capability additions
- Run 129: `tools/set_status.py` refuse lines for missing Selected VO name `videos/NNN-slug/vo/NNN-slug-take-selected.wav`. Repo-root `vo/` is called out as not Selected VO. No new CLI. No wav. Status stayed ready_for_vo.
- Run 128: `tools/next_action.py` and `tools/hint.py` record-vo output name `videos/NNN-slug/vo/NNN-slug-take-selected.wav`. Repo-root `vo/` is not the printed drop path. No new CLI. No wav. Status stayed ready_for_vo.
- Run 127: `docs/production_rules.md` Human handoff opens on live Q1 `ready_for_vo` and the packet-relative Selected VO path. doctor / queue_status / next_topic labeled new-packet only. No new page. No wav. No new CLI. Status stayed ready_for_vo.
- Run 126: `docs/human_session.md` opens on live Q1 `ready_for_vo` and the packet-relative Selected VO path. doctor / queue_status / new_packet labeled new-packet only. Steps 1-4 kept as completed path. No new step. No wav. No new CLI. Status stayed ready_for_vo.
- Run 125: `docs/agent_session.md` opens on live Q1 `ready_for_vo` and the packet-relative Selected VO path before clone/WAVE reconstruct. WAVE 3 board printers are confirmation only. No wav. No new CLI. Status stayed ready_for_vo.
- Run 124: README front door names Q1 `ready_for_vo` and the packet-relative Selected VO path before fixture/scaffold commands. No wav. No new CLI. Status stayed ready_for_vo.
- Run 123: `BLOCKED.md` TTS/mic setup now names `videos/NNN-slug/vo/NNN-slug-take-selected.wav`. Repo-root `vo/` is not a parked setup instruction. No wav. No new CLI. Status stayed ready_for_vo.
- Run 122: `.gitignore` excludes packet vo audio, cards images, exports video, and repo-root media dumps. Presence tools still see local files. Operator pages name the ignore. No wav. No new CLI. Status stayed ready_for_vo.
- Run 121: Canonical Selected VO is `videos/NNN-slug/vo/NNN-slug-take-selected.wav`. human_session, NEXT, narration, vo_session.py, and the live Q1 card now say so. Repo-root `vo/` is ignored by `render_brief` / `set_status`. No wav. No new CLI. Status stayed ready_for_vo.
- Run 120: `docs/human_session.md` step 7 names the remaining publish.md human boxes (description + pin) and forbids treating that edit as an upload. No YouTube call. No new CLI. Status stayed ready_for_vo.
- Run 119: `docs/human_session.md` step 6 names the 7 planned cards, local `cards/` folder, and render_brief / qa_checklist --force. `docs/editor.md` and `docs/assets.md` point at the same sequence. No png. No new CLI. Status stayed ready_for_vo.
- Run 118: `docs/human_session.md` step 5 names the Q1 take path and the vo_session --force / set_status ready_for_edit dry-run. `docs/narration.md` points at the same sequence. No wav. No new CLI. Status stayed ready_for_vo.
- Run 117: Q1 publish.md tags trimmed (title-word stopwords removed). qa.md mechanical PASS written from packet files. render.md Status all-missing lists 11 named outputs from format + assets backticks. No binaries. No upload. No new CLI. Status stayed ready_for_vo.
- Run 116: Q1 assets.md lists 7 planned cards from script VISUAL. publish.md has title, description, tags, pin-comment stub. No binaries. No upload. No new CLI. Status stayed ready_for_vo.
- Run 115: Q1 vo_session.md is a real reading card (ready-to-record, 952 words, ~06:21, named take path). captions.md is a 7-cue stub. Heuristic Primary locked. No wav invented. No new CLI. Status stayed ready_for_vo.
- Run 114: first live non-fixture packet passed validate_packet publish gate (script already in band; titles >=5 with one <50; thumb 3 words). Status written to ready_for_vo after dry-run-equivalent OK and no duration WARN. No new CLI. No VO invented.
- Run 113: first official-equivalent IN BAND count (952) on a live non-fixture draft; script.md applied from that draft. Status not bumped. No new CLI.
- Run 112: first non-fixture draft.md contains spoken WORDS aimed at 900-1500. Packet file set completed from template. script.md not applied. No new CLI.
- Run 111: Q1 scaffold + idea.md + queue used. Incomplete file set until Run 112.
- Run 110: hint.py write-script/expand-script Command names hook 28 / payoff 60 / beats 220x4 / CTA 50 / land ~1010.
