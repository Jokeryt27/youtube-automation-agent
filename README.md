# YouTube Automation Agent — Step 2

Research-first YouTube workflow.

## Pipeline

Topic → Research → Sources → Script → Titles → Description → Tags → Thumbnail Prompt → Human Review → Optional Upload

## Preview mode

No API key is needed:

```bash
python agent.py --preview "BGMI 4.3 Update"
```

## Live research

The research adapter expects a search API endpoint that returns JSON with a `results` array. Each result can contain:

- `title`
- `url`
- `snippet` or `description`

Set these locally as environment variables:

```text
SEARCH_API_URL=
SEARCH_API_KEY=
```

Never commit real API keys to GitHub.

## Safety

Research is supporting evidence, not automatic fact approval. Review sources, dates, and claims before publishing.
