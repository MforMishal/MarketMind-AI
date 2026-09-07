import json
from typing import Any
from .registry import Tool, build_registry


def validate(schema: dict, value: dict) -> list[str]:
	errors = []
	if not isinstance(value, dict):
		return ["arguments must be an object"]
	missing = set(schema.get("required", [])) - set(value)
	errors.extend(f"missing field: {name}" for name in missing)
	errors.extend(f"unknown field: {name}" for name in set(value) - set(schema.get("properties", {})))
	for name, rule in schema.get("properties", {}).items():
		if name not in value:
			continue
		item = value[name]
		if rule.get("type") == "string" and (not isinstance(item, str) or len(item) < rule.get("minLength", 0) or len(item) > rule.get("maxLength", 10**9)):
			errors.append(f"invalid field: {name}")
		if rule.get("type") == "integer" and (not isinstance(item, int) or item < rule.get("minimum", -10**9) or item > rule.get("maximum", 10**9)):
			errors.append(f"invalid field: {name}")
		if rule.get("enum") and item not in rule["enum"]:
			errors.append(f"invalid field: {name}; expected one of {rule['enum']}")
		if rule.get("type") == "array" and (not isinstance(item, list) or len(item) < rule.get("minItems", 0) or len(item) > rule.get("maxItems", 10**9)):
			errors.append(f"invalid field: {name}")
	return errors


class Dispatcher:
	def __init__(self, registry: dict[str, Tool] | None = None, logger=None, evidence=None):
		self.registry = registry or build_registry()
		self.logger = logger
		self.evidence = evidence or []
		self.calls = 0
		self.results: dict[str, Any] = {}

	def dispatch(self, name: str, arguments: str | dict, permission: str = "read") -> dict[str, Any]:
		if name not in self.registry:
			return {"ok": False, "error": "unknown tool", "available": sorted(self.registry)}
		tool = self.registry[name]
		try:
			args = json.loads(arguments) if isinstance(arguments, str) else arguments
		except json.JSONDecodeError as exc:
			return {"ok": False, "error": f"malformed JSON arguments: {exc.msg}"}
		errors = validate(tool.schema, args)
		if errors:
			return {"ok": False, "error": "; ".join(errors)}
		if permission == "read" and tool.permission == "write":
			return {"ok": False, "error": "permission denied"}
		if self.calls >= tool.budget:
			return {"ok": False, "error": "tool call budget exceeded"}
		self.calls += 1
		if name == "compare_companies":
			args["evidence"] = self.evidence
		if name == "save_research" and args["source_ref"] not in self.results:
			return {"ok": False, "error": f"source_ref does not resolve: {args['source_ref']}"}
		try:
			result = tool.handler(**args)
		except Exception as exc:
			return {"ok": False, "error": f"tool execution failed: {type(exc).__name__}: {exc}"}
		result_id = f"result-{self.calls}"
		self.results[result_id] = result
		if name == "save_research":
			self.evidence.append({"claim": args["claim"], "evidence_id": result_id, **args})
		return {"ok": True, "result_id": result_id, "tool": name, "data": result}
