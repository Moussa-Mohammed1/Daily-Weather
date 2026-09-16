import pandas as pd
from src.transformation.features import create_features

INPUT_PATH = "data/silver/weather_cities_joined.csv"
OUTPUT_PATH = "data/gold/weather_features.csv"


def main():
    weather = pd.read_csv(INPUT_PATH)
    gold = create_features(weather)

    gold.to_csv(OUTPUT_PATH, index=False)
    print(f"Gold dataset created: {OUTPUT_PATH}")
    print(f"Rows: {len(gold)}")


if __name__ == "__main__":
    main()