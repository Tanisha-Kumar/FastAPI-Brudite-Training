from fastapi import FastAPI
from typing import Optional, List, Literal
from pydantic import BaseModel, Field

from agent import NewsAgent
app = FastAPI()

## schema for user input

NewsDomain = Literal[
    "technology",
    "ai",
    "business",
    "finance",
    "startups",
    "science",
    "health",
    "climate",
    "politics",
    "geopolitics",
    "sports",
    "entertainment",
    "design",
    "culture"
]

TimeBudget = Literal[
    "2_min",
    "5_min",
    "10_min"
]

SummaryDepth = Literal[
    "headlines",      # ultra short
    "brief",          # 2–3 sentences per story
    "insight"         # context + implications
]

NewsRegion = Literal[
    "global",
    "us",
    "europe",
    "asia",
    "middle_east",
    "india"
]

# ---- main request schema ----

class NewsSummaryRequest(BaseModel):
    user_inp:str

    domains: List[NewsDomain] = Field(
        ...,
        description="Topics the user wants news about",
        example=["ai", "startups", "technology"]
    )

    time_budget: TimeBudget = Field(
        ...,
        description="How much time the user wants to spend reading",
        example="5_min"
    )

    summary_depth: SummaryDepth = Field(
        "brief",
        description="Level of detail in the summaries",
        example="brief"
    )

    region: NewsRegion = Field(
        "global",
        description="Geographical focus of the news",
        example="global"
    )

@app.get("/")
def read_root():
    return{"message": "Welcome Newz Summariser"}

@app.post("/summary")
def summarize(request: NewsSummaryRequest):
    try:
        agent = NewsAgent()
        return agent.run(request.user_inp)
    except Exception as e:
        return {"error" : str(e)}