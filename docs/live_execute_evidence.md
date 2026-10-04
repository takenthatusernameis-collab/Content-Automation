# Live execute evidence

This file is the only way to unfreeze a new `YouTubeAPIError` reason in
`tools/youtube_api.py` or `tools/youtube_upload.py`.

`tools/upload_variant_freeze.py` fails the selftest when a new reason
literal appears here without a matching line. Do not add a reason to the
allowlist in that tool to skip this file.

A line is valid only after a dispatched `youtube-production.yml` execute
returned that status. Record the Actions run id. Do not invent one.

Format:

    live_status: REASON_CODE
    actions_run: 000
    note: one line on what the provider returned

No live execute has been dispatched. Videos published stay 0. There are
no `live_status` lines yet.
