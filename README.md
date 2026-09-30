# YouTube Automation Agent — Step 8

## Controlled AI fallback

The agent can try multiple AI providers in a user-defined order.

Example:

```text
AI_PROVIDER_CHAIN=gemini,openai,anthropic
AI_MAX_ATTEMPTS=3
```

Flow:

**Gemini fails → OpenAI → Claude → Human review if all fail**

### Cost control

`AI_MAX_ATTEMPTS` limits how many providers can be called.

Example:

```text
AI_PROVIDER_CHAIN=gemini,openai,anthropic
AI_MAX_ATTEMPTS=2
```

Only Gemini and OpenAI can be attempted.

### Important

- Fallback is opt-in through configuration.
- Providers are never silently added.
- API keys remain local.
- A failed AI chain does not trigger YouTube publishing.
- The system does not estimate or guarantee API costs; check each provider's current pricing and limits.
