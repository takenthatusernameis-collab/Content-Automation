# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-14T03:06:00Z — Run 133

- **Objective:** While selected VO is blocked, stop qa.md from listing mechanical PASS and an unchecked VO box without naming the Selected VO drop path the board/gate already print.
- **Inspected:** HEAD after Run 132. render.md, vo_session.md, pipeline_status, next_action, set_status already share `selected_vo_drop()`. qa_checklist.py notes listed packet files only.
- **Action taken:** `qa_checklist.py` imports `selected_vo_drop`. Notes print `DROP videos/NNN-slug/vo/...` and a repo-root `vo/` warning. Live Q1 qa.md notes updated. Human boxes unchanged and unchecked. Did not invent wav. Did not bump ready_for_edit. No new CLI. No WAVE 4. No Q2. Did not map forbidden tools.
- **Result:** An operator who opens the QA card to tick VO is told the same path the board and status gate check.
- **Verification status:** Files committed via GitHub file API. Official tools not executed in this sandbox (no clone). No wav on disk. Target column left in human_session step 3. Target comment left on hint write-script/expand-script.
- **Important discovery:** After reading-card and render presence agreed, the remaining short-path omit was the file humans open to certify the take.
- **Blocker:** No selected VO file. HTTPS clone parked. Connected Voice exists but repo policy forbids inventing a selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Follow human_session Live job + steps 5–7. Do not invent wav. Do not `git add -f` the take. Do not drop it at repo-root `vo/`. Do not scaffold Q2. Do not upload. Do not add another Live job banner unless a first-contact lie is proven. Do not re-split selected_vo_drop.

## 2026-09-14T02:04:00Z — Run 132

- **Objective:** While selected VO is blocked, stop the human reading card from listing only the packet-relative `vo/...` name in the header while the board/gate/render.md already print repo-root DROP.
- **Result:** An operator who opens the reading card during recording is told the same path the board and status gate check.
- **Blocker:** No selected VO file.

## 2026-09-14T01:10:00Z — Run 131

- **Objective:** While selected VO is blocked, stop render.md from listing only the packet-relative `vo/...` name, and stop duplicating the DROP string in pipeline_status / next_action.
- **Result:** An operator who opens the packet presence file is told the same path the board and status gate check. Future printers can import one helper.
- **Blocker:** No selected VO file.

## Earlier runs 001–130
See prior commits for full detail.
