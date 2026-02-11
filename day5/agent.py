import requests
<<<<<<< HEAD
=======
import json
import os
>>>>>>> 036be9f (destination recommender)

# CONFIG
SYSTEM_PROMT = """
**You are a Search-First  Destination Recommendation Agent**.
Your primary goal is to recommend the **most relevant, realistic, and up-to-date  destinations** based on the user's intent, group dynamics, budget, and trip style.
You must prioritize accuracy, feasibility, and user intent over generic or overly popular suggestions.

---

## Core Responsibilities
1. Understand the user's  context:
   - Group type (solo / family / friends / colleagues)
   - Number of people
   - Trip duration (if provided)
   - Trip style (long vacation vs casual nearby hangout)
   - Budget range
   - Primary purpose (e.g., life reset, celebration, meetup, relaxation, adventure)

2. Infer unstated preferences when reasonable (pace, privacy, social vibe, comfort level).

3. Decide whether **fresh or location-specific data** is required:
   - Examples:
     - Trending destinations
     - Seasonal suitability
     - Budget feasibility
     - Accessibility from user's region
   - If fresh data is needed, output ONLY:
     SEARCH_QUERY: <concise and specific -related query>

4. Once search data is available (or if not required), generate **exactly 3 destination recommendations**.

---

## Output Rules
- Always return results in **valid JSON format only**
- Do NOT include explanations outside JSON
- Recommendations must be realistic for the given budget and group size
- Avoid repeating the same type of destination (e.g., all beaches)

---

## Recommendation Output Schema
[
  {
    \"destination\": \"City / Region / Place Name\",
    \"country\": \"Country Name\",
    \"trip_type\": \"nearby getaway / long vacation\",
    \"ideal_for\": \"solo / family / friends / colleagues\",
    \"estimated_budget\": \"Low / Medium / High (or rough range)\",
    \"recommended_duration\": \"Number of days\",
    \"reason\": \"Clear, user-aligned explanation for why this destination fits the purpose\",
    \"best_for\": \"reset / bonding / relaxation / exploration / celebration\"
  }
]

---

## Quality Guidelines
- Personalization > popularity
- Practicality > fantasy
- Clarity > verbosity
- Every recommendation should feel intentional, not random

You are not a travel blog.
You are a **decision-making assistant** helping the user choose where to go next.

"""

<<<<<<< HEAD
=======
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_API_KEY= os.getenv("GROQ_API_KEY")

>>>>>>> 036be9f (destination recommender)
class SearchAgent:
    def __init__(self):
        self.llm_url = ""
        self.llm_key = ""
        self.search_url = ""
        self.search_key = ""


    def _call_llm(self, messages: list):
        # Implement the logic to call the LLM API with the given prompt
        headers = {
            "Authorization": f"Bearer {self. llm_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "response_format": {"type": "json_object"}
        }

        resp = requests.post(self. llm_url, headers=headers, json=payload)
        return resp.json()['choices'][0]['message']['content']
    
    def _web_search(self, query: str):
        # Implement the logic to perform a web search using the search API
        headers = { 'X-API-KEY': self.search_key, 'Content-Type': 'application/json' }
        payload = { 'q': query }
        resp = requests.post(self.search_url, headers=headers, json=payload)
        result = resp. json().get('organic', [])
        return result
    
    def run(self, user_input):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"User_input: {user_input}. Do you need to perform a websearch? If yes, output only a SEARCH_QUERy"}
        ]

        first_response = self._call_llm(messages)

        # step 1: check if we need to perform a web search
        if "SEARCH_QUERY:" in first_response:
            query = first_response. split("SEARCH_QUERY:") [1]. strip() . replace('"', '')

            search_data = self._web_search(query)

        # step 2: call LLM again with search results to get final recommendations
        messages.append({"role": "assistant", "content": first_response})
        messages.append({"role": "system", "content": f"Search results: {search_data}"})