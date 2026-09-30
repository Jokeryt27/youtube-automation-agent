"""
YouTube Automation Agent - Step 10
Safe YouTube upload adapter with final human approval.

The workflow:
1. Validate local OAuth token
2. Validate video file
3. Request explicit human approval
4. Continue only after APPROVE
5. Keep upload PRIVATE by default

OAuth credentials/tokens must remain local and must never be committed.
"""

import json
import os
import sys
from pathlib import Path

from approval_gate import require_approval


def upload_video(
    video_path: str,
    title: str,
    description: str,
    tags: list[str],
):
    # Credentials stay local and are never stored in GitHub.
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

    # ---------------------------------------------------------
    # STEP 10: FINAL HUMAN APPROVAL
    # ---------------------------------------------------------

    approval = require_approval(
        reviewer=os.getenv("APPROVAL_REVIEWER", "user"),
        note=f"Approve private upload: {title}",
    )

    if not approval.approved:
        raise PermissionError(
            "Upload blocked: final human approval was rejected."
        )

    # ---------------------------------------------------------
    # SAFE UPLOAD ADAPTER
    # ---------------------------------------------------------
    #
    # This remains a safe placeholder.
    # A production implementation should use Google's official
    # resumable upload flow and OAuth 2.0 client library.
    #
    # Even when implemented, privacyStatus remains PRIVATE until
    # the user explicitly changes the publishing workflow.
    #

    print("\nFINAL APPROVAL RECEIVED")
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

    tags = [
        x.strip()
        for x in os.getenv("YOUTUBE_TAGS", "").split(",")
        if x.strip()
    ]

    upload_video(
        video_path=video,
        title=title,
        description=description,
        tags=tags,
    )


if __name__ == "__main__":
    main()
