# ROADMAP

Order is deliberate: understandability and reliability first, then efficiency, then autonomy.

## Next (assisted production)
31. Working topic queue + read-only next-topic printer — **done (Run 027)**
32. Predicted packet path + evidence-gated queue closer — **done (Run 028)**
33. Shared queue lib + scaffold reprints mark_topic dry-run — **done (Run 029)**
34. Read-only queue vs folder board — **done (Run 030)**
35. Queue board `--strict` + packet status column — **done (Run 031)**
36. Queue board contract selftest — **done (Run 032)**
37. Write-path contract (apply_script + set_status gates on a temp tree) — **done (Run 033)**
38. Scaffold contract (new_packet mark-handoff + titles_filled + next_id) — **done (Run 034)**
39. Contract router (`which_contract.py`) — **done (Run 035)**
40. Router contract (`router_contract.py`) — **done (Run 036)**
41. Reconstruct file list (`needed.py`) — **done (Run 037)**
42. Reconstruct presence check (`needed.py --missing` + fallback aliases) — **done (Run 038)**
43. First-fetch bootstrap (`needed.py --bootstrap`) — **done (Run 039)**
44. Fetch-wave plan (`needed.py --plan`) — **done (Run 040)**
45. Post-reconstruct operator command (`needed.py --plan` WAVE 3) — **done (Run 041)**
46. Operator reconstruct command (`needed.py --plan` WAVE 3 `queue_status.py --missing`) — **done (Run 042)**

Earlier items 1-30 remain done as recorded in prior commits.

## Later (automation)
47. TTS narration path (optional; keep human VO compatible)
48. Caption timing from a real selected take (not 150 wpm estimates)
49. ffmpeg assembly for this one locked format after one packet has VO + cards
50. YouTube upload + metadata only after packet QA passes

## Not yet
- Auto-scaffolding the next queued topic without a human instruction
- Marking a queue row used without a matching videos/ folder
- Auto-marking the queue from new_packet.py
- Turning default queue_status into a failing command (keep `--strict` opt-in)
- Mapping needed.py / doctor.py / expand_prompt.py onto a contract
- Making needed.py --missing, --bootstrap, or --plan exit non-zero
- Treating --bootstrap or --plan as a sixth contract
- Growing BOOTSTRAP or WAVE 2 / WAVE 3 into a full-repo dump
- Treating WAVE 3 as permission to auto-scaffold
- ffmpeg / TTS / YouTube OAuth / Whisper / stock / shorts
- Treating which_contract --run SKIP as a contract PASS
