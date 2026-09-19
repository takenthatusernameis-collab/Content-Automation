# ROADMAP

## Next (assisted production)
31-51cg. Prior write-path / DROP / packet work — **done (Runs 027-137)**
51ch. Narration adapter (WORDS extract, wav inspect, vo_origin sidecar) + labeled generated fallback after 24h deadline — **done (Run 213; READY_FOR_MEDIA)**
51ci. Deterministic local card generator from assets.md — **done (Run 214; READY_FOR_MEDIA)**
51cj. WORDS-based edit timeline planner (no ffmpeg) — **done (Run 215; READY_FOR_MEDIA)**
51ck. Fail-closed media QA (VO header + card size + assembly gate) — **done (Run 216; READY_FOR_MEDIA)**

## Later (automation)
52. Human override of heuristic Primary (optional; already locked)
53. On-disk selected take (human replacement or local generated file) so gates can advance
54. Caption timing from a real selected take
55. ffmpeg assembly after one packet has VO + cards and timeline.md says ready_to_assemble and media_qa PASS
56. YouTube upload after packet QA passes

## Not yet
- Treating draft.md as script.md before apply --write
- Auto-scaffolding Q2 while Q1 has no on-disk VO
- WAVE 4
- Mapping doctor.py / words.py / prove_locks.py
- Bumping ready_for_edit without Selected VO on disk
- Treating a publish.md edit as an upload
- Treating repo-root `vo/` as Selected VO
- Force-adding ignored media to flip presence rows
- Describing generated VO as a human recording
- Re-implementing selected_vo_drop in a second module
- Committing generated card PNGs
- Running ffmpeg before VO + cards exist on the gate machine
- Treating media_qa FAIL as a reason to invent media

## End-to-end automation buildout

57. **Narration adapter** — READY_FOR_MEDIA (Run 213). Remaining: on-disk take + loudness/silence checks.
58. **Card/visual generator** — READY_FOR_MEDIA (Run 214). Remaining: run on gate machine; do not commit pngs.
59. **Render/assembly pipeline** — PLAN_BUILT / READY_FOR_MEDIA (Run 215 timeline.py). Remaining: ffmpeg export only after ready_to_assemble=yes and media_qa PASS.
60. **Full media QA gate** — READY_FOR_MEDIA (Run 216 media_qa.py). Remaining: live VO/card files on the gate machine; loudness/silence; export decode after ffmpeg exists.
61. **Credential-ready YouTube uploader** — contract only
62. **YouTube feedback ingestion** — NOT_BUILT
63. **Experiment/improvement loop** — contract only
64. **Completion gate** — not claimed
