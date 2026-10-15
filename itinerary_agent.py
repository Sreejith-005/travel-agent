"""Agent 4 - Itinerary Writer: creates a day-by-day plan."""
from llm import get_llm


def itinerary_agent(state: dict) -> dict:
    trip = state["trip"]
    t = state["transport_pick"]
    h = state["hotel_pick"]

    prompt = f"""Create a friendly day-by-day travel itinerary in Markdown.

Trip: {trip['origin']} to {trip['destination']}, {trip['num_days']} days,
starting {trip['start_date']}, {trip['num_travelers']} traveller(s).
Interests: {', '.join(trip['interests']) or 'general sightseeing'}.
Transport: {t['mode']} with {t['provider']}, departing {t['departure']}, about {t['duration_hours']} hours.
Hotel: {h['name']} ({h['stars']} stars) in {h['area']}.

Rules:
- Use headings like "### Day 1 - <title>" with Morning / Afternoon / Evening bullets.
- Day 1 includes travel and hotel check-in; the last day includes check-out and the return trip.
- Mention real, well-known places and local food in {trip['destination']}.
- Keep each day short (about 4-6 lines)."""

    return {"itinerary": get_llm(0.5).invoke(prompt).content}
