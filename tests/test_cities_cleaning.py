from src.transformation.cleaning import clean_cities, clean_weather
import pandas as pd 
def test_cities_cleaning():
    cities = pd.read_csv("data/bronze/cities/cities_raw.csv")

    cleaned = clean_cities(cities)
    assert cleaned is not None
    assert "latitude" in cleaned
    assert "longitude" in cleaned