# YouTube Automation Agent — Step 7

## Multi-AI Provider System

The agent is no longer tied to OpenAI.

Set:

```text
AI_PROVIDER=gemini
```

or:

```text
AI_PROVIDER=openai
```

or:

```text
AI_PROVIDER=anthropic
```

Each provider has its own API key and model setting.

## Example

```bash
python ai_router.py "Create 3 hooks for a BGMI YouTube video."
```

## Important

- API keys must stay local and must never be committed to GitHub.
- Model names are configurable; use a model currently available in your provider account.
- This router does not automatically switch providers after an error. That can be added later as a controlled fallback.
- Human review remains part of the publishing workflow.

## Suggested architecture

Research/Search → AI Router → Script/Titles/SEO → Thumbnail → Human Review → Private YouTube Upload
