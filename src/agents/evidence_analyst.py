from ..schemas.evidence import EvidenceRecord


def analyse_result(question_id: str, result: dict, result_id: str) -> list[EvidenceRecord]:
	records = []
	if not result.get("ok"):
		return records
	data = result.get("data", {})
	if "snippet" in data:
		data = [data]
	if isinstance(data, dict) and "text" in data:
		data = [data]
	for index, item in enumerate(data if isinstance(data, list) else []):
		claim = item.get("snippet", item.get("text", "")).strip()
		if claim:
			records.append(EvidenceRecord(f"ev-{result_id}-{index}", question_id, claim, "fact", result_id, "search_result", {"title": item.get("title", "")}, "medium", item.get("date", "unknown"), [], "medium", "Corpus result; requires human verification."))
	return records
