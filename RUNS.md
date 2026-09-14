# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-14T01:10:00Z — Run 131

- **Objective:** While selected VO is blocked, stop render.md from listing only the packet-relative `vo/...` name, and stop duplicating the DROP string in pipeline_status / next_action.
- **Inspected:** HEAD after Run 130. Board, set_status refuse, and next_action already print `videos/NNN-slug/vo/...`. Q1 render.md table still showed `vo/002-...-take-selected.wav` with no repo-root DROP. pipeline_status and next_action each built that string.
- **Action taken:** Moved `selected_vo_drop()` into `tools/render_brief.py`. pipeline_status and next_action import it (`selected_vo_path` remains an alias for set_status). render() now prints DROP plus the repo-root rule. Updated live Q1 render.md the same way. Did not invent wav. Did not bump ready_for_edit. No new CLI. No WAVE 4. No Q2. Did not map forbidden tools.
- **Result:** An operator who opens the packet presence file is told the same path the board and status gate check. Future printers can import one helper.
- **Verification status:** Files committed via GitHub file API. Official tools not executed in this sandbox (no clone). No wav on disk. Target column left in human_session step 3. Target comment left on hint write-script/expand-script.
- **Important discovery:** After printers and first-contact pages agreed, the remaining short-path omit was the generated presence file humans re-read after a recording session.
- **Blocker:** No selected VO file. HTTPS clone parked. Connected Voice exists but repo policy forbids inventing a selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Follow human_session Live job + steps 5–7. Do not invent wav. Do not `git add -f` the take. Do not drop it at repo-root `vo/`. Do not scaffold Q2. Do not upload. Do not add another Live job banner unless a first-contact lie is proven. Do not re-split selected_vo_drop.

## 2026-09-14T00:20:00Z — Run 130

- **Objective:** While selected VO is blocked, stop pipeline_status from reporting missing disk without naming the Selected VO drop path the gate opens.
- **Result:** An operator who runs the production board on Q1 is told the same path render_brief / next_action / set_status check.
- **Blocker:** No selected VO file.

## 2026-09-13T23:16:00Z — Run 129

- **Objective:** While selected VO is blocked, stop set_status from refusing ready_for_edit with a generic "Selected VO missing on disk" that hides the path the gate opens.
- **Result:** An operator who dry-runs set_status after dropping a take in the wrong place is told the same path render_brief / next_action check.
- **Blocker:** No selected VO file.

## 2026-09-13T22:19:00Z — Run 128

- **Result:** An operator who runs next_action or hint on Q1 is told the same path render_brief / set_status check.

## Earlier runs 001–127
See prior commits for full detail.
