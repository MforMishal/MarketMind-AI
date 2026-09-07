from dataclasses import dataclass
import logging
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
	api_key: str = ""
	planning_model: str = "gpt-5-mini"
	research_model: str = "gpt-5-mini"
	synthesis_model: str = "gpt-5-mini"
	max_iterations: int = 20
	max_tool_calls: int = 40
	max_repair_rounds: int = 2
	budget_usd: float = 2.0
	timeout_seconds: float = 30.0
	max_retries: int = 2
	corpus_dir: Path = Path("corpus")
	runs_dir: Path = Path("runs")


def load_settings(require_api_key: bool = False) -> Settings:
	key = os.getenv("OPENAI_API_KEY", "")
	if require_api_key and not key:
		raise RuntimeError("Missing required environment variable: OPENAI_API_KEY")
	return Settings(
		api_key=key,
		planning_model=os.getenv("MARKETMIND_PLANNING_MODEL", "gpt-5-mini"),
		research_model=os.getenv("MARKETMIND_RESEARCH_MODEL", "gpt-5-mini"),
		synthesis_model=os.getenv("MARKETMIND_SYNTHESIS_MODEL", "gpt-5-mini"),
		max_iterations=int(os.getenv("MARKETMIND_MAX_ITERATIONS", "20")),
		max_tool_calls=int(os.getenv("MARKETMIND_MAX_TOOL_CALLS", "40")),
		max_repair_rounds=int(os.getenv("MARKETMIND_MAX_REPAIR_ROUNDS", "2")),
		budget_usd=float(os.getenv("MARKETMIND_BUDGET_USD", "2")),
		timeout_seconds=float(os.getenv("MARKETMIND_TIMEOUT_SECONDS", "30")),
		max_retries=int(os.getenv("MARKETMIND_MAX_RETRIES", "2")),
		corpus_dir=Path(os.getenv("MARKETMIND_CORPUS_DIR", "corpus")),
		runs_dir=Path(os.getenv("MARKETMIND_RUNS_DIR", "runs")),
	)


def configure_logging(run_id: str, runs_dir: Path) -> logging.Logger:
	logger = logging.getLogger(f"marketmind.{run_id}")
	logger.setLevel(logging.INFO)
	if not logger.handlers:
		target = runs_dir / run_id
		target.mkdir(parents=True, exist_ok=True)
		formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
		console = logging.StreamHandler()
		console.setFormatter(formatter)
		file_handler = logging.FileHandler(target / "run.log", encoding="utf-8")
		file_handler.setFormatter(formatter)
		logger.addHandler(console)
		logger.addHandler(file_handler)
	return logger
