# API verification

Verified 2026-09-07 against the official OpenAI API documentation for the Responses API, tools, and structured outputs.

The implementation isolates live calls in `src/llm/client.py` and uses `responses.create`. The default demonstration uses the deterministic local corpus, so it does not claim external facts or require an API key. Model names and pricing must be rechecked before a live submission run.
