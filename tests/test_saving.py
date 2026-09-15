import pandas as pd

from src.transformation.cleaning import (
    save_cities_clean,
    save_weather_clean,
)
from src.transformation.joining import save_weather_cities_join


def test_save_cities_clean(tmp_path):
    cities = pd.DataFrame({
        "city": ["Casablanca"],
        "latitude": [33.5992],
        "longitude": [-7.62],
    })

    output_path = tmp_path / "cities_clean.csv"
    save_cities_clean(cities, output_path)

    assert output_path.exists()
    saved = pd.read_csv(output_path)
    pd.testing.assert_frame_equal(saved, cities)


def test_save_weather_clean(tmp_path):
    weather = pd.DataFrame({
        "city": ["Casablanca"],
        "date": ["2026-01-01"],
        "temperature_max": [22.5],
    })

    output_path = tmp_path / "weather_clean.csv"
    save_weather_clean(weather, output_path)

    assert output_path.exists()
    saved = pd.read_csv(output_path)
    assert saved.to_dict("records") == weather.to_dict("records")


def test_save_weather_cities_join(tmp_path):
    joined = pd.DataFrame({
        "city": ["Casablanca"],
        "date": ["2026-01-01"],
        "latitude": [33.5992],
        "longitude": [-7.62],
    })

    output_path = tmp_path / "weather_cities_join.csv"
    save_weather_cities_join(joined, output_path)

    assert output_path.exists()
    saved = pd.read_csv(output_path)
    pd.testing.assert_frame_equal(saved, joined)