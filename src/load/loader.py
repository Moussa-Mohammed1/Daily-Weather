from pathlib import Path

import pandas as pd
from sqlalchemy import text
from src.load.connection import engine

GOLD_PATH = Path(__file__).resolve().parents[2] / "data" / "gold" / "weather_features.csv"

def load_data():
    df = pd.read_csv(GOLD_PATH)

    with engine.begin() as connection:
        for _, row in df.drop_duplicates("city").iterrows():
            connection.execute(
                text("""
                    INSERT INTO cities(name, latitude, longitude)
                    VALUES (:name, :latitude, :longitude)
                    ON CONFLICT (name) DO NOTHING
                """), 
                {
                    "name": row["city"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"]
                }
            )
            result = connection.execute(text("""
                            SELECT id, name 
                            FROM cities
                        """))

            city_map = { row.name: row.id for row in result}
            for _, row in df.iterrows():
                connection.execute(
                text("""
                    INSERT INTO weather_forecasts (
                        city_id,
                        forecast_date,
                        temperature_max,
                        temperature_min,
                        precipitation_sum,
                        precipitation_probability,
                        wind_speed_max,
                        wind_gust_max,
                        weather_code,
                        temperature_category,
                        precipitation_category,
                        wind_category,
                        temperature_risk,
                        precipitation_risk,
                        wind_risk,
                        risk_score,
                        risk_level
                    )
                    VALUES (
                        :city_id,
                        :forecast_date,
                        :temperature_max,
                        :temperature_min,
                        :precipitation_sum,
                        :precipitation_probability,
                        :wind_speed_max,
                        :wind_gust_max,
                        :weather_code,
                        :temperature_category,
                        :precipitation_category,
                        :wind_category,
                        :temperature_risk,
                        :precipitation_risk,
                        :wind_risk,
                        :risk_score,
                        :risk_level
                    )
                    ON CONFLICT (city_id, forecast_date)
                    DO UPDATE SET
                        temperature_max = EXCLUDED.temperature_max,
                        temperature_min = EXCLUDED.temperature_min,
                        precipitation_sum = EXCLUDED.precipitation_sum,
                        precipitation_probability = EXCLUDED.precipitation_probability,
                        wind_speed_max = EXCLUDED.wind_speed_max,
                        wind_gust_max = EXCLUDED.wind_gust_max,
                        weather_code = EXCLUDED.weather_code,
                        temperature_category = EXCLUDED.temperature_category,
                        precipitation_category = EXCLUDED.precipitation_category,
                        wind_category = EXCLUDED.wind_category,
                        temperature_risk = EXCLUDED.temperature_risk,
                        precipitation_risk = EXCLUDED.precipitation_risk,
                        wind_risk = EXCLUDED.wind_risk,
                        risk_score = EXCLUDED.risk_score,
                        risk_level = EXCLUDED.risk_level
                """),
                {
                    "city_id": city_map[row["city"]],
                    "forecast_date": row["date"],
                    "temperature_max": row["temperature_max"],
                    "temperature_min": row["temperature_min"],
                    "precipitation_sum": row["precipitation_sum"],
                    "precipitation_probability": row["precipitation_probability"],
                    "wind_speed_max": row["wind_speed_max"],
                    "wind_gust_max": row["wind_gust_max"],
                    "weather_code": row["weather_code"],
                    "temperature_category": row["temperature_category"],
                    "precipitation_category": row["precipitation_category"],
                    "wind_category": row["wind_category"],
                    "temperature_risk": row["temperature_risk"],
                    "precipitation_risk": row["precipitation_risk"],
                    "wind_risk": row["wind_risk"],
                    "risk_score": row["risk_score"],
                    "risk_level": row["risk_level"],
                }
            )

                print("Gold data loaded successfully!")

if __name__ == "__main__":
    load_data()