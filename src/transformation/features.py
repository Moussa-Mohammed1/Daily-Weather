import pandas as pd 

def add_temperature_category(df: pd.DataFrame):
    df = df.copy()

    df["temperature_category"] = pd.cut(
        df["temperature_max"],
        bins=[-float("inf"), 5, 15, 30, 35, float("inf")],
        labels=[
            "Very cold",
            "Cold",
            "Normal", 
            "Hot",
            "Very Hot"
        ]
    )
    return df

def add_precipitation_category(df: pd.DataFrame):
    df = df.copy()
    df["precipitation_category"] = pd.cut(
        df["precipitation_sum"],
        bins=[-float("inf"), 0, 2.5, 10, float("inf")],
        labels=[
            "None", 
            "Light",
            "Moderate",
            "Heavy"
        ]
    )

    return df

def add_wind_category(df):
    df = df.copy()

    df["wind_category"] = pd.cut(
        df["wind_speed_max"],
        bins=[-float("inf"), 20, 40, 60, float("inf")],
        labels=[
            "Normal",
            "Moderate",
            "Strong",
            "Extreme"
        ]
    )

    return df

