# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-19T02:10:00Z — Run 215

- **Objective:** After card generation, add the next reusable production capability that does not require on-disk VO: a deterministic edit timeline.
- **Inspected:** HEAD after Run 214. Q1 still ready_for_vo, no git-visible take. Roadmap item 59 was NOT_BUILT. editor.md forbids ffmpeg until VO + cards exist.
- **Action taken:** Added `tools/timeline.py` (parse WORDS beats, map assets.md cards, 150 wpm clock, 1.5s hold floor, +20s end-screen, presence gate, optional timeline.md). Imports `selected_vo_drop` from render_brief and `parse_cards` from card_generator. Did not run ffmpeg. Did not bump Q1 status. Did not scaffold Q2. Did not commit media.
- **Result:** Render/assembly moved from NOT_BUILT to PLAN_BUILT / READY_FOR_MEDIA. Human-minute estimate 8 → 7. Automated steps 87 → 88.
- **Verification status:** Isolated extract_beats unit check PASS on a 4-beat fixture. Live Q1 timeline.md not written on a persistent gate machine (no repo checkout). Full selftest against HEAD not executed in this sandbox.
- **Important discovery:** A cut list can be generated from script + assets before media exists. ffmpeg remains correctly gated on ready_to_assemble.
- **Blocker:** Packet-relative Selected VO still absent from any persistent machine the next agent can see. HTTPS clone parked.
- **Recommended next action:** On the gate machine, drop the selected take, generate cards, run `python3 tools/timeline.py PATH --write`. Do not ffmpeg until ready_to_assemble=yes. Do not `git add -f`. Do not upload. Do not scaffold Q2.

## 2026-09-19T01:15:00Z — Run 214

- **Objective:** After narration adapter, add the next reusable production capability: deterministic local card generation from assets.md.
- **Inspected:** HEAD after Run 213. Q1 still ready_for_vo, no git-visible take. Roadmap item 58 (card/visual generator) was NOT_BUILT. assets.md lists 7 planned cards. pngs already gitignored.
- **Action taken:** Added `tools/card_generator.py` (parse assets table, 1920x1080 text-card and vs-diagram render via Pillow, inspect, optional manifest, optional mark-ready). Verified locally on a 3-row fixture: three valid 1920x1080 PNGs. Did not commit binaries. Did not bump Q1 status. Did not scaffold Q2.
- **Result:** Visual/card generator moved from NOT_BUILT to READY_FOR_MEDIA. Human-minute estimate 10 → 8. Automated steps 86 → 87.
- **Verification status:** Local fixture render PASS (3/3, 1920x1080 RGB). Live Q1 cards not written on a persistent gate machine (no repo checkout). selftest card-parse check added in working copy; full fixture selftest not executed against HEAD in this sandbox.
- **Important discovery:** Card generation does not need VO on disk. It was the highest-leverage unblocked step that reduces recurring human labor across every future packet.
- **Blocker:** Packet-relative Selected VO still absent from any persistent machine the next agent can see. HTTPS clone parked. Pillow must be present on the gate machine to render.
- **Recommended next action:** On the gate machine, drop the selected take and run narration_adapter + card_generator. Do not `git add -f`. Do not upload. Do not scaffold Q2.

## 2026-09-19T00:10:00Z — Run 213

- **Objective:** After the 24-hour selected-VO deadline, perform the allowed labeled fallback and the smallest missing capability increment (narration adapter).
- **Inspected:** HEAD after Run 212. OPERATOR_HOLD active. Packet listing markdown-only; no vo/ dir; wav search empty. Current time 2026-09-19T00:03+ EEST / ~00:03Z, past `deadline_at_utc` 2026-09-19T00:00:00Z.
- **Action taken:** Added `tools/narration_adapter.py` (WORDS extract, packet-relative take inspect, `vo_origin.md` writer; imports `selected_vo_drop`). Wrote Q1 `vo_origin.md` with `kind: generated`. Updated escalation record. Synthesized workspace-only MP3 of Q1 WORDS (~5.1MB) via Voice; not committed; not force-added. Did not bump status. Did not scaffold Q2. Did not treat generated audio as a human take.
- **Result:** Narration capability moved from NOT_BUILT to READY_FOR_MEDIA. Q1 still `ready_for_vo` in git because audio is gitignored and not present on a shared disk. Human-minute estimate 11 → 10. Automated steps 85 → 86.
- **Verification status:** Voice tool returned a 5,111,808-byte MP3 in the agent workspace. Adapter source pushed to `main`. No local checkout of the repo, so `selftest.py` was not executed against HEAD in this sandbox. WAV decode path untested against a real wav.
- **Important discovery:** Seventy-five hold honors were correct before the deadline. After the deadline the high-value move is labeled generated narration plus a reusable adapter, not another hold snapshot. Audio still cannot live in git; future gate runs need the file on disk.
- **Blocker:** Packet-relative Selected VO still absent from any persistent machine the next agent can see. HTTPS clone parked.
- **Recommended next action:** Copy or record the take to the packet-relative DROP path on the gate machine. Run `python3 tools/narration_adapter.py PATH` then `vo_session.py --force` and `set_status.py --to ready_for_edit` dry-run. Keep origin kind honest. Do not `git add -f`. Do not upload. Do not scaffold Q2.

## 2026-09-18T23:23:00Z — Run 212

Hold honor. Deadline not yet eligible. Packet markdown-only; no vo/ dir.

## 2026-09-16 — Runs 138–211

Consecutive hold honors after OPERATOR_HOLD was written. Same blocker until Run 213 deadline.
