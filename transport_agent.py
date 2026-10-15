"""Agent 2 - Transport Search: finds flights/trains/buses and picks the best one."""
from tools.travel_data import search_transport
from agents.common import pick_best_option


def transport_agent(state: dict) -> dict:
    trip = state["trip"]
    options = search_transport(
        trip["origin"], trip["destination"], trip["start_date"],
        trip["num_travelers"], trip["transport_preference"],
    )
    best = pick_best_option(options, "transport", trip)
    return {"transport_options": options, "transport_pick": best}
