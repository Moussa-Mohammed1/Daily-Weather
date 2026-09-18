import json
from pathlib import Path

import pandas as pd
from src.transformation.cleaning import (
    clean_cities,
    clean_weather,
    save_cities_clean,
    save_weather_clean,
)
from src.transformation.features import create_features
from src.transformation.joining import (
    join_cities_weather,
    save_weather_cities_join,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BRONZE_CITIES_PATH = PROJECT_ROOT / "data" / "bronze" / "cities" / "cities_raw.csv"
BRONZE_WEATHER_PATH = PROJECT_ROOT / "data" / "bronze" / "weather" / "weather_raw.json"
CITIES_CLEAN_PATH = PROJECT_ROOT / "data" / "silver" / "cities_clean.csv"
WEATHER_CLEAN_PATH = PROJECT_ROOT / "data" / "silver" / "weather_clean.csv"
JOINED_PATH = PROJECT_ROOT / "data" / "silver" / "weather_cities_joined.csv"
GOLD_PATH = PROJECT_ROOT / "data" / "gold" / "weather_features.csv"


def clean_and_join():
    cities = clean_cities(pd.read_csv(BRONZE_CITIES_PATH))
    with BRONZE_WEATHER_PATH.open() as file:
        weather = clean_weather(json.load(file))

    CITIES_CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_cities_clean(cities, CITIES_CLEAN_PATH)
    save_weather_clean(weather, WEATHER_CLEAN_PATH)

    joined = join_cities_weather(cities, weather)
    save_weather_cities_join(joined, JOINED_PATH)
    print(f"Silver datasets created: {CITIES_CLEAN_PATH.parent}")
    print(f"Rows joined: {len(joined)}")


def create_features_file():
    weather = pd.read_csv(JOINED_PATH)
    gold = create_features(weather)

    GOLD_PATH.parent.mkdir(parents=True, exist_ok=True)
    gold.to_csv(GOLD_PATH, index=False)
    print(f"Gold dataset created: {GOLD_PATH}")
    print(f"Rows: {len(gold)}")


def main():
    clean_and_join()
    create_features_file()


if __name__ == "__main__":
    main()