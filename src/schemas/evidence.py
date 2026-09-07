from dataclasses import asdict, dataclass, field
from typing import Any

CLAIM_TYPES = {"fact", "inference", "recommendation", "uncertainty"}


@dataclass
class EvidenceRecord:
	evidence_id: str
	question_id: str
	claim: str
	claim_type: str
	source_ref: str
	source_kind: str
	source_detail: dict[str, Any] = field(default_factory=dict)
	credibility: str = "unknown"
	recency: str = "unknown"
	corroboration: list[str] = field(default_factory=list)
	confidence: str = "low"
	analyst_notes: str = ""

	def validate(self) -> list[str]:
		errors = []
		if self.claim_type not in CLAIM_TYPES:
			errors.append("invalid claim_type")
		if self.confidence not in {"high", "medium", "low"}:
			errors.append("invalid confidence")
		if not self.source_ref:
			errors.append("source_ref is required")
		return errors

	def to_dict(self) -> dict[str, Any]:
		return asdict(self)
