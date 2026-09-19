from dotenv import load_dotenv
import requests
import os 
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

def fetch_weather(lat, lng):
    url = os.getenv("API_URL")
    retry_policy = Retry(
        total=4,
        connect=4,
        read=4,
        status=4,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry_policy))
    params = {
        "latitude": lat,
        "longitude": lng,
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
    response = session.get(
        url,
        params=params,
        timeout=30
    )
    response.raise_for_status()
    return response.json()