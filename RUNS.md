# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-14T04:10:00Z — Run 134

- **Objective:** While selected VO is blocked, stop captions.md from telling a human to "read cues against the selected VO take" without naming the DROP path the board/gate already print.
- **Inspected:** HEAD after Run 133. render.md, vo_session.md, qa.md, pipeline_status, next_action, set_status already share `selected_vo_drop()`. caption_brief.py export names pointed at narration.md only.
- **Action taken:** `caption_brief.py` imports `selected_vo_drop`. Generated captions.md prints `DROP videos/NNN-slug/vo/...`, export names include that path, and the Human box names it. Live Q1 captions.md header/export/human updated. Cue list unchanged. Did not invent wav. Did not bump ready_for_edit. No new CLI. No WAVE 4. No Q2. Did not map forbidden tools.
- **Result:** An operator who opens the captions card to align cues is told the same path the board and status gate check.
- **Verification status:** Files committed via GitHub file API. Official tools not executed in this sandbox (no clone). No wav on disk. Target column left in human_session step 3. Target comment left on hint write-script/expand-script.
- **Important discovery:** After QA notes agreed, the remaining short-path omit was the file humans open to time captions against the take.
- **Blocker:** No selected VO file. HTTPS clone parked. Connected Voice exists but repo policy forbids inventing a selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Follow human_session Live job + steps 5–7. Do not invent wav. Do not `git add -f` the take. Do not drop it at repo-root `vo/`. Do not scaffold Q2. Do not upload. Do not add another Live job banner unless a first-contact lie is proven. Do not re-split selected_vo_drop.

## 2026-09-14T03:06:00Z — Run 133

- **Objective:** While selected VO is blocked, stop qa.md from listing mechanical PASS and an unchecked VO box without naming the Selected VO drop path the board/gate already print.
- **Result:** An operator who opens the QA card to tick VO is told the same path the board and status gate check.
- **Blocker:** No selected VO file.

## 2026-09-14T02:04:00Z — Run 132

- **Objective:** While selected VO is blocked, stop the human reading card from listing only the packet-relative `vo/...` name in the header while the board/gate/render.md already print repo-root DROP.
- **Result:** An operator who opens the reading card during recording is told the same path the board and status gate check.
- **Blocker:** No selected VO file.

## Earlier runs 001–131
See prior commits for full detail.
