from agents.base_agent import CustomAgent

class BloodTestAnalysisAgent(CustomAgent):
    def execute_task(self, task):
        prompt = (
            f"Analyze the following blood test report and provide a summary that is "
            f"understandable to a person without medical knowledge. Highlight any "
            f"significant findings and potential areas of concern:\n\n{task}"
        )
        return self.gemini_api.generate_summary(prompt)