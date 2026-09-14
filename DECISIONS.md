# DECISIONS

Format: date | decision | why | revisit when

- 2026-09-14 | vo_session.py imports selected_vo_drop. Generated vo_session.md prints repo-root DROP. Record-to uses the same helper. | Run 132: the reading card humans hold while recording still listed packet-relative `vo/...` in the header after render.md agreed. | After a real selected take exists; do not invent a wav; do not add a new CLI; do not re-split the helper
- 2026-09-14 | selected_vo_drop lives in render_brief.py. pipeline_status and next_action import it. Generated render.md prints the repo-root DROP path. Table rows stay packet-relative. | Run 131 | After a real selected take exists; do not invent a wav; do not add a new CLI; do not re-split the helper
- 2026-09-13 | Selected VO lives only under the packet folder. Repo-root `vo/` is not Selected VO. | Run 121 | After a real selected take exists at the packet path; do not add a second search at repo root; do not invent a wav

Earlier decisions remain in force in prior commits.
