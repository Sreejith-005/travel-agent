"""Agent 3 - Hotel Search: finds hotels and picks the best one."""
from tools.travel_data import search_hotels
from agents.common import pick_best_option


def hotel_agent(state: dict) -> dict:
    trip = state["trip"]
    options = search_hotels(
        trip["destination"], trip["start_date"], trip["end_date"],
        trip["nights"], trip["num_travelers"], trip["hotel_preference"],
    )
    best = pick_best_option(options, "hotel", trip)
    return {"hotel_options": options, "hotel_pick": best}
