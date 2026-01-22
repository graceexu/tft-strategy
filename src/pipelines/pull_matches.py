import json
import time
from pathlib import Path

from riotwatcher import TftWatcher, ApiError

from config import RIOT_API_KEY, PLATFORM, MATCH_REGION, RAW_MATCH_DIR


def save_json(path: Path, obj: dict) -> None:
    """Write JSON to disk nicely (utf-8, pretty, stable)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def pull_matches_for_summoner(
    summoner_name: str,
    count: int = 10,
    sleep_seconds: float = 1.2,
) -> None:
    """
    Fetch recent TFT matches for a summoner and save each match JSON to data/raw/matches/.
    """
    tft = TftWatcher(RIOT_API_KEY)

    # 1) Find the player (Summoner -> PUUID)
    try:
        summ = tft.summoner.by_name(PLATFORM, summoner_name)
    except ApiError as e:
        status = getattr(e.response, "status_code", None)
        text = getattr(e.response, "text", None)
        print(f"ApiError on summoner.by_name(): status={status}")
        if text:
            print("Response body:", text)
        raise
    puuid = summ["puuid"]

    # 2) Get recent match IDs
    match_ids = tft.match.by_puuid(MATCH_REGION, puuid, count=count)

    print(f"Found {len(match_ids)} matches for {summoner_name} ({PLATFORM}, {MATCH_REGION}).")

    # 3) Download each match JSON and save to disk
    for i, match_id in enumerate(match_ids, start=1):
        out_path = RAW_MATCH_DIR / f"{match_id}.json"

        if out_path.exists():
            print(f"[{i}/{len(match_ids)}] Skipping (already exists): {match_id}")
            continue

        print(f"[{i}/{len(match_ids)}] Fetching: {match_id}")
        match = tft.match.by_id(MATCH_REGION, match_id)
        save_json(out_path, match)

        # Be nice to rate limits
        time.sleep(sleep_seconds)

    print(f"Done. Raw matches saved to: {RAW_MATCH_DIR}")


def main():
    # Simple CLI input
    summoner_name = input("Enter summoner name: ").strip()
    if not summoner_name:
        raise SystemExit("Summoner name cannot be empty.")

    try:
        pull_matches_for_summoner(summoner_name, count=10)
    except ApiError as e:
        status = getattr(e.response, "status_code", None)
        text = getattr(e.response, "text", "")
        print(f"Riot API error: status={status}")
        print(text)
        raise



if __name__ == "__main__":
    main()
