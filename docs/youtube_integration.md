# YouTube integration contract

## Goal

Keep the repository structurally ready for automated YouTube publishing so that, once the channel credentials are supplied, credentials are the final manual bottleneck rather than a missing implementation.

The live adapter is `tools/youtube_upload.py`. It is dry-run only. It does not call the YouTube API. It never prints secret values.

The live feedback adapter is `tools/youtube_feedback.py`. It is dry-run only. It does not call Analytics or comment APIs. It never invents metrics.

## Required pipeline

1. Validate the packet locally: status, selected VO, cards, captions/metadata as applicable, and final master export.
2. Read `videos/NNN-slug/publish.md` as the canonical upload-metadata source.
3. Validate the local export and metadata in a **dry run** with no provider call.
4. Check for the required YouTube authentication material without printing its values.
5. When credentials are present, authenticate and upload through the YouTube Data API.
6. Persist only non-secret operational state: upload-attempt timestamp, provider video ID, final privacy state, and a redacted result/error code.
7. Never upload, publish, or change channel state merely because a manual hold expired; the hold only removes the repository-side block.
8. After a real provider_video_id exists, run `tools/youtube_feedback.py` in dry-run. Live fetch remains gated on OAuth.

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

Still NOT_BUILT:

11. authenticated upload adapter (`videos.insert`);
12. live Analytics reports and commentThreads.list;
13. final credential-only integration test.

The last step that cannot be completed without a real channel credential must be clearly reported as `YOUTUBE_AUTH_REQUIRED`.

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
