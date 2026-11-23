# Labor reduction map

Created 2026-11-18T11:50:00Z (Run 1311). Tracks recurring human work and automation status to compound efficiency. Estimates are rough, grounded in observed pipeline steps. Update with evidence after first published video.

## Pipeline stages and current automation

| Stage | Current status | Remaining human minutes (est. per video) | Automation notes | Next reduction opportunity |
|-------|----------------|------------------------------------------|------------------|----------------------------|
| Topic / idea | queued in topic_queue.md; starters exist | 5-10 | next_topic.py, queued_full_starter.py, idea_brief.py | Feed post-publish feedback into topic ranking |
| Research | claim_source_table.py, research starters, research_verification_checklist.py (enhanced Run 1314+; Run 1318: sources.md cross-check; Run 1319: --write-skeleton; Run 1323: grounded search query suggestions; Run 1324: primary-source site operators on statistical claims; Run 1325: auto-classify and rank source candidates by type; Run 1326: type summary counts + secondary-dominance warning; Run 1331: auto-link suggestions via word-overlap; Run 1332: source quality hints) | 1-5 | Tools generate tables and search prompts; checklist extracts claims, reports linking status vs sources.md, writes fillable skeleton on demand (never overwrites), prints ready-to-paste search queries from claim excerpts with automatic primary preference for %/study-like items, ranks existing source candidates (primary / primary-likely / secondary / unknown) via domain/keyword heuristics, and now prints type counts with a warning if secondary dominate, plus quality hints (study/report stronger, blog lower, year notes) | Further: any last remaining quality signals |
| Script | script_writer.md + many suggest/coach tools (Run 1335: priority high-signal originality flags in originality_report) | 5-15 | draft_starter, expansion coaches, words.py, claim/originality scans; enhanced: apply_script dry-run prints non-blocking anti-slop INFO + originality_notes (pointer + mechanism check + deeper concrete markers & lived-experience flags + sentence density + problem language echo + CTA mechanism alignment + mechanism one-sentence length). Restored after multiple placeholder regressions (Runs 1315-1320). Run 1322/1327/1328/1329/1330: full set of main originality signals always visible in dry-run. Report now highlights priority weak/missing/check signals first for focused review. | Further: any last remaining originality signals or other script coaches |
| Narration | generated fallback authorized for Q1; human recording option | 0 (gen) or 15-30 (record) | media_qa validates; local TTS not default | Pluggable TTS adapter when policy allows |
| Cards / visuals | card_generator.py READY_FOR_MEDIA | 5 | Deterministic from assets.md; size/text checks | B-roll optional adapter |
| Assembly | timeline.py + assemble.py PLAN_BUILT | 2-5 | Dry-run ffmpeg; --execute after media_qa PASS | Full local encode on gate machine |
| Captions | caption tools + aligner draft (Run 1333: priority high-CPS cues surfaced first in quality summary) | 8-18 | Silence-proportional draft; human spot-check; quality summary now highlights top fast CPS cues for focused review | ASR-based timing when available |
| Metadata / thumb | title/desc/tags/thumb suggest tools (Run 1334: priority high-signal issues in metadata_qa_report) | 4-8 | metadata_bundle.py consolidates; QA report now highlights priority hits first for focused review | Auto-approve after quality gates |
| QA / gates | media_qa, complete.py, contracts_suite | 5 | Fail-closed local gates | Live provider checks after credentials |
| Publish | youtube_upload.py READY_FOR_CREDENTIAL | 5 (secrets + dispatch) | Dry-run ready; live videos.insert needs OAuth | Reduce to one-click after first success |
| Feedback | youtube_feedback.py READY_FOR_CREDENTIAL | 5 (dispatch after window) | Observation window enforced | Auto-collect + summarize for experiment |
| Experiment | experiment_loop.py PLAN_BUILT | 10-15 | Baseline/decision templates; no invented metrics | Auto-propose next hypothesis from feedback |
| **Total remaining (after OAuth)** | | **~74-159** | Pre-upload path largely automated | First publish unlocks feedback loop |

## Compounding notes

- Pre-upload path (idea -> master) is reliable after materialize (verified Run 1311: media_qa PASS, next_action upload-blocked).
- Primary remaining recurring labor is the OAuth credential gate (one-time setup) plus post-publish review of feedback and experiment decisions.
- After first private video id: use docs/q1_post_publish_prep.md + after_upload_steps.py to close the loop.
- Do not invent metrics or media. Prefer tools that reduce the minutes in the table above.

See docs/production_capabilities.md for capability states and ROADMAP.md for ordered next steps.
