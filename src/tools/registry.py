from dataclasses import dataclass
from typing import Any, Callable
from ..schemas.tools import TOOLS, schemas
from .impl.corpus import DOCUMENTS, retrieve, search


@dataclass
class Tool:
	name: str
	schema: dict[str, Any]
	handler: Callable[..., Any]
	permission: str
	budget: int
	timeout: float


def calculate_metric(operation: str, values: list[float], period: float = 1) -> dict:
	if operation == "average":
		result = sum(values) / len(values)
		formula = "sum(values) / len(values)"
	elif operation == "ratio":
		result = values[0] / values[1]
		formula = "values[0] / values[1]"
	elif operation == "share":
		result = values[0] / sum(values)
		formula = "values[0] / sum(values)"
	elif operation == "growth_rate":
		result = (values[-1] - values[0]) / values[0]
		formula = "(last - first) / first"
	else:
		result = (values[-1] / values[0]) ** (1 / period) - 1
		formula = "(last / first) ** (1 / period) - 1"
	return {"result": result, "formula": formula, "inputs": values, "operation": operation}


def compare_companies(entities: list[str], attributes: list[str], evidence: list[dict] | None = None) -> dict:
	evidence = evidence or []
	matrix = {}
	for entity in entities:
		matrix[entity] = {}
		for attribute in attributes:
			matches = [item for item in evidence if entity.lower() in item.get("claim", "").lower() and attribute in item.get("claim", "").lower()]
			matrix[entity][attribute] = matches[0]["claim"] if matches else "not established"
	return {"entities": entities, "attributes": attributes, "matrix": matrix}


def build_registry() -> dict[str, Tool]:
	metadata, definitions = TOOLS, schemas()
	return {
		"search_information": Tool("search_information", definitions["search_information"], search, metadata["search_information"]["permission"], 20, 5),
		"retrieve_document": Tool("retrieve_document", definitions["retrieve_document"], retrieve, "read", 20, 5),
		"calculate_metric": Tool("calculate_metric", definitions["calculate_metric"], calculate_metric, "compute", 10, 2),
		"compare_companies": Tool("compare_companies", definitions["compare_companies"], compare_companies, "compute", 10, 5),
		"save_research": Tool("save_research", definitions["save_research"], lambda **args: args, "write", 40, 2),
		"generate_report": Tool("generate_report", definitions["generate_report"], lambda **args: args, "write", 2, 5),
	}
