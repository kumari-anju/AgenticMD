import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

def get_llm():
    """
    Initialize and return the Gemini LLM.
    """
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0
    )

