from ..schemas.plan import Objective, ResearchPlan, SubQuestion


def plan(scope: dict) -> ResearchPlan:
	topic = scope["objective"]
	objectives = [
		Objective("o1", "Category and vendors", [SubQuestion("q1", f"Which vendors are identified in the corpus for {topic}?", "competitor", ["search_information", "retrieve_document"]), SubQuestion("q2", "What category characteristics are stated by the corpus?", "market", ["search_information", "retrieve_document"])]),
		Objective("o2", "Pricing and differentiation", [SubQuestion("q3", "Which published prices and pricing tiers are supported by sources?", "pricing", ["search_information", "retrieve_document"]), SubQuestion("q4", "What product capabilities and integrations are documented?", "product", ["search_information", "retrieve_document"])]),
		Objective("o3", "Gaps and implications", [SubQuestion("q5", "Which requested facts are not established by the corpus?", "market", ["search_information"]), SubQuestion("q6", "What contradictions or risks require human review?", "trend", ["search_information", "retrieve_document"])]),
	]
	result = ResearchPlan(topic, objectives, scope.get("assumptions", []))
	errors = result.validate()
	if errors:
		raise ValueError("invalid research plan: " + "; ".join(errors))
	return result
