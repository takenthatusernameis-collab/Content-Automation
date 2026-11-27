# Labor reduction map

Estimated remaining human minutes per stage for a typical packet (after Q1 pattern). Values are approximate and intended for prioritization only.

| Stage | Est. human min | Automation state | Notes |
|-------|----------------|------------------|-------|
| Research / idea lock | 5–15 | assisted | Queue + apply_idea; claim-source table helps | 
| Script draft + originality | 10–25 | assisted | apply_script dry-run + originality signals; anti-slop scanners |
| Script final / expand | 5–15 | assisted | script_expander + quality_scan |
| Metadata (title/desc/tags/chapters/comment) | 2–5 | assisted | metadata_bundle + publish_brief locks |
| Narration (Selected VO) | 0 (Q1 generated) / 15–40 (future human) | READY_FOR_MEDIA | Generated take authorized for Q1; human recording optional later |
| Cards / visuals | 0–5 | READY_FOR_MEDIA | Deterministic card_generator; gitignored |
| Captions spot-check | 3–6 | assisted | caption_spotcheck_assistant.py structured list + soft flags; hard gate caption_gate.py |
| Thumbnail review | 1–3 | assisted | thumbnail_spotcheck_assistant.py structured list + soft flags (size/dims/aspect); sensory still human |
| Assembly / encode | 0 | PLAN_BUILT / READY_FOR_MEDIA | assemble --execute gated on media_qa PASS |
| Media QA | 0 | READY_FOR_MEDIA | media_qa + export_probe fail-closed |
| Upload + captions + thumb | 0 once secrets set | READY_FOR_CREDENTIAL | youtube_upload dry-run ready; execute needs OAuth |
| Studio pin / end-screen | 2–5 | manual | Data API cannot finish; studio_pin.md helps |
| Feedback collect (after +10d) | 0 once secrets set | READY_FOR_CREDENTIAL | youtube_feedback dry-run ready |
| Experiment decide | 5–10 | PLAN_BUILT | experiment_loop + decision file; needs real metrics |
| **OAuth secrets (one-time)** | **10–20** | **BLOCKED** | **Sole remaining publish gate; STALL_OAUTH_IDLE** |

**Total recurring human minutes per video after first publish:** target < 30 once secrets exist and Studio clicks are accepted.

**Current system human minutes to first private video:** ~10–20 (OAuth only).

Updated: 2026-11-27T17:28:00Z (Run 1354). Thumbnail spot-check reduced via assistant. Caption spot-check reduced via assistant. Prefer reductions that compound across many videos.
