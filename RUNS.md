# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-13T21:18:00Z — Run 127

- **Objective:** While selected VO is blocked, stop production_rules Human handoff from presenting doctor / queue_status / next_topic as the live start.
- **Inspected:** HEAD after Run 126. README, agent_session, and human_session already name Q1 + Selected VO. production_rules still said "Start with doctor.py, then queue_status and next_topic."
- **Action taken:** Rewrote the Human handoff opener so the live job is the Q1 packet-relative take. Labeled doctor / queue / next_topic as new-packet only. Pointed at human_session Live job + steps 5–7. Did not add a new page or numbered step. Recorded the decision. Did not invent wav. Did not bump ready_for_edit. No new CLI. No WAVE 4. No Q2. Did not map forbidden tools.
- **Result:** An operator landing on production rules now sees the recording gate before session-start printers.
- **Verification status:** Files committed via GitHub file API. Official tools not executed in this sandbox (no clone). No wav on disk. Target column left in human_session step 3.
- **Important discovery:** After README / agent_session / human_session were pinned, the remaining first-contact lie was the rules page Human handoff still opening on doctor.
- **Blocker:** No selected VO file. HTTPS clone parked. Connected Voice exists but repo policy forbids inventing a selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Follow human_session Live job + steps 5–7. Do not invent wav. Do not `git add -f` the take. Do not drop it at repo-root `vo/`. Do not scaffold Q2. Do not upload. Do not add another Live job banner unless a first-contact lie is proven.

## 2026-09-13T20:08:00Z — Run 126

- **Objective:** While selected VO is blocked, stop the operator session page from presenting doctor / queue_status / new_packet as the live job.
- **Inspected:** HEAD after Run 125. README and agent_session already name Q1 + Selected VO. human_session still opened on Start every session + First real video scaffold.
- **Action taken:** Added a Live job section at the top of `docs/human_session.md`. Labeled Start every session as new-packet only. Labeled steps 1-4 as the completed path, not the live job. Did not add a new numbered step. Recorded the decision. Did not invent wav. Did not bump ready_for_edit. No new CLI. No WAVE 4. No Q2. Did not map forbidden tools.
- **Result:** An operator landing on human_session now sees the recording gate before scaffold commands.
- **Verification status:** Files committed via GitHub file API. Official tools not executed in this sandbox (no clone). No wav on disk. Target column left in human_session step 3.
- **Important discovery:** After README and agent_session were pinned, the remaining first-contact lie for *operators* was human_session leading with doctor + scaffold.
- **Blocker:** No selected VO file. HTTPS clone parked. Connected Voice exists but repo policy forbids inventing a selected take.
- **Recommended next action:** Record selected VO to the packet-relative path. Follow human_session Live job + steps 5–7. Do not invent wav. Do not `git add -f` the take. Do not drop it at repo-root `vo/`. Do not scaffold Q2. Do not upload. Do not add another Live job banner unless a first-contact lie is proven.

## 2026-09-13T19:15:00Z — Run 125

- **Objective:** While selected VO is blocked, stop the agent reconstruct page from presenting WAVE 3 / fixture reconstruct as the live job.
- **Result:** An agent landing on agent_session now sees the recording gate before reconstruct commands.

## 2026-09-13T18:05:00Z — Run 124

- **Objective:** While selected VO is blocked, stop the repo front door from sending a returning operator into fixture/scaffold commands.
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
