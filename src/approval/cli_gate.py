def approve(report: dict, input_fn=input) -> dict:
	print("\nApproval required. This system never approves by default.")
	print(f"Objective: {report['research_objective']}")
	print(f"Confidence: {report['confidence_level']} - {report['confidence_rationale']}")
	print(f"Limitations: {len(report['limitations_and_gaps'])}")
	decision = input_fn("Decision [approve/reject/expand/rescope]: ").strip().lower()
	if decision not in {"approve", "reject", "expand", "rescope"}:
		return {"decision": "reject", "notes": "Invalid decision; publication blocked."}
	notes = input_fn("Notes: ").strip()
	return {"decision": decision, "notes": notes}
