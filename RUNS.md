# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-09-09T12:22:00Z — Run 026

- **Objective:** Close the three-run "runtime unverified" loop. Prove `tools/selftest.py` against sample-001 without padding WORDS or wrapping doctor.
- **Inspected:** STATE/NEXT/ROADMAP/README/selftest after Run 025. NEXT still forbids rewriting gated tools and forbids start.py. Clone still private.
- **Action taken:** Did not retry clone. Listed tools + sample folder via GitHub API, curled `download_url` tokens into `/tmp/ca` (selftest + 8 imported tools + packet/idea/script/titles/thumbnail/qa/assets). Ran `python3 tools/selftest.py`. Added `docs/agent_session.md` so later agents reconstruct instead of restating unverified. Did not change sample-001. Did not rewrite gated tools.
- **Result:**
```
Fixture: sample-001-why-systems-beat-motivation
Gate: PASS
Status: draft
Code: expand-script
Duration WARN: spoken 153 words (~01:01 at 150 wpm) below explainer-6-10min band 900–1500
First live command: python3 tools/expand_prompt.py videos/sample-001-why-systems-beat-motivation
SELFTEST PASS
This command writes nothing.
EXIT:0
```
- **Verification status:** completed. Selftest runtime PASS on reconstructed tree. Memory files updated. No media. No status bump.
- **Important discovery:** GitHub content `download_url` tokens are enough to execute the fixture contract when git clone fails. Repeating "unverified" after that path exists is labor, not caution.
- **Blocker:** Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist. HTTPS clone remains unavailable; do not retry it as the first action.
- **Recommended next action:** Human follows `docs/human_session.md` on a new packet. Agents: reconstruct per `docs/agent_session.md` only after a tool change; do not invent WORDS; do not pad the fixture; do not wrap doctor in start.py.

## 2026-09-09T11:20:00Z — Run 025

- **Objective:** Runs 022–024 left doctor/hint/validate runtime unverified because the sandbox cannot clone the private repo. Encode the fixture contract as an executable selftest so the next clone or local session can prove gates without rereading STATE.
- **Inspected:** STATE/NEXT/ROADMAP/README/doctor/hint/next_action/pipeline_status/validate/set_status/apply_script after Run 024. Sample still the only packet. NEXT forbids wrapping doctor in start.py and forbids padding WORDS.
- **Action taken:** Added `tools/selftest.py` (read-only; sample-001 only). Asserts publish PASS, duration WARN + `--duration` FAIL, draft status, no drift, next-action `expand-script`, first live hint command has no `--write`, fixture lock present, set_status and apply_script refuse the fixture. Did not change sample-001. Did not rewrite gated tools. Did not add start.py.
- **Result:** Selftest file present. Memory files updated. No media. No status bump. Live import against the fixture still cannot run in this sandbox (no checkout of videos/ + render_brief.py together).
- **Verification status:** completed for file presence and encoded contracts. Runtime later proven in Run 026.
- **Important discovery:** Repeating “runtime unverified” without a check file is itself the labor. A selftest is cheaper than another prose restatement. Flag: three consecutive runs could not execute Python against the fixture from this agent path.
- **Blocker:** Private-repo clone still unavailable from this sandbox. Still waiting on a human-owned non-fixture draft in band. ffmpeg recipe parked until VO + cards exist.
- **Recommended next action:** On a full checkout, run `python3 tools/selftest.py`. Human follows `docs/human_session.md` on a new packet. Agents: do not invent WORDS, do not pad the fixture, do not wrap doctor in start.py.

## 2026-09-09T10:20:00Z — Run 024

- **Objective:** After doctor exists, stop leaving humans to reconstruct the expand → apply → set_status path from NEXT.md and 21 tool files. Still no WORDS invention, no fixture pad, no wav, no TTS, no ffmpeg, no OAuth.
- **Recommended next action:** Human follows `docs/human_session.md` on a new packet.

## Earlier runs 001–023
See prior commits for full detail.
