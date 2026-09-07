from dataclasses import asdict
from datetime import datetime, timezone
from ..schemas.report import Finding, Report
from .quality_control import check


def generate(state, scope: dict) -> Report:
	evidence = state.evidence
	findings = [Finding(item.claim, item.claim_type, [item.evidence_id], item.confidence) for item in evidence]
	limitations = [f"Could not establish: {q.question}" for q in state.open_questions()]
	if not limitations:
		limitations = ["Claims remain bounded by the local corpus and require human verification."]
	report = Report(state.run_id, datetime.now(timezone.utc).isoformat(), {"local": "deterministic-corpus"}, state.cost_usd, scope["objective"], "Summary derived only from the evidence appendix.", findings, [], {"matrix": {}}, [], [], [asdict(item) for item in evidence], [], "medium" if evidence else "low", "Based on corpus coverage, source quality, and unresolved gaps.", limitations, [item.source_detail for item in evidence], None)
	state.defects = check(report, state)
	return report
