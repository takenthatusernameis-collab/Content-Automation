# ROADMAP

## Next (assisted production)
31-51n. Queue through write_path apply locks — **done (Runs 027-066; body restored Run 067)**
51o-51aj. Write-path / words / prove_locks / printer + page alignment — **done (Runs 067-088)**
51ak-51ay. idea_brief through alias READY — **done (Runs 089-103)**
51az-51bf. Writer allocation through hint Target comment — **done (Runs 104-110)**
51bg. Q1 packet scaffold + idea paste — **done (Run 111, other agent)**
51bh. Q1 draft.md first WORDS in claimed band — **done pending words.py (Run 112)**
51bi. Official-equivalent words count + apply script.md — **done (Run 113; 952 IN BAND)**
51bj. validate_packet + title/thumb brief + ready_for_vo — **done (Run 114; gate PASS, no duration WARN)**
51bk. vo_session reading card + captions stub from WORDS — **done (Run 115; ready-to-record; take missing)**
51bl. assets list + publish stub — **done (Run 116)**
51bm. publish tag trim + qa mechanical + render presence — **done (Run 117; all-missing; no media)**
51bn. after-VO operator path on human_session + narration — **done (Run 118; no wav)**
51bo. after-edit card path on human_session + editor/assets — **done (Run 119; no png)**
51bp. after-presence publish edit on human_session — **done (Run 120; no upload)**
51bq. lock Selected VO to packet-relative path — **done (Run 121; no wav)**
51br. gitignore local VO/card/export binaries — **done (Run 122; no wav)**
51bs. align BLOCKED.md VO setup path with packet-relative gates — **done (Run 123; no wav)**

## Later (automation)
52. Human override of heuristic Primary (optional; already locked)
53. TTS narration path (optional) or recorded selected take
54. Caption timing from a real selected take
55. ffmpeg assembly after one packet has VO + cards
56. YouTube upload after packet QA passes

## Not yet
- Treating draft.md as script.md before apply --write
- Auto-scaffolding Q2 while Q1 has no VO
- WAVE 4
- Making apply or words idea-lock INFO a BLOCKED error or --strict FAIL
- Another Band-landing reprint CLI
- Stripping the Target column from docs/human_session.md step 3
- Stripping the Target comment from hint.py
- Mapping doctor.py / words.py / prove_locks.py
- Bumping ready_for_edit without Selected VO on disk
- Treating a publish.md edit as an upload
- Treating repo-root `vo/` as Selected VO
- Force-adding ignored media to flip presence rows
