"""Agent 1 - Travel Planner: turns the user's sentence into structured trip details."""
from datetime import date, timedelta
from typing import Optional
from pydantic import BaseModel, Field
from llm import get_llm


class TripDetails(BaseModel):
    origin: str = Field(default="", description="City the traveller starts from, or empty if not stated")
    destination: str = Field(default="", description="City/place the traveller wants to visit, or empty")
    start_date: str = Field(description="Departure date as YYYY-MM-DD")
    num_days: int = Field(default=3, description="Total number of days of the trip")
    num_travelers: int = Field(default=1, description="Number of people travelling")
    budget: Optional[float] = Field(default=None, description="Total budget as a number, if stated")
    transport_preference: str = Field(default="any", description="One of: flight, train, bus, any")
    hotel_preference: str = Field(default="any", description="One of: budget, mid-range, luxury, any")
    interests: list[str] = Field(default_factory=list, description="e.g. food, beaches, history, adventure")


def planner_agent(state: dict) -> dict:
    today = date.today()
    prompt = f"""Today's date is {today.isoformat()} ({today.strftime('%A')}).
Extract the trip details from the request below.
- Work out exact dates for phrases like "next Friday" or "in December".
- If origin or destination is not mentioned, leave it empty. Do NOT guess.
- If no date is given, use a date one week from today.

Request: {state['user_request']}"""

    trip = get_llm(0).with_structured_output(TripDetails).invoke(prompt).model_dump()

    # Clean up values
    trip["num_days"] = max(1, trip["num_days"])
    trip["num_travelers"] = max(1, trip["num_travelers"])
    start = date.fromisoformat(trip["start_date"])
    trip["end_date"] = (start + timedelta(days=trip["num_days"] - 1)).isoformat()
    trip["nights"] = max(1, trip["num_days"] - 1)

    if not trip["origin"] or not trip["destination"]:
        return {"trip": trip,
                "error": "I couldn't find both a starting city and a destination. "
                         "Please mention them, e.g. 'from Chennai to Goa'."}
    return {"trip": trip}
