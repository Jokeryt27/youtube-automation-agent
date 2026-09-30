# Step 6 — End-to-End Test

The test harness checks:
- content preview generation
- exactly 5 title options
- script/description/tags/thumbnail prompt
- 16:9 thumbnail planning
- human-review checklist
- upload safety when no YouTube token is configured

Run after extracting Step 5 next to the Step 6 folder:

```bash
python run_tests.py
```

A real YouTube upload is NOT performed by this test.
