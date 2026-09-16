import pandas as pd
from sqlalchemy import text
from src.database.connection import engine

GOLD_PATH = "data/gold/weather_features.csv"

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
                        --- inserting into the weather_forecasts 
                    """)
                )
            