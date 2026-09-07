def analyse(request: str) -> dict:
	if not isinstance(request, str) or not 1 <= len(request.strip()) <= 1000:
		raise ValueError("request must be between 1 and 1000 characters")
	text = request.strip()
	ambiguities = []
	defaults = {"entity_type": "software vendors", "segment": "not specified", "geography": "global", "time_horizon": "current state", "deliverable_type": "business intelligence report"}
	for field, prompt in (("segment", "Which customer segment should be covered?"), ("geography", "Which geography should be covered?"), ("time_horizon", "What time horizon should be used?")):
		if defaults[field] not in text.lower() and field not in text.lower():
			ambiguities.append({"field": field, "question": prompt, "assumption": defaults[field]})
	return {"objective": text, "entity_type": defaults["entity_type"], "segment": defaults["segment"], "geography": defaults["geography"], "time_horizon": defaults["time_horizon"], "deliverable_type": defaults["deliverable_type"], "ambiguities": ambiguities, "assumptions": [f"{item['field']} assumed as {item['assumption']}" for item in ambiguities]}
