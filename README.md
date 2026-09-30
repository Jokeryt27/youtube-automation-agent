# YouTube Automation Agent — Step 4

## Thumbnail + Human Review

The project now produces a structured thumbnail plan:

- 16:9 aspect ratio
- Main visual concept
- Short thumbnail text
- Image-generation prompt
- Human review checklist

## Test

```bash
python thumbnail.py "BGMI 4.3 Update" "BGMI 4.3 Update — What's New?"
```

## Review before publishing

Check that the thumbnail:
1. Is readable on a phone.
2. Matches the actual video.
3. Does not invent people, logos, numbers or claims.
4. Is not misleading.
5. Has correct spelling.

The agent does not publish the thumbnail automatically.
