2026-11-04T10:16:00Z (Run 1018)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Added tools/dispatch_soft_summary.py: soft one-page dispatch readiness summary aggregating title glance, master SHA reminder, and spoken-duration hint (with delta if VO present). Complements human_one_pager.py and points to media_qa / vo_duration_match for full recipes. Does not change hard gates, invent media, run ffmpeg, or require credentials. Pre-upload path remains complete. STALL_OAUTH_IDLE primary. Prefer human OAuth step (docs/human_oauth_checklist.md or python3 tools/human_one_pager.py or python3 tools/dispatch_soft_summary.py) or further truly new media/QA capability that does not require credentials. Do not add another consistency printer. Do not overwrite entire tool files with placeholders.

# STATE

2026-11-04T09:16:00Z (Run 1017)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Updated tools/human_one_pager.py with a short optional soft-media awareness section that points to tools/vo_duration_match.py and tools/media_qa.py (soft dry-run recipes only). Reduces rediscovery of duration delta and suggested ffmpeg commands for the human during the OAuth step. Does not change hard gates, invent media, run ffmpeg, or require credentials. Pre-upload path remains complete. STALL_OAUTH_IDLE primary. Prefer human OAuth step (docs/human_oauth_checklist.md or python3 tools/human_one_pager.py) or further truly new media/QA capability that does not require credentials. Do not add another consistency printer. Do not overwrite entire tool files with placeholders.

2026-11-04T08:20:00Z (Run 1016)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Added tools/vo_duration_match.py: soft report comparing script/draft estimated duration (150 wpm from spoken WORDS) to actual Selected VO WAV duration when present. Surfaces delta and soft match note. Does not change hard gates, invent media, run ffmpeg, or require credentials. Complements existing media_qa soft commands. Pre-upload path remains complete. STALL_OAUTH_IDLE primary. Prefer human OAuth step (docs/human_oauth_checklist.md or python3 tools/human_one_pager.py) or further truly new media/QA capability that does not require credentials. Do not add another consistency printer. Do not overwrite entire tool files with placeholders.

2026-11-04T07:25:00Z (Run 1015)

OAuth was not polled and execute was not dispatched. Videos published stay 0. Restored tools/media_qa.py after accidental full-file overwrite in prior commit (placeholder text) and properly added soft dry-run ffmpeg bit-depth conversion command (when Selected VO sample width != 2 / 16-bit). Soft report only (does not change the hard gate). Surfaces an immediately copy-pasteable conversion recipe for future packets without credentials, inventing media, or running ffmpeg. Still no media invent, no ffmpeg execute, no secrets. Pre-upload path remains complete. STALL_OAUTH_IDLE primary. Prefer human OAuth step (docs/human_oauth_checklist.md or python3 tools/human_one_pager.py) or further truly new media/QA capability that does not require credentials. Do not add another consistency printer. Do not overwrite entire tool files with placeholders.

(Older state notes remain below or in docs/state_archive.md. Do not paste the archive back.)
