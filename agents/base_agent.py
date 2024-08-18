from crewai import Agent as CrewAIAgent

class CustomAgent(CrewAIAgent):
    def __init__(self, *args, **kwargs):
        self.gemini_api = kwargs.pop('gemini_api', None)
        super().__init__(*args, **kwargs)

    def execute_task(self, task):
        # This method will be overridden in child classes
        raise NotImplementedError