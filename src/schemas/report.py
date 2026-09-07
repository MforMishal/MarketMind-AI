from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Finding:
	statement: str
	claim_type: str
	evidence_ids: list[str] = field(default_factory=list)
	confidence: str = "low"


@dataclass
class Report:
	report_id: str
	generated_at: str
	model_versions: dict[str, str]
	run_cost: float
	research_objective: str
	executive_summary: str
	market_overview: list[Finding]
	key_trends: list[Finding]
	competitor_analysis: dict[str, Any]
	opportunities: list[Finding]
	risks: list[Finding]
	evidence_appendix: list[dict[str, Any]]
	recommendations: list[Finding]
	confidence_level: str
	confidence_rationale: str
	limitations_and_gaps: list[str]
	sources: list[dict[str, Any]]
	approval: dict[str, Any] | None = None

	def validate(self, evidence_ids: set[str]) -> list[str]:
		errors = []
		for group in (self.market_overview, self.key_trends, self.opportunities, self.risks, self.recommendations):
			for finding in group:
				if finding.claim_type == "fact" and not finding.evidence_ids:
					errors.append("fact finding has no evidence")
				if not set(finding.evidence_ids) <= evidence_ids:
					errors.append("finding references missing evidence")
		if not self.limitations_and_gaps:
			errors.append("limitations_and_gaps must not be empty")
		return errors

	def to_dict(self) -> dict[str, Any]:
		return asdict(self)
