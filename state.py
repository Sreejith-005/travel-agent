"""The shared 'notebook' that every agent reads from and writes to."""
from typing import TypedDict


class TravelState(TypedDict, total=False):
    user_request: str        # what the user typed
    trip: dict               # structured trip details (from the planner agent)
    transport_options: list  # all transport options found
    transport_pick: dict     # the best transport option
    hotel_options: list      # all hotels found
    hotel_pick: dict         # the best hotel
    itinerary: str           # day-by-day plan (markdown text)
    budget: dict             # cost breakdown
    error: str               # set when something is missing/wrong
