# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
PLATFORM = os.getenv("PLATFORM", "na1")
MATCH_REGION = os.getenv("MATCH_REGION", "americas")

if not RIOT_API_KEY:
    raise RuntimeError("RIOT_API_KEY is not set. Put it in your .env file.")