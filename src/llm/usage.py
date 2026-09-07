from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass
class Usage:
	run_id: str
	stage: str
	input_tokens: int = 0
	output_tokens: int = 0
	cost_usd: float = 0.0
	latency_ms: float = 0.0


class UsageBook:
	def __init__(self, run_id: str):
		self.run_id = run_id
		self.calls: list[Usage] = []

	def add(self, usage: Usage) -> None:
		self.calls.append(usage)

	@property
	def total_cost(self) -> float:
		return round(sum(item.cost_usd for item in self.calls), 8)

	@property
	def total_tokens(self) -> int:
		return sum(item.input_tokens + item.output_tokens for item in self.calls)

	def save(self, path: Path) -> None:
		path.write_text(json.dumps({"calls": [asdict(x) for x in self.calls], "total_cost": self.total_cost}, indent=2), encoding="utf-8")
