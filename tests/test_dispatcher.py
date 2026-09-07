import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.tools.dispatcher import Dispatcher


def test_invalid_calls_are_structured_errors():
    dispatcher = Dispatcher()
    assert dispatcher.dispatch("unknown", {})["ok"] is False
    assert dispatcher.dispatch("search_information", "{")["ok"] is False
    assert dispatcher.dispatch("search_information", {"query": "x", "max_results": 21})["ok"] is False
    assert dispatcher.dispatch("save_research", {"question_id": "q", "claim": "x", "claim_type": "fact", "source_ref": "missing", "confidence": "low"}, "write")["ok"] is False