from agents.base_agent import CustomAgent

class HealthRecommendationAgent(CustomAgent):
    def execute_task(self, task):
        prompt = (
            f"Based on the following blood test analysis summary and related articles, "
            f"provide specific health recommendations:\n\n{task}\n\n"
            f"Please provide actionable recommendations "
            f"for improving health based on the blood test results and information from the articles."
        )
        return self.gemini_api.generate_recommendations(prompt)