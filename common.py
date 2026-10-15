"""Helper shared by the transport and hotel agents: ask the LLM to pick the best option."""
import json
from pydantic import BaseModel, Field
from llm import get_llm


class Recommendation(BaseModel):
    best_id: int = Field(description="The 'id' of the best option")
    reason: str = Field(description="One or two sentences explaining why")


def pick_best_option(options: list, kind: str, trip: dict) -> dict:
    """Returns the chosen option dict with an extra 'reason' field."""
    # Don't send links to the LLM, it doesn't need them
    slim = [{k: v for k, v in o.items() if k != "link"} for o in options]

    prompt = f"""You are a travel expert choosing the best {kind} option.

Trip details: {json.dumps(trip)}

Options:
{json.dumps(slim, indent=2)}

Pick the best overall value. Consider the traveller's budget (if given),
preferences, travel time and rating. Answer with the option id and a short reason."""

    try:
        llm = get_llm(0).with_structured_output(Recommendation)
        rec = llm.invoke(prompt)
        chosen = next((o for o in options if o["id"] == rec.best_id), None)
        if chosen:
            return {**chosen, "reason": rec.reason}
    except Exception:
        pass  # fall through to the simple fallback below

    cheapest = min(options, key=lambda o: o["total_price"])
    return {**cheapest, "reason": "Cheapest option (automatic fallback)."}
