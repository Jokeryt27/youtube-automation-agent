"""YouTube content-package generator. Requires Python 3.10+."""
import argparse
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def generate_with_ai(topic: str, language: str, channel: str) -> dict:
    key = os.getenv('OPENAI_API_KEY', '').strip()
    if not key:
        raise RuntimeError('OPENAI_API_KEY is missing. Set it locally; never upload it to GitHub.')
    instruction = (
        'Create a YouTube content package as a JSON object with exactly these keys: '
        'topic (string), titles (array of 5 strings), script (string), description (string), '
        'tags (array of 12 strings), thumbnail_prompt (string), fact_check_notes (array of strings), '
        'review_required (boolean, true). Write in the requested language. '
        'Do not invent facts, statistics, product specifications, or release dates. '
        'Mark claims requiring current verification in fact_check_notes. '
        'Make the script engaging, clear, and ready for human editing; avoid clickbait promises.'
    )
    payload = {
        'model': os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'),
        'instructions': instruction,
        'input': f'Topic: {topic}\nLanguage: {language}\nChannel: {channel}\n'
                 'Make the script approximately 500-700 words if the topic permits.',
        'text': {'format': {'type': 'json_object'}},
    }
    req = Request(
        'https://api.openai.com/v1/responses',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urlopen(req, timeout=90) as response:
            result = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f'API request failed (HTTP {exc.code}). Check API key, billing, and model access.') from exc
    except URLError as exc:
        raise RuntimeError(f'Network error: {exc.reason}') from exc
    parts = [part.get('text', '') for item in result.get('output', [])
             for part in item.get('content', []) if part.get('type') == 'output_text']
    if not parts:
        raise RuntimeError('API returned no text output.')
    try:
        package = json.loads(''.join(parts))
    except json.JSONDecodeError as exc:
        raise RuntimeError('API output was not valid JSON.') from exc
    required = {'topic', 'titles', 'script', 'description', 'tags', 'thumbnail_prompt', 'fact_check_notes'}
    if not isinstance(package, dict) or not required.issubset(package):
        raise RuntimeError('API output is missing required fields.')
    package['review_required'] = True
    return package


def preview_package(topic: str, language: str, channel: str) -> dict:
    """Clearly labeled template for testing without an API key; not AI-generated."""
    return {
        'topic': topic,
        'titles': [f'{topic} | Complete Guide', f'{topic} | What You Should Know',
                   f'{topic} | Key Details', f'{topic} | Explained Simply',
                   f'{topic} | Quick Overview'],
        'script': (f'[TEMPLATE ONLY — write and verify the actual script]\n'
                   f'Hook: Why does {topic} matter?\n'
                   'Intro: Introduce the topic.\n'
                   'Main section: Add 3-5 verified points and examples.\n'
                   'Outro: Summarize and invite viewers to comment.'),
        'description': f'{topic}: An overview from {channel}. Verify details before publishing.',
        'tags': [topic, channel, 'YouTube', 'guide'],
        'thumbnail_prompt': f'Dark cinematic YouTube thumbnail about {topic}; one clear focal point; short readable text; no unverified claims.',
        'fact_check_notes': ['Template only: all factual claims must be checked before publishing.'],
        'review_required': True,
        'mode': 'preview_template_not_ai',
        'language': language,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate a YouTube content package.')
    parser.add_argument('topic', nargs='?', help='Video topic; prompted if omitted')
    parser.add_argument('--language', default='Hindi / Hinglish')
    parser.add_argument('--channel', default='Little Toxic')
    parser.add_argument('--preview', action='store_true', help='Generate a template without AI/API calls')
    parser.add_argument('--output', default='output/content-package.json')
    args = parser.parse_args()
    topic = (args.topic or input('Enter YouTube topic: ')).strip()
    if not topic:
        parser.error('Topic cannot be empty.')
    try:
        package = (preview_package(topic, args.language, args.channel) if args.preview
                   else generate_with_ai(topic, args.language, args.channel))
    except RuntimeError as exc:
        parser.exit(1, f'Error: {exc}\nTry --preview to test without an API key.\n')
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(package, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(package, ensure_ascii=False, indent=2))
    print(f'\nSaved to: {path}')
    print('REVIEW REQUIRED: Verify facts and edit before uploading.')


if __name__ == '__main__':
    main()
