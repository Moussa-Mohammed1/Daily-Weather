from extraction.cities import extract_raw_cities, save_bronze_cities
from extraction.weather_api import fetch_weather
import json
from transformation.cleaning import clean_cities, clean_weather

def main():
    cities = extract_raw_cities("data/source/ma.csv")
    print(f"Extracted {len(cities)} cities")
    save_bronze_cities(
        cities, 
        "data/bronze/cities/cities_raw.csv"
    )

    weather_data = []
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
            "data/bronze/weather/weather_raw.json",
            "w"
        ) as file:
            json.dump(
                weather_data,
                file,
                indent=4
            )
    print("Weather extracted and saved completely.")

