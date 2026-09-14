# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-14T02:04:00Z — Run 132

- **Objective:** While selected VO is blocked, stop the human reading card from listing only the packet-relative `vo/...` name in the header while the board/gate/render.md already print repo-root DROP.
- **Inspected:** HEAD after Run 131. render.md, pipeline_status, next_action, set_status already share `selected_vo_drop()`. vo_session.py still printed `Selected take path: vo/...` and rebuilt Record-to as `videos/{packet.name}/{vo_rel}`.
- **Action taken:** `vo_session.py` imports `selected_vo_drop`. Header prints `DROP videos/NNN-slug/vo/...`. Record-to uses the same helper. Live Q1 vo_session.md header updated. Spoken WORDS unchanged. Did not invent wav. Did not bump ready_for_edit. No new CLI. No WAVE 4. No Q2. Did not map forbidden tools.
- **Result:** An operator who opens the reading card during recording is told the same path the board and status gate check.
- **Verification status:** Files committed via GitHub file API. Official tools not executed in this sandbox (no clone). No wav on disk. Target column left in human_session step 3. Target comment left on hint write-script/expand-script.
- **Important discovery:** After presence files agreed, the remaining short-path omit was the file humans actually hold while recording.
- **Blocker:** No selected VO file. HTTPS clone parked. Connected Voice exists but repo policy forbids inventing a selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Follow human_session Live job + steps 5–7. Do not invent wav. Do not `git add -f` the take. Do not drop it at repo-root `vo/`. Do not scaffold Q2. Do not upload. Do not add another Live job banner unless a first-contact lie is proven. Do not re-split selected_vo_drop.

## 2026-09-14T01:10:00Z — Run 131

- **Objective:** While selected VO is blocked, stop render.md from listing only the packet-relative `vo/...` name, and stop duplicating the DROP string in pipeline_status / next_action.
- **Result:** An operator who opens the packet presence file is told the same path the board and status gate check. Future printers can import one helper.
- **Blocker:** No selected VO file.

## 2026-09-14T00:20:00Z — Run 130

- **Objective:** While selected VO is blocked, stop pipeline_status from reporting missing disk without naming the Selected VO drop path the gate opens.
- **Result:** An operator who runs the production board on Q1 is told the same path render_brief / next_action / set_status check.
- **Blocker:** No selected VO file.

## Earlier runs 001–129
See prior commits for full detail.
