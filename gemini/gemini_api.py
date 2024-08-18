import requests
from config import GEMINI_API_KEY, SEARCH_WEB_KEY, SEARCH_WEB_ENGINE_ID

class GoogleGeminiAPI:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

    def _make_api_request(self, prompt):
        url = f"{self.api_url}?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None

    def generate_summary(self, text):
        prompt = f"Provide a concise summary of the following blood test report:\n\n{text}"
        response_json = self._make_api_request(prompt)
        
        if response_json:
            try:
                return response_json['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError) as e:
                print(f"Error extracting summary from response: {e}")
        return ""

    def web_search(self, query):
        search_url = "https://customsearch.googleapis.com/customsearch/v1"
        params = {
            "key": SEARCH_WEB_KEY,
            "cx": SEARCH_WEB_ENGINE_ID,
            "q": query
        }
        response = requests.get(search_url, params=params)
        
        if response.status_code == 200:
            response_json = response.json()
            try:
                return [f"{item['title']} - {item['link']}" for item in response_json.get('items', [])]
            except KeyError as e:
                print(f"Error extracting articles from response: {e}")
        else:
            print(f"API Error: {response.status_code} - {response.text}")
        return []

    def generate_recommendations(self, prompt):
        response_json = self._make_api_request(prompt)
        
        if response_json:
            try:
                return response_json['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError) as e:
                print(f"Error extracting recommendations from response: {e}")
        return ""