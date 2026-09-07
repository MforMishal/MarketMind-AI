# MarketMind AI
Deployed here: https://market-mind-aii.streamlit.app/
Bounded, evidence-first business research agent for AAI-412 / PRAC-05.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.main
```

The default mode uses the deterministic corpus in `src/tools/impl/corpus.py`; it never presents model-generated text as retrieved evidence. The run creates `runs/<run_id>/` with the plan, evidence, QC result, report, state, usage summary, and log. Publication requires an explicit `approve` decision; rejection, expansion, and rescoping are not silently approved.

Live OpenAI mode requires `OPENAI_API_KEY` in the environment. Never commit `.env` or a real key. API assumptions and verification date are recorded in `docs/api_verification.md`.

## Controls

The dispatcher resolves tools, parses JSON, validates strict schemas, checks permission and call budgets, catches handler failures, and attaches result IDs. The workflow is bounded by iteration and tool-call caps, uses explicit `unanswerable` gaps, persists serializable state, and runs deterministic QC for unsupported claims, missing evidence, coverage gaps, contradictions, and low confidence.

This repository is a compact runnable foundation. A production submission still needs the student-owned corpus, 18 repeated evaluation cases, screenshots, measured temperature experiment, technical PDF, and manual source spot-checks required by the assignment.
