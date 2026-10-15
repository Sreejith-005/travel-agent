"""Booking step.

Real booking needs payment and partner APIs, so this SIMULATES it:
it creates a fake reference number and gives the user real links
to finish the booking on the provider's website.
"""
import uuid
from datetime import datetime


def simulate_booking(trip: dict, transport: dict, hotel: dict, budget: dict) -> dict:
    return {
        "reference": "TRV-" + uuid.uuid4().hex[:8].upper(),
        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "transport": f"{transport['mode'].title()} - {transport['provider']} "
                     f"({trip['origin']} to {trip['destination']}, {trip['start_date']})",
        "hotel": f"{hotel['name']} ({hotel['nights']} nights)",
        "total": budget["total"],
        "transport_link": transport["link"],
        "hotel_link": hotel["link"],
    }
