import json
import random
import time
from typing import Any

from .usage import Usage, UsageBook


class LLMClient:
	def __init__(self, api_key: str, usage: UsageBook, timeout: float = 30, retries: int = 2):
		self.usage, self.timeout, self.retries = usage, timeout, retries
		self._client = None
		if api_key:
			from openai import OpenAI
			self._client = OpenAI(api_key=api_key, timeout=timeout)

	def complete(self, messages: list[dict[str, str]], stage: str, model: str, tools: list[dict[str, Any]] | None = None) -> Any:
		if not self._client:
			raise RuntimeError("OpenAI client unavailable: set OPENAI_API_KEY for live mode")
		started = time.perf_counter()
		for attempt in range(self.retries + 1):
			try:
				response = self._client.responses.create(model=model, input=messages, tools=tools or [])
				input_tokens = getattr(getattr(response, "usage", None), "input_tokens", 0) or 0
				output_tokens = getattr(getattr(response, "usage", None), "output_tokens", 0) or 0
				self.usage.add(Usage(self.usage.run_id, stage, input_tokens, output_tokens, 0.0, (time.perf_counter() - started) * 1000))
				return response
			except Exception as exc:
				if attempt >= self.retries:
					raise RuntimeError(f"{type(exc).__name__}: {exc}") from exc
				time.sleep(min(8, 2**attempt + random.random()))

	@staticmethod
	def text(response: Any) -> str:
		return getattr(response, "output_text", "") or ""
