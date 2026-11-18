# Labor reduction map

Created 2026-11-18T11:50:00Z (Run 1311). Tracks recurring human work and automation status to compound efficiency. Estimates are rough, grounded in observed pipeline steps. Update with evidence after first published video.

## Pipeline stages and current automation

| Stage | Current status | Remaining human minutes (est. per video) | Automation notes | Next reduction opportunity |
|-------|----------------|------------------------------------------|------------------|----------------------------|
| Topic / idea | queued in topic_queue.md; starters exist | 5-10 | next_topic.py, queued_full_starter.py, idea_brief.py | Feed post-publish feedback into topic ranking |
| Research | claim_source_table.py, research starters, research_verification_checklist.py | 15-30 | Tools generate tables and search prompts; human verifies sources | Standardized verification checklist (new tool reduces recurring check time) |
| Script | script_writer.md + many suggest/coach tools | 20-40 | draft_starter, expansion coaches, words.py, claim/originality scans | Stronger anti-slop enforcement in apply_script |
| Narration | generated fallback authorized for Q1; human recording option | 0 (gen) or 15-30 (record) | media_qa validates; local TTS not default | Pluggable TTS adapter when policy allows |
| Cards / visuals | card_generator.py READY_FOR_MEDIA | 5 | Deterministic from assets.md; size/text checks | B-roll optional adapter |
| Assembly | timeline.py + assemble.py PLAN_BUILT | 2-5 | Dry-run ffmpeg; --execute after media_qa PASS | Full local encode on gate machine |
| Captions | caption tools + aligner draft | 10-20 | Silence-proportional draft; human spot-check | ASR-based timing when available |
| Metadata / thumb | title/desc/tags/thumb suggest tools | 5-10 | metadata_bundle.py consolidates | Auto-approve after quality gates |
| QA / gates | media_qa, complete.py, contracts_suite | 5 | Fail-closed local gates | Live provider checks after credentials |
| Publish | youtube_upload.py READY_FOR_CREDENTIAL | 5 (secrets + dispatch) | Dry-run ready; live videos.insert needs OAuth | Reduce to one-click after first success |
| Feedback | youtube_feedback.py READY_FOR_CREDENTIAL | 5 (dispatch after window) | Observation window enforced | Auto-collect + summarize for experiment |
| Experiment | experiment_loop.py PLAN_BUILT | 10-15 | Baseline/decision templates; no invented metrics | Auto-propose next hypothesis from feedback |
| **Total remaining (after OAuth)** | | **~90-180** | Pre-upload path largely automated | First publish unlocks feedback loop |

## Compounding notes

- Pre-upload path (idea -> master) is reliable after materialize (verified Run 1311: media_qa PASS, next_action upload-blocked).
- Primary remaining recurring labor is the OAuth credential gate (one-time setup) plus post-publish review of feedback and experiment decisions.
- After first private video id: use docs/q1_post_publish_prep.md + after_upload_steps.py to close the loop.
- Do not invent metrics or media. Prefer tools that reduce the minutes in the table above.

See docs/production_capabilities.md for capability states and ROADMAP.md for ordered next steps.
