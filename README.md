# YouTube Automation Agent — Step 5

## Safe YouTube Upload

This step adds a YouTube upload adapter with an important safety default:

**Every upload is PRIVATE.**

The project does not automatically publish videos.

## Required local environment

```text
YOUTUBE_ACCESS_TOKEN=
YOUTUBE_TAGS=
```

Never put a real token in GitHub.

## Test the adapter

```bash
python youtube_upload.py video.mp4 "My Video Title" "My description"
```

The current adapter validates the video and prints the upload metadata. It intentionally does not perform a public upload.

## Production OAuth

For a real YouTube upload, configure Google/YouTube OAuth 2.0 locally and use the official YouTube Data API resumable upload flow. Store credentials outside the repository.

## Recommended workflow

1. Generate content.
2. Review research.
3. Review script/title/thumbnail.
4. Prepare video.
5. Upload as PRIVATE.
6. User checks the uploaded video in YouTube Studio.
7. Only then change visibility manually or through a separately approved action.
