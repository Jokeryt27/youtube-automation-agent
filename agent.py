"""
YouTube Automation Agent - Step 2
Research-first content workflow.

Preview mode works without an API key.
Live research uses a configurable search API endpoint supplied through environment variables.
"""

from dataclasses import dataclass, asdict
import json
import os
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen


@dataclass
class Source:
    title: str
    url: str
    snippet: str = ""


@dataclass
class ResearchPackage:
    topic: str
    key_points: list[str]
    sources: list[Source]


def research_preview(topic: str) -> ResearchPackage:
    return ResearchPackage(
        topic=topic.strip(),
        key_points=[
            f"Define and explain the main idea behind: {topic.strip()}.",
            "Identify recent developments and dates that should be verified.",
            "Separate confirmed facts from opinions or predictions.",
            "Use multiple independent sources before publishing.",
        ],
        sources=[],
    )


def web_search(topic: str, max_results: int = 5) -> ResearchPackage:
    endpoint = os.getenv("SEARCH_API_URL", "").strip()
    api_key = os.getenv("SEARCH_API_KEY", "").strip()

    if not endpoint or not api_key:
        raise RuntimeError(
            "Set SEARCH_API_URL and SEARCH_API_KEY in your local environment, "
            "or run with --preview."
        )

    url = endpoint + ("&" if "?" in endpoint else "?") + "q=" + quote(topic)
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": "youtube-automation-agent/0.2",
        },
    )

    with urlopen(request, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))

    raw = data.get("results", data if isinstance(data, list) else [])
    sources = []
    for item in raw[:max_results]:
        if isinstance(item, dict):
            sources.append(
                Source(
                    title=str(item.get("title", "Untitled")),
                    url=str(item.get("url", "")),
                    snippet=str(item.get("snippet", item.get("description", ""))),
                )
            )

    key_points = [
        "Review every source manually before treating a claim as confirmed.",
        "Check publication dates and prefer primary/official sources when available.",
        "Do not publish unsupported claims, rumors, or copied text.",
    ]

    return ResearchPackage(topic=topic.strip(), key_points=key_points, sources=sources)


def main() -> None:
    topic = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else input("Enter YouTube topic: ").strip()
    if not topic:
        raise SystemExit("Topic cannot be empty.")

    package = research_preview(topic) if "--preview" in sys.argv else web_search(topic)
    print(json.dumps(asdict(package), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
