# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-09-13 Run 114 | ~40 estimate | 84 | titles/thumb heuristic + validate PASS + status ready_for_vo |
| 2026-09-13 Run 121 | ~26 estimate | 84 | Selected VO path locked packet-relative; VO still human |
| 2026-09-13 Run 128 | ~20 estimate | 84 | next_action/hint record-vo name packet-relative take; VO still human |
| 2026-09-13 Run 129 | ~19 estimate | 84 | set_status missing-VO refuse names packet-relative take; VO still human |
| 2026-09-14 Run 130 | ~18 estimate | 84 | pipeline_status DROP names packet-relative take; VO still human |
| 2026-09-14 Run 131 | ~17 estimate | 84 | render.md DROP + shared selected_vo_drop; VO still human |
| 2026-09-14 Run 132 | ~16 estimate | 84 | vo_session.md DROP uses selected_vo_drop; VO still human |
| 2026-09-14 Run 133 | ~15 estimate | 84 | qa.md Notes DROP uses selected_vo_drop; VO still human |
| 2026-09-14 Run 134 | ~14 estimate | 84 | captions.md DROP uses selected_vo_drop; VO still human |
| 2026-09-14 Run 135 | ~13 estimate | 85 | selftest DROP-import lock + editor.md DROP; VO still human |

These numbers are **estimates**, not stopwatch data. Earlier rows remain in prior commits.

## Capability additions
- Run 135: `tools/selftest.py` fails if VO printers drop `selected_vo_drop` from `render_brief.py`. `docs/editor.md` names the packet-relative DROP. No new CLI. No wav. Status stayed ready_for_vo.
- Run 134: `tools/caption_brief.py` imports `selected_vo_drop()`. Generated `captions.md` prints `DROP videos/NNN-slug/vo/NNN-slug-take-selected.wav`. Live Q1 captions.md header/export/human updated. Cue list unchanged. No new CLI. No wav. Status stayed ready_for_vo.
- Run 133: `tools/qa_checklist.py` imports `selected_vo_drop()`. Generated `qa.md` Notes print DROP. Human VO box stays unchecked.
- Run 132: `tools/vo_session.py` imports `selected_vo_drop()`. Generated `vo_session.md` prints DROP. Record-to uses the same helper.
- Run 131: `tools/render_brief.selected_vo_drop()` is the shared Selected VO path helper. `pipeline_status` and `next_action` import it. Generated `render.md` prints DROP.
