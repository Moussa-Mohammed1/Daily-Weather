import pandas as pd 
from src.transformation.joining import join_cities_weather
from src.transformation.cleaning import clean_cities, clean_weather
def test_join_weather_cities():
    cities = pd.read_csv("data/bronze/cities/cities_raw.csv")
    weather = pd.read_json("data/bronze/weather/weather_raw.json")

    cleaned_cities = clean_cities(cities)
    cleaned_weather = clean_weather(weather)

    assert {"latitude", "longitude"}.issubset(cleaned_cities.columns)
    assert isinstance(cleaned_cities, pd.DataFrame)
    assert not cleaned_cities.empty
    assert isinstance(cleaned_weather, pd.DataFrame)
    assert not cleaned_weather.empty

    joined = join_cities_weather(cleaned_cities, cleaned_weather)
    assert isinstance(joined, pd.DataFrame)
    assert not joined.empty
    assert "city" in joined


def test_clean_cities_removes_invalid_rows():
    cities = pd.DataFrame({
        "city": [" Casablanca ", "Rabat", "Rabat", None],
        "lat": ["33.5", 34.0, 34.0, 10],
        "lng": ["-7.6", -6.8, -6.8, 200],
    })

    cleaned = clean_cities(cities)

    assert list(cleaned["city"]) == ["Casablanca", "Rabat"]
    assert cleaned["latitude"].dtype.kind in "fi"