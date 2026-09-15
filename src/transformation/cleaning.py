import pandas as pd
import json
def clean_cities(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned = cleaned[
        ["city", "lat", "lng"]
    ]
    cleaned = cleaned.rename(
        columns={
            "lat": "latitude",
            "lng": "longitude"
        }
    )
    cleaned["city"] = (
        cleaned["city"].astype("string").str.strip()
    )
    cleaned["latitude"] = pd.to_numeric(
        cleaned["latitude"],
        errors="coerce"
        )
    cleaned["longitude"] = pd.to_numeric(
        cleaned["longitude"],
        errors="coerce"
        )
    cleaned = cleaned.dropna(
        subset=["city", "latitude", "longitude"]
    )
    cleaned = cleaned.drop_duplicates(subset=["city"])
    cleaned = cleaned[
        cleaned["latitude"].between(-90, 90) & cleaned["longitude"].between(-180, 180)
    ]

    return cleaned

def clean_weather(weather_data: list) -> pd.DataFrame:
    
    rows = []

    for city_data in weather_data:

        city = city_data["city"]
        daily = city_data["weather"]["daily"]

        for i in range(len(daily["time"])):

            rows.append({
                "city": city,
                "date": daily["time"][i],
                "temperature_max": daily["temperature_2m_max"][i],
                "temperature_min": daily["temperature_2m_min"][i],
                "precipitation_sum": daily["precipitation_sum"][i],
                "precipitation_probability": daily["precipitation_probability_max"][i],
                "wind_speed_max": daily["wind_speed_10m_max"][i],
                "wind_gust_max": daily["wind_gusts_10m_max"][i],
                "weather_code": daily["weather_code"][i],
            })

    df = pd.DataFrame(rows)

    df["date"] = pd.to_datetime(df["date"])

    numeric_columns = [
        "temperature_max",
        "temperature_min",
        "precipitation_sum",
        "precipitation_probability",
        "wind_speed_max",
        "wind_gust_max",
        "weather_code",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.dropna(
        subset=["city", "date"]
    )

    df = df.drop_duplicates(
        subset=["city", "date"]
    )

    return df