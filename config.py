"""Central settings. Change values here instead of hunting through the code."""
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()  # reads the .env file

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

# Currency symbol shown in the app (the simulated prices use this scale)
CURRENCY = "$"

# Rough daily costs per person, used by the budget agent
FOOD_PER_PERSON_PER_DAY = 30
LOCAL_PER_PERSON_PER_DAY = 20   # local transport, entry tickets, etc.
