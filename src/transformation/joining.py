import pandas as pd

def join_cities_weather(
        cities: pd.DataFrame,
        weather: pd.DataFrame
)-> pd.DataFrame:
    merged = weather.merge(
        cities,
        on="city",
        how="left"
    )
    return merged

def save_weather_cities_join(joined_weather_cities: pd.DataFrame, output_path: str):
    joined_weather_cities.to_csv(output_path, index=False)