"""
Multi-AI provider router for the YouTube Automation Agent.

Supported providers:
- openai
- gemini
- anthropic

All credentials are read from environment variables.
"""

import json
import os
import sys
from urllib.request import Request, urlopen


def _post(url, payload, headers):
    req = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=90) as response:
        return json.loads(response.read().decode("utf-8"))


def ask_openai(prompt):
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENAI_API_KEY is missing.")
    url = os.getenv(
        "OPENAI_API_URL",
        "https://api.openai.com/v1/chat/completions",
    )
    model = os.getenv("OPENAI_MODEL", "").strip()
    if not model:
        raise RuntimeError("Set OPENAI_MODEL to a model available in your account.")

    data = _post(
        url,
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        },
        {"Authorization": f"Bearer {key}"},
    )
    return data["choices"][0]["message"]["content"]


def ask_gemini(prompt):
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY is missing.")
    model = os.getenv("GEMINI_MODEL", "").strip()
    if not model:
        raise RuntimeError("Set GEMINI_MODEL to a Gemini model available in your account.")

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent"
    )
    data = _post(
        url,
        {"contents": [{"parts": [{"text": prompt}]}]},
        {"x-goog-api-key": key},
    )
    return data["candidates"][0]["content"]["parts"][0]["text"]


def ask_anthropic(prompt):
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is missing.")
    model = os.getenv("ANTHROPIC_MODEL", "").strip()
    if not model:
        raise RuntimeError("Set ANTHROPIC_MODEL to a model available in your account.")

    data = _post(
        "https://api.anthropic.com/v1/messages",
        {
            "model": model,
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}],
        },
        {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
    )
    return "".join(
        block.get("text", "")
        for block in data.get("content", [])
        if block.get("type") == "text"
    )


def ask(prompt, provider=None):
    provider = (provider or os.getenv("AI_PROVIDER", "gemini")).strip().lower()

    if provider == "openai":
        return ask_openai(prompt)
    if provider == "gemini":
        return ask_gemini(prompt)
    if provider == "anthropic":
        return ask_anthropic(prompt)

    raise ValueError(
        f"Unsupported AI_PROVIDER={provider}. Use openai, gemini, or anthropic."
    )


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]).strip() or "Say hello in one short sentence."
    print(ask(prompt))
