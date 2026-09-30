"""
YouTube Automation Agent - Step 4
Content package + thumbnail planning + human review checklist.
"""

from dataclasses import dataclass, asdict
import json
import sys


@dataclass
class ThumbnailPlan:
    aspect_ratio: str
    concept: str
    text: str
    prompt: str
    review_checklist: list[str]


def build_thumbnail_plan(topic: str, title: str) -> ThumbnailPlan:
    topic = topic.strip()
    title = title.strip()
    short_text = title[:28].strip()

    return ThumbnailPlan(
        aspect_ratio="16:9",
        concept=f"One strong focal visual representing {topic}",
        text=short_text,
        prompt=(
            f"YouTube thumbnail, 16:9, topic: {topic}. "
            f"Create one strong focal subject, cinematic lighting, high contrast, "
            f"clean background, clear separation from background, and large readable "
            f"space for the text: '{short_text}'. "
            "Do not invent people, logos, statistics, screenshots, or claims. "
            "Keep the composition readable at small size."
        ),
        review_checklist=[
            "Text is short and readable on a phone.",
            "Thumbnail matches the actual video topic.",
            "No invented people, logos, statistics, or claims.",
            "Main subject is clear at small size.",
            "No misleading visual implication.",
            "Check spelling before publishing.",
        ],
    )


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--preview"]
    if not args:
        raise SystemExit(
            'Usage: python thumbnail.py "Topic" "Title"'
        )

    topic = args[0]
    title = args[1] if len(args) > 1 else topic
    plan = build_thumbnail_plan(topic, title)
    print(json.dumps(asdict(plan), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
