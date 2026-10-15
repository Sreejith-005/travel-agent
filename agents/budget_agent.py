"""Agent 5 - Budget Calculator: adds up all costs. Plain Python, no LLM needed."""
import config


def budget_agent(state: dict) -> dict:
    trip = state["trip"]
    days, people = trip["num_days"], trip["num_travelers"]

    breakdown = {
        "Transport (round trip)": state["transport_pick"]["total_price"],
        "Hotel": state["hotel_pick"]["total_price"],
        "Food": config.FOOD_PER_PERSON_PER_DAY * days * people,
        "Local travel & activities": config.LOCAL_PER_PERSON_PER_DAY * days * people,
    }
    total = sum(breakdown.values())

    user_budget = trip.get("budget")
    within = None if not user_budget else total <= user_budget
    difference = None if not user_budget else round(user_budget - total)

    # How much could the traveller save by choosing the cheapest options?
    cheapest_transport = min(o["total_price"] for o in state["transport_options"])
    cheapest_hotel = min(o["total_price"] for o in state["hotel_options"])
    savings = (breakdown["Transport (round trip)"] - cheapest_transport) + \
              (breakdown["Hotel"] - cheapest_hotel)

    tip = ""
    if savings > 0:
        tip = (f"Choosing the cheapest transport and hotel would save about "
               f"{config.CURRENCY}{savings:,.0f}.")

    return {"budget": {
        "breakdown": breakdown,
        "total": total,
        "per_person": round(total / people),
        "user_budget": user_budget,
        "within_budget": within,
        "difference": difference,
        "tip": tip,
    }}
