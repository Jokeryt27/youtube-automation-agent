"""
YouTube Automation Agent - Step 8
Controlled multi-AI fallback router.

Example:
AI_PROVIDER_CHAIN=gemini,openai,anthropic
AI_MAX_ATTEMPTS=3

The router only tries providers explicitly listed by the user.
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
    model = os.getenv("OPENAI_MODEL", "").strip()
    if not key or not model:
        raise RuntimeError("OpenAI credentials/model are not configured.")

    data = _post(
        os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions"),
        {"model": model, "messages": [{"role": "user", "content": prompt}]},
        {"Authorization": f"Bearer {key}"},
    )
    return data["choices"][0]["message"]["content"]


def ask_gemini(prompt):
    key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL", "").strip()
    if not key or not model:
        raise RuntimeError("Gemini credentials/model are not configured.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    data = _post(
        url,
        {"contents": [{"parts": [{"text": prompt}]}]},
        {"x-goog-api-key": key},
    )
    return data["candidates"][0]["content"]["parts"][0]["text"]


def ask_anthropic(prompt):
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    model = os.getenv("ANTHROPIC_MODEL", "").strip()
    if not key or not model:
        raise RuntimeError("Anthropic credentials/model are not configured.")

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


PROVIDERS = {
    "openai": ask_openai,
    "gemini": ask_gemini,
    "anthropic": ask_anthropic,
}


def ask_with_fallback(prompt):
    chain = [
        x.strip().lower()
        for x in os.getenv("AI_PROVIDER_CHAIN", "gemini").split(",")
        if x.strip()
    ]

    max_attempts = int(os.getenv("AI_MAX_ATTEMPTS", str(len(chain))))
    max_attempts = max(1, min(max_attempts, len(chain)))

    errors = []

    for provider in chain[:max_attempts]:
        if provider not in PROVIDERS:
            errors.append(f"{provider}: unsupported provider")
            continue

        try:
            result = PROVIDERS[provider](prompt)
            if result and result.strip():
                return {
                    "provider": provider,
                    "attempts": len(errors) + 1,
                    "content": result,
                }
        except Exception as exc:
            errors.append(f"{provider}: {type(exc).__name__}: {exc}")

    raise RuntimeError(
        "All configured AI providers failed. No automatic publishing action was taken.\n"
        + "\n".join(errors)
    )


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]).strip()
    if not prompt:
        raise SystemExit(
            'Usage: python ai_fallback.py "Create a YouTube hook about BGMI."'
        )
    print(json.dumps(ask_with_fallback(prompt), indent=2, ensure_ascii=False))
