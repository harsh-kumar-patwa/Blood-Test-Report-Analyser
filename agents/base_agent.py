from crewai import Agent as CrewAIAgent
from pydantic import Field
from typing import Any

class CustomAgent(CrewAIAgent):
    gemini_api: Any = Field(default=None, exclude=True)

    def __init__(self, *args, **kwargs):
        gemini_api = kwargs.pop('gemini_api', None)
        super().__init__(*args, **kwargs)
        self.gemini_api = gemini_api

    def execute_task(self, task):
        # This method will be overridden in child classes
        raise NotImplementedError