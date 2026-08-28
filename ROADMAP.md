# ROADMAP

Order is deliberate: understandability and reliability first, then efficiency, then autonomy.

## Now (foundation)
1. Keep operating memory accurate after every run
2. Freeze a video packet contract so every video uses the same folder and files
3. Working niche locked in `docs/channel.md` (human may override)
4. Channel voice spec exists in the same file

## Next (assisted production)
5. Idea intake: one-line topic -> idea card — **done (Run 002)**
6. Script writer prompt + beat validator (hook length, promise, payoff) — **done (prompt Run 002; `--draft` gate Run 004)**
7. Title/thumbnail brief generator from packet fields — **done (Run 003)**
8. Editor project conventions (naming, tracks, end screen) — **done as conventions (Run 004); no ffmpeg**
9. Mechanical QA checklist writer for `qa.md` — **done (Run 005)**
10. Research intake stub (source list + no unverifiable stats reminder) — **done (Run 006)**
11. Scaffold wiring: new packet folders get generated `qa.md` + `research.md` without a second command — **done (Run 007)**
12. Optional title/thumb brief at scaffold time when those files are still empty — **done (Run 008)**
13. Publish metadata stub (`publish.md`: description, tags, pinned comment) from packet fields — **done (Run 009); no upload**
14. Caption / narration path conventions (text first; no vendor lock-in) — **done (Run 010)**
15. Asset/card filename conventions from script VISUAL lines — **done (Run 011); no stock API**
16. Face-free format timing page + named export paths — **done (Run 012); no ffmpeg recipe**
17. Packet-local render presence checklist — **done (Run 013); exists vs missing only**
18. Read-only multi-packet status board — **done (Run 014); no writes**
19. Read-only next human action — **done (Run 015); no writes**
20. VO session reading card from WORDS — **done (Run 016); no wav / no TTS**
21. Spoken-duration band vs locked format — **done (Run 017); WARN default, `--duration` FAIL, next-action expand-script**
22. Beat-budget expand brief — **done (Run 018); does not rewrite WORDS**

## Later (automation)
23. TTS narration path (optional; keep human VO compatible)
24. Caption timing from a real selected take (not 150 wpm estimates)
25. ffmpeg assembly for this one locked format after one packet has VO + cards
26. YouTube upload + metadata only after packet QA passes

## Not yet
- Multi-platform posting
- Autopilot hourly content loops
- Analytics-driven topic selection (needs data)
- Paid stock/API shopping
- Web-scrape-as-research (explicitly rejected until a human verification step exists)
- Whisper / invented SRT from estimates
- Second format (shorts) until a human changes DECISIONS.md
- Auto-advancing packet status from the board
- Making duration WARN a default FAIL (would break sample-001 PASS)
- Auto-writing spoken WORDS from expand.md budgets
