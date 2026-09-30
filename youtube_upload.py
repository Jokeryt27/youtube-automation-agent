"""
YouTube Automation Agent - Step 5
Safe YouTube upload adapter.

This module uploads a video as PRIVATE by default.
OAuth credentials/token handling is intentionally kept local and out of GitHub.
"""

import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen


def upload_video(video_path: str, title: str, description: str, tags: list[str]):
    token = os.getenv("YOUTUBE_ACCESS_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "YOUTUBE_ACCESS_TOKEN is not set. Configure OAuth locally; "
            "never commit the token to GitHub."
        )

    path = Path(video_path)
    if not path.is_file():
        raise FileNotFoundError(f"Video not found: {path}")

    metadata = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False,
        },
    }

    # This is a safe adapter placeholder. A production implementation should
    # use Google's official resumable upload flow and OAuth 2.0 client library.
    print("READY FOR YOUTUBE UPLOAD")
    print(json.dumps(metadata, indent=2, ensure_ascii=False))
    print(f"Video file: {path}")
    print("Privacy status: PRIVATE")
    print("No public publishing action was performed.")


def main():
    if len(sys.argv) < 4:
        raise SystemExit(
            'Usage: python youtube_upload.py VIDEO.mp4 "Title" "Description"'
        )

    video = sys.argv[1]
    title = sys.argv[2]
    description = sys.argv[3]
    tags = [x.strip() for x in os.getenv("YOUTUBE_TAGS", "").split(",") if x.strip()]

    upload_video(video, title, description, tags)


if __name__ == "__main__":
    main()
