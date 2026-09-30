"""
YouTube Automation Agent - Step 3
Research -> Script + Titles + Description + Tags + Thumbnail Prompt.

This version uses an OpenAI-compatible chat endpoint configured through
environment variables. No real API keys belong in the repository.
"""

from dataclasses import dataclass, asdict
import json
import os
import sys
from urllib.request import Request, urlopen


@dataclass
class ContentPackage:
    topic: str
    research: dict
    script: str
    titles: list[str]
    description: str
    tags: list[str]
    thumbnail_prompt: str


def preview_package(topic: str, research: dict) -> ContentPackage:
    clean = topic.strip()
    return ContentPackage(
        topic=clean,
        research=research,
        script=(
            f"HOOK: Start with a clear reason to care about {clean}.\n\n"
            f"INTRO: Explain what {clean} is and what the viewer will learn.\n\n"
            "MAIN: Cover the verified facts from the research, one point at a time.\n\n"
            "CONCLUSION: Summarize the key takeaway and invite the viewer to subscribe."
        ),
        titles=[
            f"{clean}: What You Need to Know",
            f"The Truth About {clean}",
            f"{clean} Explained Simply",
            f"Everything You Should Know About {clean}",
            f"{clean}: Latest Facts & Details",
        ],
        description=(
            f"This video explains {clean} using the supplied research. "
            "Check the listed sources and verify current details before publishing."
        ),
        tags=[clean, "youtube", "explained", "facts", "latest"],
        thumbnail_prompt=(
            f"Create a high-contrast YouTube thumbnail about {clean}. "
            "Use one strong focal subject, cinematic lighting, simple background, "
            "large readable space for short text, and no invented logos or claims."
        ),
    )


def call_ai(topic: str, research: dict) -> ContentPackage:
    endpoint = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions").strip()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Use --preview for a local test."
        )

    prompt = f"""
Create a YouTube content package from the topic and research below.

Rules:
- Use only claims supported by the research.
- Clearly avoid rumors and unsupported predictions.
- Do not copy source text.
- Return valid JSON with exactly these keys:
  script, titles, description, tags, thumbnail_prompt
- titles: exactly 5 strings.
- tags: 8 to 15 short strings.
- script: a complete, natural voiceover script with hook, intro, main points,
  conclusion and a simple CTA.
- thumbnail_prompt: a concise image-generation prompt; do not invent logos,
  people, statistics, or claims.

TOPIC:
{topic}

RESEARCH:
{json.dumps(research, ensure_ascii=False)}
""".strip()

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You create factual, reviewable YouTube content."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }).encode("utf-8")

    req = Request(
        endpoint,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    with urlopen(req, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))

    content = data["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        content = content.strip("`")
        if content.startswith("json"):
            content = content[4:].strip()

    result = json.loads(content)

    return ContentPackage(
        topic=topic,
        research=research,
        script=str(result["script"]),
        titles=list(result["titles"]),
        description=str(result["description"]),
        tags=list(result["tags"]),
        thumbnail_prompt=str(result["thumbnail_prompt"]),
    )


def load_research(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    args = sys.argv[1:]
    preview = "--preview" in args
    args = [a for a in args if a != "--preview"]

    if not args:
        raise SystemExit(
            'Usage: python agent.py --preview "Your topic" [research.json]'
        )

    topic = args[0]
    research = load_research(args[1]) if len(args) > 1 else {
        "key_points": [],
        "sources": [],
    }

    package = preview_package(topic, research) if preview else call_ai(topic, research)
    print(json.dumps(asdict(package), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
