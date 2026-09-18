import json
from pathlib import Path

from src.extraction.cities import extract_raw_cities, save_bronze_cities
from src.extraction.weather_api import fetch_weather


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BRONZE_CITIES_PATH = PROJECT_ROOT / "data" / "bronze" / "cities" / "cities_raw.csv"
BRONZE_WEATHER_PATH = PROJECT_ROOT / "data" / "bronze" / "weather" / "weather_raw.json"
SOURCE_CITIES_PATH = PROJECT_ROOT / "data" / "source" / "ma.csv"

def main():
    cities = extract_raw_cities(SOURCE_CITIES_PATH)
    print(f"Extracted {len(cities)} cities")
    save_bronze_cities(
        cities, 
        BRONZE_CITIES_PATH
    )

    weather_data = []
    BRONZE_WEATHER_PATH.parent.mkdir(parents=True, exist_ok=True)
    for _, city in cities.iterrows():
        print(f"Fetching weather for {city['city']}")

        weather = fetch_weather(city['lat'], city['lng'])
        weather_data.append({
            "city": city['city'],
            "latitude": city['lat'],
            "longitude": city['lng'],
            "weather": weather
        })

        with open(
            BRONZE_WEATHER_PATH,
            "w"
        ) as file:
            json.dump(
                weather_data,
                file,
                indent=4
            )
    print("Weather extracted and saved completely.")

