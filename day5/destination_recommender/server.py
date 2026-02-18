from fastapi import FastAPI
from typing import Optional, List, Literal
from pydantic import BaseModel, Field

app = FastAPI("Destination recommender", description = "A simple API for recommending destination based on the user's intent")

## schema for user input

# ---- predefined enums / controlled vocab ----

GroupType = Literal["solo", "friends", "family", "colleagues", "partner"]

DistancePreference = Literal[
    "local",          # same city / nearby
    "short_escape",   # few hours to 1 day
    "getaway",        # 2–4 days
    "long_trip"       # 5+ days
]

BudgetLevel = Literal[
    "budget_friendly",
    "moderate",
    "comfortable",
    "flexible"
]

IntentType = Literal[
    "mental_reset",
    "casual_hangout",
    "social_meetup",
    "family_time",
    "team_outing",
    "focused_work",
    "celebration",
    "exploration"
]

VibeType = Literal[
    "quiet",
    "social",
    "nature",
    "cozy",
    "productive",
    "adventurous",
    "aesthetic"
]

TimeAvailability = Literal[
    "few_hours",
    "half_day",
    "full_day",
    "multiple_days",
    "flexible"
]

# ---- main request schema ----

class DestinationRecommendationRequest(BaseModel):
    intent: IntentType = Field(
        ...,
        description="Primary purpose of going out or traveling",
        example="mental_reset"
    )

    group_type: GroupType = Field(
        ...,
        description="Who the user is going with",
        example="friends"
    )

    people_count: Optional[int] = Field(
        None,
        ge=1,
        description="Number of people in the group (auto-1 for solo)",
        example=3
    )

    distance_preference: DistancePreference = Field(
        ...,
        description="How far the user is willing to go",
        example="local"
    )

    time_available: Optional[TimeAvailability] = Field(
        None,
        description="Amount of time available for the outing or trip",
        example="few_hours"
    )

    budget_level: BudgetLevel = Field(
        ...,
        description="User's budget comfort level",
        example="moderate"
    )

    vibe: Optional[List[VibeType]] = Field(
        None,
        description="Preferred atmosphere or vibe",
        example=["quiet", "nature"]
    )

    additional_notes: Optional[str] = Field(
        None,
        description="Any extra preferences or constraints from the user",
        example="Not too crowded, easy commute"
    )

@app.get("/")
def read_root():
    return{"message": "Welcome to Destination recommender API"}

