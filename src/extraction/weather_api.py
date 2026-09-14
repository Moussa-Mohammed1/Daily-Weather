from dotenv import load_dotenv
import requests
import os 

load_dotenv()

def fetch_weather(lat, lng):
    url = os.getenv("API_URL")
    params = {
        "latitude": lat,
        "langitude": lng,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "weather_code",
        ],
        "forecast_days": 7,
    }
    response = requests.get(
        url,
        params=params,
        timeout=30
    )
    response.raise_for_status()
    return response.json()

fetch_weather(lat=33.6833, lng=33.6833)