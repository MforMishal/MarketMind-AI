import json
from pathlib import Path


def main() -> None:
	cases = json.loads(Path(__file__).with_name("test_cases.json").read_text(encoding="utf-8"))
	print(json.dumps({"case_count": len(cases), "fail_cases_repeat_count": 3, "status": "manifest ready"}, indent=2))


if __name__ == "__main__":
	main()
