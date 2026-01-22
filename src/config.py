import os
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / ".env")

# secrets + settings
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
PLATFORM = os.getenv("PLATFORM", "na1")           
MATCH_REGION = os.getenv("MATCH_REGION", "americas")  

if not RIOT_API_KEY:
    raise RuntimeError("RIOT_API_KEY is missing. Put it in your .env file.")

# paths
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
RAW_MATCH_DIR = DATA_DIR / "raw" / "matches"
RAW_MATCH_DIR.mkdir(parents=True, exist_ok=True)
