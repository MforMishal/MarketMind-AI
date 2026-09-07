from dataclasses import asdict, dataclass, field
from typing import Any

TOOLS = {"search_information", "retrieve_document", "calculate_metric", "compare_companies", "save_research", "generate_report"}
EVIDENCE_TYPES = {"pricing", "product", "market", "competitor", "regulatory", "trend"}


@dataclass
class SubQuestion:
	id: str
	question: str
	required_evidence: str = "market"
	candidate_tools: list[str] = field(default_factory=lambda: ["search_information"])
	priority: int = 1
	status: str = "open"


@dataclass
class Objective:
	id: str
	title: str
	sub_questions: list[SubQuestion]


@dataclass
class ResearchPlan:
	objective: str
	objectives: list[Objective]
	assumptions: list[str] = field(default_factory=list)

	def validate(self) -> list[str]:
		errors: list[str] = []
		if not 1 <= len(self.objectives) <= 6:
			errors.append("objectives must contain 1 to 6 items")
		ids: set[str] = set()
		for objective in self.objectives:
			if not 1 <= len(objective.sub_questions) <= 5:
				errors.append(f"{objective.id} must contain 1 to 5 questions")
			for question in objective.sub_questions:
				if question.id in ids:
					errors.append(f"duplicate question id: {question.id}")
				ids.add(question.id)
				if not question.question.strip() or not set(question.candidate_tools) <= TOOLS:
					errors.append(f"invalid question: {question.id}")
				if question.required_evidence not in EVIDENCE_TYPES:
					errors.append(f"invalid evidence type: {question.id}")
		return errors

	def to_dict(self) -> dict[str, Any]:
		return asdict(self)
