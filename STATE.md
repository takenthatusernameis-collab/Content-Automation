# STATE

2026-11-23T19:28:47Z (Run 1337)

After Run 1336. Added tools/priority_review_summary.py: single aggregator that runs quality_scan, originality_report, caption_quality_summary, and metadata_qa_report then prints only their high-signal PRIORITY sections. Verified by re-fetch of file contents (extract_priority_block and main logic present, size ~4.3k). Reduces recurring human minutes by providing one focused entry point instead of multiple sequential reports. Updated labor_reduction_map (cross-stage review). STALL_OAUTH_IDLE continues (~50 days from ~2026-10-02, HIGH / INCREASINGLY_SUSPICIOUS after >40 days and 1300+ runs with published=0). No secrets polled, no dispatch, no live packet or media commits. Long stall remains the sole blocker; the only advancing action is the human OAuth step (three secrets + one execute=true dispatch). Pure inspection runs should be minimized. Prefer human progress or truly new unblocked capabilities that compound. Priority aggregator further reduces recurring review minutes across stages.

Older state notes live in `docs/state_archive.md`. Do not paste the archive back.
