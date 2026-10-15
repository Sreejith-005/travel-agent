"""Creates the Groq language model used by all agents."""
from langchain_groq import ChatGroq
import config


def get_llm(temperature: float = 0.2) -> ChatGroq:
    return ChatGroq(
        model=config.MODEL_NAME,
        temperature=temperature,
        api_key=config.GROQ_API_KEY,
    )
