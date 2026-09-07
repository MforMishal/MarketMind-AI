import argparse
import json
import sys
import uuid
from dataclasses import asdict
from pathlib import Path

from .agents.evidence_analyst import analyse_result
from .agents.planner import plan
from .agents.report_generator import generate
from .agents.request_analyser import analyse
from .approval.cli_gate import approve
from .config import configure_logging, load_settings
from .schemas.evidence import EvidenceRecord
from .state.persistence import save_state
from .state.research_state import ResearchState
from .tools.dispatcher import Dispatcher


def run(request: str, approve_fn=None) -> dict:
	settings = load_settings()
	run_id = uuid.uuid4().hex[:12]
	logger = configure_logging(run_id, settings.runs_dir)
	scope = analyse(request)
	research_plan = plan(scope)
	state = ResearchState(run_id, scope, research_plan, stage="research")
	dispatcher = Dispatcher(logger=logger, evidence=state.evidence)
	while state.open_questions() and state.iteration < settings.max_iterations and state.tool_calls < settings.max_tool_calls:
		question = state.open_questions()[0]
		state.iteration += 1
		result = dispatcher.dispatch("search_information", {"query": question.question, "source_type": "all", "max_results": 5}, "read")
		state.tool_calls = dispatcher.calls
		state.tool_history.append(result)
		state.evidence.extend(analyse_result(question.id, result, result.get("result_id", "none")))
		question.status = "answered" if state.evidence else "unanswerable"
		if not result.get("ok") or not result.get("data"):
			question.status = "unanswerable"
	state.incomplete = bool(state.open_questions())
	report = generate(state, scope)
	report_dict = report.to_dict()
	decision = (approve_fn or approve)(report_dict)
	report_dict["approval"] = decision
	target = settings.runs_dir / run_id
	target.mkdir(parents=True, exist_ok=True)
	(target / "plan.json").write_text(json.dumps(research_plan.to_dict(), indent=2), encoding="utf-8")
	(target / "evidence.json").write_text(json.dumps([asdict(item) for item in state.evidence], indent=2), encoding="utf-8")
	(target / "qc.json").write_text(json.dumps(state.defects, indent=2), encoding="utf-8")
	(target / "report.json").write_text(json.dumps(report_dict, indent=2), encoding="utf-8")
	(target / "usage.json").write_text(json.dumps({"tokens": state.tokens, "cost_usd": state.cost_usd, "tool_calls": state.tool_calls}, indent=2), encoding="utf-8")
	save_state(state, target)
	if decision.get("decision") != "approve":
		logger.warning("publication blocked: %s", decision.get("decision"))
	return report_dict


def main() -> int:
	parser = argparse.ArgumentParser(description="Run a bounded MarketMind research run.")
	parser.add_argument("request", nargs="?", default="Research the market for AI-powered customer support software and prepare a business intelligence report.")
	args = parser.parse_args()
	try:
		result = run(args.request)
		print(json.dumps({"run_id": result["report_id"], "decision": result["approval"]["decision"]}, indent=2))
		return 0
	except (RuntimeError, ValueError) as exc:
		print(f"error: {exc}", file=sys.stderr)
		return 2


if __name__ == "__main__":
	raise SystemExit(main())
