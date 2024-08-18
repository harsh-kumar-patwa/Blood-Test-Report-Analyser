from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional
from gemini.gemini_api import GoogleGeminiAPI

class GeminiLLM(LLM):
    gemini_api: GoogleGeminiAPI = None

    def __init__(self, gemini_api: GoogleGeminiAPI):
        super().__init__()
        self.gemini_api = gemini_api

    @property
    def _llm_type(self) -> str:
        return "gemini"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return self.gemini_api.generate_summary(prompt)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"gemini_api": self.gemini_api}