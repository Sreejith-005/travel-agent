"""Streamlit web interface. Run with:  streamlit run app.py"""
import pandas as pd
import streamlit as st

import config
from graph import build_graph
from booking import simulate_booking

st.set_page_config(page_title="AI Travel Agent", page_icon="✈️", layout="wide")

AGENT_LABELS = {
    "planner_agent": "Planner agent understood your request",
    "transport_agent": "Transport agent searched flights, trains and buses",
    "hotel_agent": "Hotel agent searched hotels",
    "itinerary_agent": "Itinerary agent wrote your day-by-day plan",
    "budget_agent": "Budget agent calculated the total cost",
}
EXAMPLES = [
    "Plan a 4-day trip from Chennai to Goa for 2 people next month, budget 1500, I love beaches and seafood",
    "Weekend trip from Delhi to Jaipur by train for 3 friends, mid-range hotel, interested in history",
    "5 days from Mumbai to Manali, 1 person, budget hotel, adventure activities",
]


def money(x) -> str:
    return f"{config.CURRENCY}{x:,.0f}"


def run_planning(text: str) -> dict:
    """Runs the LangGraph workflow and shows live progress."""
    graph = build_graph()
    result = {}
    with st.status("Your AI agents are working...", expanded=True) as status:
        for step in graph.stream({"user_request": text}):
            for node_name, update in step.items():
                result.update(update)
                st.write(f"✅ {AGENT_LABELS.get(node_name, node_name)}")
        status.update(label="Planning complete!", state="complete", expanded=False)
    return result


def options_table(options: list, columns: list):
    """Shows a list of dicts as a table with a clickable link column."""
    df = pd.DataFrame(options)[columns + ["link"]]
    st.dataframe(
        df, hide_index=True, width='stretch',
        column_config={"link": st.column_config.LinkColumn("Book / compare", display_text="Open")},
    )


def show_results(r: dict):
    trip, t, h, b = r["trip"], r["transport_pick"], r["hotel_pick"], r["budget"]

    st.subheader(f"🧭 {trip['origin']} → {trip['destination']}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Dates", f"{trip['start_date']}")
    c2.metric("Duration", f"{trip['num_days']} days")
    c3.metric("Travellers", trip["num_travelers"])
    c4.metric("Estimated total", money(b["total"]))

    # Budget verdict
    if b["within_budget"] is True:
        st.success(f"Within your budget of {money(b['user_budget'])} "
                   f"({money(b['difference'])} to spare).")
    elif b["within_budget"] is False:
        st.warning(f"Over your budget of {money(b['user_budget'])} "
                   f"by {money(-b['difference'])}. {b['tip']}")

    tab1, tab2, tab3, tab4 = st.tabs(["⭐ Best picks", "🚆 Transport & Hotels", "🗓️ Itinerary", "💰 Budget"])

    with tab1:
        left, right = st.columns(2)
        with left:
            st.markdown("#### 🚆 Best transport")
            st.markdown(f"**{t['mode'].title()} - {t['provider']}**  \n"
                        f"Departs {t['departure']} · {t['duration_hours']} h  \n"
                        f"Round trip total: **{money(t['total_price'])}**")
            st.info(t["reason"])
        with right:
            st.markdown("#### 🏨 Best hotel")
            st.markdown(f"**{h['name']}** ({'⭐' * h['stars']})  \n"
                        f"{h['area']} · rating {h['rating']}  \n"
                        f"{money(h['price_per_night'])}/night · total **{money(h['total_price'])}**")
            st.info(h["reason"])

    with tab2:
        st.markdown("#### Transport options (round-trip prices)")
        options_table(r["transport_options"],
                      ["mode", "provider", "departure", "duration_hours", "total_price"])
        st.markdown("#### Hotel options")
        options_table(r["hotel_options"],
                      ["name", "stars", "rating", "area", "price_per_night", "total_price"])
        st.caption("Prices are simulated estimates. Use the links to see live prices.")

    with tab3:
        st.markdown(r["itinerary"])

    with tab4:
        df = pd.DataFrame({"Item": list(b["breakdown"].keys()),
                           "Cost": [money(v) for v in b["breakdown"].values()]})
        st.table(df.set_index("Item"))
        st.markdown(f"### Total: {money(b['total'])}  \n"
                    f"Per person: {money(b['per_person'])}")
        if b["tip"]:
            st.caption(b["tip"])

    # ---------------- Confirmation before booking ----------------
    st.divider()
    st.subheader("✅ Confirm your booking")
    st.write(f"You are about to book **{t['mode']} ({t['provider']})** and "
             f"**{h['name']}** for a total of **{money(b['total'])}**.")
    agree = st.checkbox("Yes, these details are correct and I want to book.")
    if st.button("Confirm & Book", type="primary", disabled=not agree):
        st.session_state.booking = simulate_booking(trip, t, h, b)

    booking = st.session_state.get("booking")
    if booking:
        st.success(f"Booking recorded! Reference: **{booking['reference']}**")
        st.write(f"- Transport: {booking['transport']}\n"
                 f"- Hotel: {booking['hotel']}\n"
                 f"- Total: {money(booking['total'])}\n"
                 f"- Time: {booking['booked_at']}")
        st.info("This is a simulated booking, so no payment was made. "
                "Use the buttons below to complete your real reservation.")
        b1, b2 = st.columns(2)
        b1.link_button("Book transport", booking["transport_link"])
        b2.link_button("Book hotel", booking["hotel_link"])


# ============================== Page layout ==============================
st.title("✈️ AI Travel Agent")
st.caption("Describe your trip in plain English. Five AI agents plan it for you.")

if not config.GROQ_API_KEY:
    st.error("GROQ_API_KEY not found. Copy `.env.example` to `.env`, add your key, and restart.")
    st.stop()

if "request_text" not in st.session_state:
    st.session_state.request_text = ""


def use_example(text: str):
    st.session_state.request_text = text


with st.sidebar:
    st.header("💡 Try an example")
    for ex in EXAMPLES:
        st.button(ex, on_click=use_example, args=(ex,), use_container_width=True)

request = st.text_area("Where do you want to go?", key="request_text", height=100,
                       placeholder="e.g. 3-day trip from Bangalore to Kochi for 2 people, budget 1000")

if st.button("🔍 Plan my trip", type="primary"):
    if not request.strip():
        st.warning("Please describe your trip first.")
    else:
        st.session_state.booking = None
        try:
            st.session_state.result = run_planning(request)
        except Exception as e:
            st.session_state.result = None
            st.error(f"Something went wrong: {e}")

result = st.session_state.get("result")
if result:
    if result.get("error"):
        st.warning(result["error"])
    else:
        show_results(result)
