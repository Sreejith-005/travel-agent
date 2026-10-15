"""Connects all the agents into one LangGraph workflow.

    planner -> transport -> hotel -> itinerary -> budget -> END
       |
       +-- (if origin/destination missing) -> END
"""
from langgraph.graph import StateGraph, END
from state import TravelState
from agents.planner_agent import planner_agent
from agents.transport_agent import transport_agent
from agents.hotel_agent import hotel_agent
from agents.itinerary_agent import itinerary_agent
from agents.budget_agent import budget_agent


def route_after_planner(state: dict) -> str:
    """Stop early if the planner could not understand the request."""
    return "stop" if state.get("error") else "continue"


def build_graph():
    graph = StateGraph(TravelState)

    # Node names must differ from the state keys, so we add "_agent"
    graph.add_node("planner_agent", planner_agent)
    graph.add_node("transport_agent", transport_agent)
    graph.add_node("hotel_agent", hotel_agent)
    graph.add_node("itinerary_agent", itinerary_agent)
    graph.add_node("budget_agent", budget_agent)

    graph.set_entry_point("planner_agent")
    graph.add_conditional_edges(
        "planner_agent", route_after_planner,
        {"continue": "transport_agent", "stop": END},
    )
    graph.add_edge("transport_agent", "hotel_agent")
    graph.add_edge("hotel_agent", "itinerary_agent")
    graph.add_edge("itinerary_agent", "budget_agent")
    graph.add_edge("budget_agent", END)

    return graph.compile()
