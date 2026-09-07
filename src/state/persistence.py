import json
from pathlib import Path
from .research_state import ResearchState


def save_state(state: ResearchState, directory: Path) -> Path:
	directory.mkdir(parents=True, exist_ok=True)
	path = directory / "state.json"
	path.write_text(json.dumps(state.to_dict(), indent=2), encoding="utf-8")
	return path
