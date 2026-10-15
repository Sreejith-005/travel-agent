# AI Travel Auto-Booking Agent

Describe a trip in plain English; five agents (built with LangGraph, LangChain and Groq)
plan it, and a Streamlit app shows the results and asks for confirmation before booking.

## Project structure

```
travel_agent/
├── app.py                  # Streamlit web interface
├── graph.py                # LangGraph workflow connecting the agents
├── state.py                # Shared state passed between agents
├── config.py               # Settings (API key, model, currency, daily costs)
├── llm.py                  # Groq LLM setup
├── booking.py              # Simulated booking + real booking links
├── agents/
│   ├── planner_agent.py    # Understands the request -> structured trip details
│   ├── transport_agent.py  # Finds flights/trains/buses, picks the best
│   ├── hotel_agent.py      # Finds hotels, picks the best
│   ├── itinerary_agent.py  # Writes the day-by-day plan
│   ├── budget_agent.py     # Calculates the total cost (plain Python)
│   └── common.py           # Shared "pick the best option" helper
└── tools/
    └── travel_data.py      # Simulated search results + real search links
```

## Setup

1. Install Python 3.10 or newer.
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```
3. Install packages:
   ```
   pip install -r requirements.txt
   ```
4. Get a free API key at https://console.groq.com/keys
5. Copy `.env.example` to `.env` and paste your key:
   ```
   GROQ_API_KEY=gsk_...
   ```
6. Run the app:
   ```
   streamlit run app.py
   ```

## How it works

`planner -> transport -> hotel -> itinerary -> budget`

If the planner cannot find both a starting city and a destination, the graph stops
and the app asks you to add them.

## Using real travel APIs

`tools/travel_data.py` currently simulates prices and adds real search links
(Google Flights, Rome2rio, Booking.com). To use a real API (for example Amadeus),
replace the bodies of `search_transport()` and `search_hotels()` and return
the same list-of-dicts format. Nothing else needs to change.
`booking.py` is where a real payment/booking call would go.
