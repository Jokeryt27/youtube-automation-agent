# YouTube Automation Agent — Step 3

Research → AI Content Package.

## Output

The agent generates:

- Complete YouTube script
- 5 title options
- Description
- Tags
- Thumbnail prompt

## Preview test

```bash
python agent.py --preview "BGMI 4.3 Update"
```

With research JSON:

```bash
python agent.py --preview "BGMI 4.3 Update" research.json
```

## Live AI generation

Set these locally:

```text
OPENAI_API_KEY=
OPENAI_API_URL=https://api.openai.com/v1/chat/completions
OPENAI_MODEL=gpt-4.1-mini
```

Never commit a real API key to GitHub.

## Review

Generated content is a draft. Verify research, dates, claims, names, numbers and source links before publishing.
