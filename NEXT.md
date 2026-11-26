# NEXT

Primary next action (human only): Set the three YouTube OAuth secrets and dispatch once.

```bash
python3 tools/oauth_complete_guide.py
# or
python3 tools/human_starter.py
```

Then:
```bash
gh secret set YOUTUBE_CLIENT_ID --repo takenthatusernameis-collab/Content-Automation
gh secret set YOUTUBE_CLIENT_SECRET --repo takenthatusernameis-collab/Content-Automation
gh secret set YOUTUBE_REFRESH_TOKEN --repo takenthatusernameis-collab/Content-Automation
gh workflow dispatch youtube-production.yml --repo takenthatusernameis-collab/Content-Automation -f execute=true -f collect_feedback=false
```

Do not poll secrets. Do not rematerialize media if already present. Do not scaffold Q2.

After private video id appears: `python3 tools/post_publish_path_ready.py` then follow docs/q1_post_publish_prep.md and tools/after_upload_steps.py.

For agents: Prefer small reusable unblocked improvements that reduce human minutes in docs/labor_reduction_map.md or improve reliability (e.g. production_path_integrity_check.py now enforced in selftest.yml alongside post_publish_integrity_check.py, human_guidance_integrity_check.py, run_number_consistency_check.py and tracking_integrity_check.py). Always verify actual file contents after claimed edits (not just docs or commit messages). Minimize pure inspection runs while STALL_OAUTH_IDLE persists. Recent: production path integrity now runs on every CI push/PR; post-publish integrity now runs on every CI push/PR; human guidance integrity now runs on every CI push/PR; run-number consistency runs on every CI; tracking integrity runs on every CI; labor_estimate.py includes suggested next local step + command; priority_review_summary.py includes that next step + cumulative high-signal minutes; status_one_pager.py available for concise status.

See docs/HUMAN_PRIORITY.md and tools/human_next_action.py.
