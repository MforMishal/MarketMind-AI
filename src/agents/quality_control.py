def check(report, state) -> list[dict]:
	defects = []
	evidence_ids = {item.evidence_id for item in state.evidence}
	for finding in report.key_trends + report.market_overview + report.opportunities + report.risks + report.recommendations:
		if finding.claim_type == "fact" and not finding.evidence_ids:
			defects.append({"type": "unsupported_claim", "severity": "high", "location": finding.statement, "gap_question": "Find a source supporting this fact."})
		if not set(finding.evidence_ids) <= evidence_ids:
			defects.append({"type": "missing_source", "severity": "high", "location": finding.statement, "gap_question": "Retrieve the missing evidence source."})
	covered = {item.question_id for item in state.evidence}
	for question in state.open_questions():
		if question.id not in covered:
			defects.append({"type": "coverage_gap", "severity": "medium", "location": question.id, "gap_question": question.question})
	if any("conflict" in item.claim.lower() or "disagree" in item.claim.lower() for item in state.evidence):
		defects.append({"type": "contradiction", "severity": "medium", "location": "evidence", "gap_question": "Compare the conflicting source claims and preserve both."})
	if any(item.confidence == "low" for item in state.evidence):
		defects.append({"type": "low_confidence", "severity": "low", "location": "evidence", "gap_question": "Find corroborating evidence."})
	return defects
