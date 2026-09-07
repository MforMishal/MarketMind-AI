TOOLS = {
	"search_information": {"permission": "read", "budget": 20, "timeout": 5},
	"retrieve_document": {"permission": "read", "budget": 20, "timeout": 5},
	"calculate_metric": {"permission": "compute", "budget": 10, "timeout": 2},
	"compare_companies": {"permission": "compute", "budget": 10, "timeout": 5},
	"save_research": {"permission": "write", "budget": 40, "timeout": 2},
	"generate_report": {"permission": "write", "budget": 2, "timeout": 5},
}

def schemas() -> dict:
	return {
		"search_information": {"type": "object", "required": ["query"], "additionalProperties": False, "properties": {"query": {"type": "string", "minLength": 1, "maxLength": 300}, "source_type": {"type": "string", "enum": ["all", "vendor", "pricing", "press"]}, "max_results": {"type": "integer", "minimum": 1, "maximum": 20}, "recency_window": {"type": "string", "enum": ["1y", "3y", "5y", "any"]}}},
		"retrieve_document": {"type": "object", "required": ["document_id"], "additionalProperties": False, "properties": {"document_id": {"type": "string", "minLength": 1, "maxLength": 100}, "section": {"type": "string", "maxLength": 100}}},
		"calculate_metric": {"type": "object", "required": ["operation", "values"], "additionalProperties": False, "properties": {"operation": {"type": "string", "enum": ["growth_rate", "cagr", "share", "ratio", "average"]}, "values": {"type": "array", "minItems": 1, "maxItems": 20, "items": {"type": "number"}}, "period": {"type": "number", "minimum": 1, "maximum": 100}}},
		"compare_companies": {"type": "object", "required": ["entities", "attributes"], "additionalProperties": False, "properties": {"entities": {"type": "array", "minItems": 1, "maxItems": 20, "items": {"type": "string", "minLength": 1, "maxLength": 100}}, "attributes": {"type": "array", "minItems": 1, "maxItems": 10, "items": {"type": "string", "enum": ["pricing", "target_customer", "integrations", "deployment", "funding"]}}}},
		"save_research": {"type": "object", "required": ["question_id", "claim", "claim_type", "source_ref", "confidence"], "additionalProperties": False, "properties": {"question_id": {"type": "string"}, "claim": {"type": "string", "minLength": 1, "maxLength": 1000}, "claim_type": {"type": "string", "enum": ["fact", "inference", "recommendation", "uncertainty"]}, "source_ref": {"type": "string"}, "confidence": {"type": "string", "enum": ["high", "medium", "low"]}}},
		"generate_report": {"type": "object", "required": ["run_id"], "additionalProperties": False, "properties": {"run_id": {"type": "string"}, "sections": {"type": "array", "maxItems": 20, "items": {"type": "string"}}}},
	}
