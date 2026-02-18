import requests
import json
import os

# CONFIG
SYSTEM_PROMPT = """
    You are a Daily News Summarization Agent.

    Your job is to deliver a concise, accurate, and up-to-date news briefing
    tailored to the user's interests and available reading time.

    ---

    ## Core Responsibilities

    1. Understand user preferences:
        - Interested domains/topics
        - Time budget (e.g., 2 min, 5 min)
        - Desired depth (quick scan vs meaningful understanding)

    2. ALWAYS use fresh news data (last 24–48 hours).

    3. Decide the optimal number of stories based on time:
        - 2 min → ~3–4 key stories
        - 5 min → ~6–8 stories
        - 10 min → ~10–12 stories

    4. Prioritize:
        - Relevance to user interests
        - Impact and importance
        - Clarity over noise

    ---

    ## Search Behavior

    Before summarizing, you MUST request a web search.
    Output ONLY the following format:

    SEARCH_QUERY: <concise query including topic + recency>

    Example:
    SEARCH_QUERY: latest AI and tech news last 24 hours

    ---

    ## Final Output Rules

    - Output ONLY valid JSON
    - No explanations outside JSON
    - Summaries must fit the stated time budget
    - Avoid clickbait or speculation
    - Be neutral and factual

    ---

    ## Output Schema

    {
    "time_budget": "2 min / 5 min",
    "date": "YYYY-MM-DD",
    "topics": ["AI", "Finance"],
    "summary": [
        {
        "headline": "Short clear headline",
        "source": "News outlet",
        "summary": "2–3 sentence concise explanation",
        "why_it_matters": "One sentence relevance"
        }
    ]
    }

    You are not a news aggregator.
    You are a clarity engine for busy humans.
"""

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_API_KEY= os.getenv("GROQ_API_KEY")
SEARCH_KEY = os.getenv("SEARCH_KEY")

class NewsAgent:
    def __init__(self):
        self.llm_url = GROQ_BASE_URL + "/chat/completions"
        self.llm_key = GROQ_API_KEY
        self.search_url = 'https://google.serper.dev/search'
        self.search_key = SEARCH_KEY

    def _call_llm(self, messages: list):
        """call LLM to tell us what to search on websearch tool"""

        headers = {
            "Authorization": f"Bearer {self.llm_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "response_format": {"type": "json_object"}
        }

        resp = requests.post(self.llm_url, headers=headers, json=payload)
        response = resp.json()["choices"][0]["message"]["content"]

        print("LLM response")
        print(response)

        return response

    def _web_search(self, query: str):
        headers = {
            "X-API-KEY": self.search_key,
            "Content-Type": "application/json"
        }
        payload = {"q": query}
        resp = requests.post(self.search_url, headers=headers, json=payload)
        response = resp.json().get("organic", [])

        print("Web Search")
        print(response)

        return response
    
    def _convert_to_json(self, response_str):
        try:
            json_data = response_str.strip()
            if json_data.startswith("```json"):
                json_data = json_data[len("```json"):].strip()
            if json_data.endswith("```"):
                json_data = json_data[:-len("```")].strip()
            return eval(json_data)
        except Exception as e:
            print(f'Error converting to JSON: {e}')
            return()

    def run(self, user_input):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""User_input: {user_input}. Do you need to perform web search? if Yes output only a SEARCH_QUERY in the format: 'SEARCH_QUERY: <query>'. If No provide the summary in json format"""}
        ]

        first_response = self._call_llm(messages)

        if "SEARCH_QUERY:" in first_response:
            query = first_response.split("SEARCH_QUERY:")[1].strip().replace('"', '')
            search_data = self._web_search(query)

            messages.append({"role": "assistant", "content": first_response})
            messages.append({"role": "system", "content": f"Search results:{search_data}\nNow give the final JSON"})

            final_summary = self._call_llm(messages)
            json_response = self._convert_to_json(final_summary)
            return json_response
        
        return self._convert_to_json(first_response)