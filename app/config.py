# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

settings = Settings()
