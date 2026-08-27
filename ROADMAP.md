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
10. Research intake stub (source list + unsourced-stat reminder) — **done (Run 006)**
11. Scaffold wiring: new packet folders get generated `qa.md` + `research.md` without a second command

## Later (automation)
12. TTS narration path (optional; keep human VO compatible)
13. Caption generation from narration text
14. Render checklist / ffmpeg assembly for simple formats (talking-head-free explainers first)
15. YouTube upload + metadata only after packet QA passes

## Not yet
- Multi-platform posting
- Autopilot hourly content loops
- Analytics-driven topic selection (needs data)
- Paid stock/API shopping
- Web-scrape-as-research (explicitly rejected until a human verification step exists)
