"""
YouTube Automation Agent - starter
Generates a repeatable content package from a topic.
"""

from dataclasses import dataclass, asdict
import json


@dataclass
class VideoPackage:
    topic: str
    title_options: list[str]
    description: str
    tags: list[str]
    script_outline: list[str]


def build_package(topic: str) -> VideoPackage:
    clean_topic = topic.strip()
    if not clean_topic:
        raise ValueError("Topic cannot be empty.")

    return VideoPackage(
        topic=clean_topic,
        title_options=[
            f"{clean_topic} — Everything You Need to Know",
            f"The Truth About {clean_topic}",
            f"{clean_topic}: What Nobody Tells You",
        ],
        description=(
            f"In this video, we cover {clean_topic} with a clear, engaging overview. "
            "Verify facts and sources before publishing."
        ),
        tags=[clean_topic, "youtube", "automation", "video"],
        script_outline=[
            "Hook: explain why the viewer should care.",
            "Context: introduce the topic and key facts.",
            "Main points: explain the most useful information.",
            "Examples/evidence: add verified supporting details.",
            "Conclusion: summarize and give the viewer a clear takeaway.",
            "CTA: invite viewers to subscribe or watch the next video.",
        ],
    )


if __name__ == "__main__":
    topic = input("Enter YouTube topic: ")
    package = build_package(topic)
    print(json.dumps(asdict(package), indent=2, ensure_ascii=False))
