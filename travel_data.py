"""
Travel search tools.

Most travel APIs (Amadeus, Skyscanner, Booking.com ...) need paid or
approved accounts, so this file SIMULATES search results and attaches
real search links so the user can finish the booking on the real site.

To use a real API later, replace the body of `search_transport` and
`search_hotels` but keep the same return format (a list of dicts).
"""
import math
import random
from urllib.parse import quote


def _rng(*parts: str) -> random.Random:
    """Same inputs -> same 'random' results, so the app feels consistent."""
    seed = "|".join(p.lower().strip() for p in parts)
    return random.Random(seed)


def estimate_distance_km(a: str, b: str) -> int:
    cities = sorted([a.lower().strip(), b.lower().strip()])
    return _rng(*cities).randint(250, 2200)


# ---------------------------------------------------------------- transport
MODES = {
    "flight": {"speed": 650, "overhead": 2.5, "base": 35, "per_km": 0.09,
               "providers": ["SkyJet", "BlueWing", "AirNova"]},
    "train": {"speed": 75, "overhead": 0.5, "base": 8, "per_km": 0.04,
              "providers": ["ExpressRail", "CityLine", "RapidRail"]},
    "bus": {"speed": 50, "overhead": 0.5, "base": 5, "per_km": 0.025,
            "providers": ["RoadKing", "GreenLine", "NightRider"]},
}


def _transport_link(mode: str, origin: str, destination: str, date: str) -> str:
    if mode == "flight":
        q = quote(f"Flights from {origin} to {destination} on {date}")
        return f"https://www.google.com/travel/flights?q={q}"
    return f"https://www.rome2rio.com/map/{quote(origin)}/{quote(destination)}"


def search_transport(origin, destination, travel_date, travelers, preference="any"):
    """Return a list of transport options (prices are for a ROUND TRIP)."""
    km = estimate_distance_km(origin, destination)
    rng = _rng(origin, destination, travel_date)
    options = []

    for mode, info in MODES.items():
        if preference not in ("any", mode):
            continue
        for provider in rng.sample(info["providers"], 2):
            one_way = (info["base"] + km * info["per_km"]) * rng.uniform(0.85, 1.25)
            hours = km / info["speed"] + info["overhead"]
            dep_hour = rng.choice([6, 8, 10, 13, 16, 20])
            options.append({
                "id": len(options) + 1,
                "mode": mode,
                "provider": provider,
                "departure": f"{dep_hour:02d}:00",
                "duration_hours": round(hours, 1),
                "price_per_person_one_way": round(one_way),
                "total_price": round(one_way * 2 * travelers),
                "link": _transport_link(mode, origin, destination, travel_date),
            })

    if not options and preference != "any":      # unknown preference -> show all
        return search_transport(origin, destination, travel_date, travelers, "any")
    return options


# ------------------------------------------------------------------- hotels
HOTEL_NAMES = ["Grand Palace", "City Comfort Inn", "Lakeview Residency",
               "The Urban Nest", "Royal Orchid", "Budget Stay Lodge",
               "Skyline Suites", "Heritage Haveli"]
AREAS = ["City Centre", "Old Town", "Near Station", "Riverside", "Market Area"]


def search_hotels(destination, check_in, check_out, nights, travelers, preference="any"):
    """Return a list of hotels. Rooms are assumed to fit 2 people each."""
    rng = _rng(destination, check_in)
    rooms = math.ceil(travelers / 2)
    options = []

    for name in rng.sample(HOTEL_NAMES, 5):
        stars = rng.choice([2, 3, 3, 4, 4, 5])
        per_night = round(stars * 18 * rng.uniform(0.8, 1.3) + 10)
        q = quote(destination)
        link = (f"https://www.booking.com/searchresults.html?ss={q}"
                f"&checkin={check_in}&checkout={check_out}"
                f"&group_adults={travelers}&no_rooms={rooms}")
        options.append({
            "id": len(options) + 1,
            "name": f"{name}",
            "stars": stars,
            "rating": round(rng.uniform(3.5, 4.9), 1),
            "area": rng.choice(AREAS),
            "price_per_night": per_night,
            "rooms": rooms,
            "nights": nights,
            "total_price": per_night * nights * rooms,
            "link": link,
        })

    if preference == "budget":
        filtered = [h for h in options if h["stars"] <= 3]
    elif preference == "luxury":
        filtered = [h for h in options if h["stars"] >= 4]
    else:
        filtered = options
    return filtered or options
