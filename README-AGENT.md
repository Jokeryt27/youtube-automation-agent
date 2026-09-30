# Agent Plan — Step 7

## AI providers

1. OpenAI
2. Google Gemini
3. Anthropic

## Provider routing

AI_PROVIDER chooses the active provider.

## Future upgrade

Add an optional fallback chain:

Primary provider → retry → secondary provider → human review

Do not silently switch providers for paid API calls without explicit configuration.
