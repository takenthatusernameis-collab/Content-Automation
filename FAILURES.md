# FAILURES

## 2026-09-13 — agent reconstruct page as live job (Run 125)

- **Tried:** Runs 118-124 aligned human/operator pages, BLOCKED, gitignore, and README on the packet-relative take. agent_session still opened on clone + WAVE reconstruct.
- **Evidence:** Recurring agents are told to start on `docs/agent_session.md` when clone fails. That page presented doctor / queue_status / next_topic as the start sequence after WAVE 3 even though Q1 is already `ready_for_vo`.
- **Lesson:** Pin the agent page the same way as README. Reconstruct is for tool work, not a substitute for the recording gate.
- **Avoid:** WAVE 4. Mapping doctor.py. Inventing a wav. Another page that only restates NEXT.md.

## 2026-09-13 — short Selected VO path on operator pages (Run 121)

- **Tried:** Runs 118-120 named `vo/002-...-take-selected.wav` on human_session / NEXT without saying it is inside the packet folder.
- **Evidence:** `tools/render_brief.py` `presence_rows` only checks `packet / vo/...`. A take dropped at repo-root `vo/` would stay missing and `set_status ready_for_edit` would refuse.
- **Lesson:** Name the path the gate actually opens. Do not shorten it for markdown convenience.
- **Avoid:** Adding a second search at repo-root `vo/`. Inventing a wav to prove the path. Another operator step that only restates NEXT.md. Force-adding ignored media.

## 2026-09-13 — STATE lag after parallel Run 111 scaffold

- **Tried:** This run began from Run 110 docs while HEAD already had Q1 commits.
- **Lesson:** List recent commits before treating STATE.md as HEAD. Parallel agents can take the next run number.
- **Avoid:** Writing a second Run 111. Re-scaffolding Q1. Another Target-reprint pass now that a live draft exists.

## 2026-09-13 — reconstruct-loop still closed (Runs 107-110)

- **Tried last five reconstruct runs:** needed.py reconstruct / WAVE 3 / doctor unmapped lists / alias READY (Runs 099-103).
- **Runs 104-110:** Named band targets on writer prompts, template, expand_brief, expand_prompt, human_session, hint Command instead of a new reconstruct path.
- **Avoid:** WAVE 4, mapping doctor.py, a Band-landing reprint CLI, stripping Target comments, applying --write to sample-001.

## 2026-09-12 — reconstruct-loop watch (Runs 099-103)

- **Tried:** Five consecutive runs changed needed.py reconstruct / WAVE 3 / doctor unmapped lists / alias READY.
- **Evidence:** Automated-step count rose 80 → 84. Videos produced stayed 0.
- **Lesson:** Remaining labor after printers agree is a real packet with WORDS in band.
- **Avoid:** WAVE 4 or a MAP need-list edit unless a new READY lie is proven with an isolated tree.

## 2026-09-12 — placeholder overwrite of queue_status.py / words.py / apply_script.py (Runs 098 / 093 / 091 / 076)

- **Lesson:** Never commit a placeholder path. Push the verified local file body only. Check committed size immediately.

## 2026-09-12 — page-alignment chain watch (Runs 082-088)

- **Lesson:** After the printers and operator pages agree, do not spend the next run finding one more markdown file to name idea_brief.

## 2026-09-09 — treating clone failure as selftest unverified

- Clone failure is an access constraint, not a contract failure. Do not retry HTTPS clone as the first action.
