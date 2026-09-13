# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-13T22:19:00Z — Run 128

- **Objective:** While selected VO is blocked, stop next_action / hint from printing a short `vo/` drop path that gates do not open.
- **Inspected:** HEAD after Run 127. README / agent_session / human_session / production_rules / BLOCKED already name `videos/NNN-slug/vo/...`. next_action Why used `vo/{vid}-{slug}-take-selected.wav`. hint record-vo Command said "the named vo/ path".
- **Action taken:** next_action.selected_vo_path() now prints `videos/{vid}-{slug}/vo/{vid}-{slug}-take-selected.wav`. hint.py record-vo Command uses that helper and forbids repo-root `vo/` plus `git add -f`. Did not add a Live job banner. Did not invent wav. Did not bump ready_for_edit. No new CLI. No WAVE 4. No Q2. Did not map forbidden tools.
- **Result:** An operator who runs next_action or hint on Q1 is told the same path render_brief / set_status check.
- **Verification status:** Files committed via GitHub file API. Official tools not executed in this sandbox (no clone). No wav on disk. Target column left in human_session step 3. Target comment left on hint write-script/expand-script.
- **Important discovery:** After first-contact pages were pinned, the remaining short-path lie was inside the record-vo printers themselves.
- **Blocker:** No selected VO file. HTTPS clone parked. Connected Voice exists but repo policy forbids inventing a selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Follow human_session Live job + steps 5–7. Do not invent wav. Do not `git add -f` the take. Do not drop it at repo-root `vo/`. Do not scaffold Q2. Do not upload. Do not add another Live job banner unless a first-contact lie is proven.

## 2026-09-13T21:18:00Z — Run 127

- **Objective:** While selected VO is blocked, stop production_rules Human handoff from presenting doctor / queue_status / next_topic as the live start.
- **Result:** An operator landing on production rules now sees the recording gate before session-start printers.

## 2026-09-13T20:08:00Z — Run 126

- **Result:** An operator landing on human_session now sees the recording gate before scaffold commands.

## 2026-09-13T19:15:00Z — Run 125

- **Result:** An agent landing on agent_session now sees the recording gate before reconstruct commands.

## 2026-09-13T18:05:00Z — Run 124

- **Result:** Opening README now names the remaining human gate before the fixture command list.

## 2026-09-13T17:05:00Z — Run 123

- **Result:** A human reading BLOCKED.md before recording will place the take where `render_brief` / `set_status` look. Human gate is still the selected take.

## 2026-09-13T16:20:00Z — Run 122

- **Result:** A recording session can drop the take at the packet path without that file entering git by default.

## 2026-09-13T15:10:00Z — Run 121

- **Result:** A recording session can place the file where the gate actually looks.

## 2026-09-13T14:15:00Z — Run 120

- **Result:** Operator path now covers ready_for_vo through the first legal publish-metadata edit.

## 2026-09-13T13:10:00Z — Run 119

- **Result:** Operator path now covers ready_for_vo through the first legal card refresh.

## 2026-09-13T12:25:00Z — Run 118

- **Result:** Operator path now covers ready_for_vo through the first legal status bump.

## 2026-09-13T11:14:00Z — Run 117

- **Result:** Upload tags are usable. Editor has a named presence list that will stay honest until files exist.

## Earlier runs 001–116
See prior commits for full detail.
