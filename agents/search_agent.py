from agents.base_agent import CustomAgent

class ArticleSearchAgent(CustomAgent):
    def execute_task(self, task):
        search_query = f"Health articles link related to: {task}"
        articles = self.gemini_api.web_search(search_query)
        return articles[:5]  # Limit to top 5 articles for relevance