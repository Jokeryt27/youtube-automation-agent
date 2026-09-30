
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent / "youtube-automation-agent-step5"

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

checks = []

# Step 3 preview
p = run([sys.executable, str(ROOT / "agent.py"), "--preview", "BGMI New Update"])
checks.append(("Content preview", p.returncode == 0))
if p.returncode == 0:
    data = json.loads(p.stdout)
    checks += [
        ("5 titles", len(data["titles"]) == 5),
        ("Script present", bool(data["script"].strip())),
        ("Description present", bool(data["description"].strip())),
        ("Tags present", len(data["tags"]) > 0),
        ("Thumbnail prompt present", bool(data["thumbnail_prompt"].strip())),
    ]

# Step 4 thumbnail
p = run([sys.executable, str(ROOT / "thumbnail.py"), "BGMI New Update", "BGMI New Update — What's New?"])
checks.append(("Thumbnail planner", p.returncode == 0))
if p.returncode == 0:
    data = json.loads(p.stdout)
    checks += [
        ("16:9 thumbnail", data["aspect_ratio"] == "16:9"),
        ("Review checklist", len(data["review_checklist"]) >= 4),
    ]

# Step 5 upload safety check: no token should fail before any upload.
p = run([sys.executable, str(ROOT / "youtube_upload.py"), "missing.mp4", "Test", "Test"])
checks.append(("Upload blocks without token", p.returncode != 0))

for name, ok in checks:
    print(("PASS" if ok else "FAIL") + " - " + name)

print(f"\nResult: {sum(ok for _, ok in checks)}/{len(checks)} checks passed")
if not all(ok for _, ok in checks):
    raise SystemExit(1)
