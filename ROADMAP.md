# ROADMAP

Order is deliberate: understandability and reliability first, then efficiency, then autonomy.

## Now (foundation)
1. Keep operating memory accurate after every run
2. Freeze a video packet contract so every video uses the same folder and files
3. Working niche locked in `docs/channel.md` (human may override)
4. Channel voice spec exists in the same file

## Next (assisted production)
5. Idea intake: one-line topic -> idea card — **done (Run 002)**
6. Script writer prompt + beat validator — **done (prompt Run 002; `--draft` gate Run 004)**
7. Title/thumbnail brief generator from packet fields — **done (Run 003)**
8. Editor project conventions — **done as conventions (Run 004); no ffmpeg**
9. Mechanical QA checklist writer for `qa.md` — **done (Run 005)**
10. Research intake stub — **done (Run 006)**
11. Scaffold wiring: generated stubs without a second command — **done (Run 007)**
12. Optional title/thumb brief at scaffold time when empty — **done (Run 008)**
13. Publish metadata stub — **done (Run 009); no upload**
14. Caption / narration path conventions — **done (Run 010)**
15. Asset/card filename conventions — **done (Run 011); no stock API**
16. Face-free format timing page + named export paths — **done (Run 012); no ffmpeg recipe**
17. Packet-local render presence checklist — **done (Run 013)**
18. Read-only multi-packet status board — **done (Run 014)**
19. Read-only next human action — **done (Run 015)**
20. VO session reading card from WORDS — **done (Run 016)**
21. Spoken-duration band vs locked format — **done (Run 017)**
22. Beat-budget expand brief — **done (Run 018)**
23. Paste-ready expand prompt assembler — **done (Run 019)**
24. Paste-back script apply gate — **done (Run 020); refuses fixture; dry-run default**
25. Evidence-gated status writer — **done (Run 021); board stays read-only**
26. Read-only command hint from next-action codes — **done (Run 022)**
27. Read-only one-command doctor / health check — **done (Run 023)**

## Later (automation)
28. TTS narration path (optional; keep human VO compatible)
29. Caption timing from a real selected take (not 150 wpm estimates)
30. ffmpeg assembly for this one locked format after one packet has VO + cards
31. YouTube upload + metadata only after packet QA passes

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
- Auto-writing spoken WORDS from expand.md budgets or expand_prompt stdout
- Applying expand_prompt stdout onto sample-001 via apply_script
- Promoting sample-001 with set_status
- Printing `--write` as the first hint.py or doctor.py command
