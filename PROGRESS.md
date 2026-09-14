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

These numbers are **estimates**, not stopwatch data. Earlier rows remain in prior commits.

## Capability additions
- Run 131: `tools/render_brief.selected_vo_drop()` is the shared Selected VO path helper. `pipeline_status` and `next_action` import it. Generated `render.md` prints `DROP videos/NNN-slug/vo/NNN-slug-take-selected.wav`. Table rows stay packet-relative. No new CLI. No wav. Status stayed ready_for_vo.
- Run 130: `tools/pipeline_status.py` prints DROP when Selected VO is missing, including legal `ready_for_vo`.
