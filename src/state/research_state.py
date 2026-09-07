from dataclasses import asdict, dataclass, field
from typing import Any

from ..schemas.evidence import EvidenceRecord
from ..schemas.plan import ResearchPlan


@dataclass
class ResearchState:
	run_id: str
	scope: dict[str, Any]
	plan: ResearchPlan
	evidence: list[EvidenceRecord] = field(default_factory=list)
	tool_history: list[dict[str, Any]] = field(default_factory=list)
	iteration: int = 0
	tool_calls: int = 0
	tokens: int = 0
	cost_usd: float = 0.0
	defects: list[dict[str, Any]] = field(default_factory=list)
	stage: str = "intake"
	incomplete: bool = False

	def to_dict(self) -> dict[str, Any]:
		return asdict(self)

	def open_questions(self):
		return [q for o in self.plan.objectives for q in o.sub_questions if q.status == "open"]
