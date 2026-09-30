# YouTube Automation Agent — Step 1

Generate a **draft** YouTube script, 5 title options, description, tags, and a thumbnail prompt from one topic. A person must verify facts and approve everything before publication. **This version does not upload to YouTube.**

## Requirements

- Python 3.10 or later
- Internet and a funded API account for AI generation (API usage may cost money)
- No third-party Python packages required

## Quick test (free, no API key)

```bash
python agent.py "BGMI update" --preview
```

This prints a **template**, not an AI-generated script.

## AI generation

Set your API key **only on your own device** (do not commit it to GitHub):

macOS/Linux:
```bash
export OPENAI_API_KEY="your-key-here"
python agent.py "BGMI update" --language "Hindi / Hinglish" --channel "Little Toxic"
```

Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="your-key-here"
python agent.py "BGMI update" --language "Hindi / Hinglish" --channel "Little Toxic"
```

Optional model selection: set `OPENAI_MODEL` to a model available to your API account. The default is `gpt-4.1-mini`.

The package is saved in `output/content-package.json` (ignored by Git). Read `fact_check_notes` and independently verify all time-sensitive claims. No research or fact-checking API is connected in Step 1.

## Upload to GitHub from mobile

Open your repo → **Add file** → **Upload files** → upload the individual files from this ZIP (not the ZIP itself) → **Commit changes**. To replace `agent.py` on mobile, open the file → pencil/edit → paste the new content, or delete the old file and upload the replacement. Never upload API keys, `.env`, or generated private content.
