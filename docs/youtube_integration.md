# YouTube integration contract

## Goal

Keep the repository structurally ready for automated YouTube publishing so that, once the channel credentials are supplied, credentials are the final manual bottleneck rather than a missing implementation.

The live adapter is `tools/youtube_upload.py`. Dry-run remains the default; `--execute` performs authenticated `videos.insert` and, when the corresponding local files are present and the token is authorized, caption/thumbnail writes. It never prints secret values.

`videos.insert` uses the resumable protocol (`uploadType=resumable`, 8 MiB chunks, 308 resume). A single multipart POST of the master is not the video path. Captions and thumbnails stay multipart. A missing session Location is `RESUMABLE_SESSION_MISSING`. A 308 that does not advance is `RESUMABLE_STALLED`. HTTP 500, 502, 503, and 504, and a network error on a chunk PUT, query the session with `Content-Range: bytes */size` and resume from the returned Range. Three failures at the same stage raise `RESUMABLE_RETRY_EXHAUSTED`. A 404 on a mid-upload status query is `RESUMABLE_SESSION_EXPIRED`. A 200 or 201 with an empty body queries that same session once. A 404 or 410 on that follow-up is `RESUMABLE_COMPLETED_SESSION_GONE`: the last byte was accepted and the session can no longer return the id. That hold is persisted and the next execute must not start another videos.insert. Do not invent a provider video id.

The live feedback adapter is `tools/youtube_feedback.py`. Dry-run remains the default; `--execute` performs authenticated Analytics and comment-thread reads. It never invents metrics.

## Required pipeline

1. Validate the packet locally: status, selected VO, cards, captions/metadata as applicable, and final master export.
2. Read `videos/NNN-slug/publish.md` as the canonical upload-metadata source.
3. Validate the local export and metadata in a **dry run** with no provider call.
4. Check for the required YouTube authentication material without printing its values.
5. When credentials are present, authenticate and upload through the YouTube Data API using `python3 tools/youtube_upload.py PATH --execute`.
6. Persist only non-secret operational state: upload-attempt timestamp, provider video ID, final privacy state, and a redacted result/error code.
7. Do not upload merely because a hold expired, but do upload/publish through the normal authenticated path when all mechanical gates pass. Approval-only holds are authorized for agent completion; authentication and provider-policy requirements remain mandatory.
8. After a real provider_video_id exists and `upload_state.json` has an `uploaded_at` at least 7 days old, run `tools/youtube_feedback.py PATH --execute` with valid OAuth. A missing timestamp is `OBSERVATION_WINDOW_UNKNOWN`. An earlier collect is `OBSERVATION_WINDOW_NOT_DUE` and must not be stored as COLLECTED.

## Credential-last design

The repository may construct and test the uploader, metadata mapping, request formatting, retry behavior, idempotency guard, and redacted state handling **without** credentials.

The final manual bottleneck is provider authorization material, stored outside Git:

- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`
- optional `YOUTUBE_API_KEY` for public-read/quota diagnostics
- optional `YOUTUBE_CHANNEL_ID` as a non-secret routing value

Never commit any of these values. Do not put them in `publish.md`, `STATE.md`, logs, test fixtures, or workflow output.

For uploads, an OAuth 2.0 authorization token is required; an API key by itself is not sufficient for `videos.insert`. Use the minimum upload scope needed by the implementation.

The production path also uploads `captions.srt` and `thumbnail.png` after the video id exists. `youtube.upload` alone can insert the video and set the thumbnail, but `captions.insert` requires `https://www.googleapis.com/auth/youtube.force-ssl` or `https://www.googleapis.com/auth/youtube`. A refresh token with only the upload scope would create a private video and then loop on `POST_UPLOAD_INCOMPLETE`. Create the refresh token with both:

- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube.force-ssl`

`https://www.googleapis.com/auth/youtube` covers upload, captions, thumbnails, and comments by itself. Feedback collect also needs `https://www.googleapis.com/auth/yt-analytics.readonly`. `tools/youtube_upload.py` reads the granted scopes from tokeninfo after refresh and raises `SCOPE_INSUFFICIENT` before `videos.insert` when a needed scope is missing. It does not write `upload_state.json` for that refusal.

A present `thumbnail.png` must be a PNG of at least 640x360 and at most 2MB. A present `captions.srt` must be UTF-8, contain at least one parseable `-->` cue, keep cues in forward order, and not end more than one second past a probed master. A pin comment over 10000 characters is also refused. `artifact_block_reason()` sets inspect to `HOLD_LOCAL` and execute raises `ARTIFACT_REJECTED` before the token refresh and before `videos.insert`. A missing thumbnail or caption file stays missing and is not invented. An artifact refusal does not write `upload_state.json`.


## GitHub Actions runtime

The repository now includes `.github/workflows/youtube-production.yml` as the external runtime path. It is deliberately `workflow_dispatch` only: a production write is never triggered merely by a repository push.

The workflow:

1. checks out `main`;
2. if `execute` or `collect_feedback` is true, runs `tools/oauth_preflight.py` before ffmpeg or materialize and exits 3 when any secret is empty;
3. uses the built-in GitHub Actions token as `GH_TOKEN` to download the private Q1 releases, unless the dispatch is collect-only;
4. runs the checksum-locked Q1 materializer on dry-run and execute; collect-only skips media download;
5. performs the existing local upload gates on dry-run;
6. reads YouTube OAuth values only from GitHub Actions secrets;
7. runs the existing `--execute` uploader when explicitly requested;
8. persists only redacted `upload_state.json` when a provider video ID exists, so a later run can resume instead of blindly re-uploading the same fingerprint; and
9. when `collect_feedback=true`, runs `youtube_feedback.py --execute` then `experiment_loop.py --write-state`, and commits `feedback_state.json` only if gate is `COLLECTED`. Default is false. It does not upload and does not invent a baseline or decision.

Required GitHub Actions secrets are:

- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

The workflow keeps the uploader's initial privacy mode at `private`. Posting the optional first comment remains opt-in because the corresponding OAuth grant must include the comment-write scope used by the adapter.

The workflow requires `contents: write` because its persistent mutations are the non-secret upload state and, after a real fetch, collected feedback state. It does not write media files to the repository.

## Authentication boundary

The uploader fails closed with:

`YOUTUBE_AUTH_REQUIRED`

when required OAuth credentials are absent or invalid.

The feedback collector fails closed with `HOLD_UNPUBLISHED` when `upload_state.json` has no provider_video_id, and with `YOUTUBE_AUTH_REQUIRED` when OAuth is absent.

The daily unstick agent may construct or repair everything up to that boundary without waiting for a human. When the boundary is reached, it should request only the missing credential material and nothing else.

## Safety / idempotency

Before an upload attempt:

- require a completed local master export;
- require a valid `publish.md`;
- compute a stable packet/export fingerprint;
- refuse to upload the same fingerprint twice unless an explicit replacement operation is requested;
- use a non-destructive initial privacy mode configured by the repository policy (`private` in the dry-run adapter);
- keep provider IDs and statuses in redacted state only.

Do not implement automatic deletion or channel-wide maintenance as part of the first uploader.

## Construction order

Implemented without credentials (Run 217):

1. metadata parser and validation;
2. export-path validation;
3. fingerprint/idempotency contract;
4. OAuth configuration loader (presence only);
5. dry-run request builder;
6. redacted result/state writer.

Implemented without credentials (Run 219):

7. feedback collector with HOLD_UNPUBLISHED / YOUTUBE_AUTH_REQUIRED gates;
8. 7-day observation window contract;
9. dry-run Analytics + commentThreads plan;
10. redacted feedback_state.json writer.

Ready for credential / provider execution:

11. authenticated upload adapter (`videos.insert`);
12. live Analytics reports and commentThreads.list;
13. credential-only integration testing when real OAuth is supplied.

The last step that cannot be completed without a real channel credential must be clearly reported as `YOUTUBE_AUTH_REQUIRED`. Approval-only status is not a reason to stop.

## External reference

YouTube's current Data API documentation states that insert/update/delete requests require authorization, and `videos.insert` accepts OAuth scopes including `https://www.googleapis.com/auth/youtube.upload`.

References:
- https://developers.google.com/youtube/v3/docs
- https://developers.google.com/youtube/v3/docs/videos/insert
- https://developers.google.com/youtube/v3/guides/authentication


## Feedback access

After publication, the same credentialed integration should support:

- YouTube Analytics reports through the Analytics API, using an appropriately authorized readonly scope.
- Video comment-thread retrieval through the Data API, with `comments.list` available when complete reply retrieval is required.
- Redacted storage of the video ID, retrieval timestamp, observation window, and imported metrics/comments. Never store OAuth tokens in feedback files.

YouTube's Analytics reporting API supports metrics such as views, likes/dislikes, estimated minutes watched, average view duration, and average view percentage.
YouTube's Data API supports comment-thread retrieval by video ID; replies may require the comments.list method.

The feedback collector must fail closed at `YOUTUBE_AUTH_REQUIRED` when readonly authorization is absent, just as the uploader does for upload authorization.
The collector must also fail closed at `HOLD_UNPUBLISHED` when no provider video ID exists. Empty metrics are not collected feedback.
