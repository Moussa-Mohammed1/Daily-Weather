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

def calculate_risk_score(df: pd.DataFrame):
    df = df.copy()

    precip_risk = (
        df["precipitation_sum"] / 30 * 70
        + df["precipitation_probability"] /100 * 30)

    wind_risk = (
        df["wind_speed_max"] / 60 * 100
    ).clip(0, 100)

    hot_risk = (
        (df["temperature_max"] - 30) / 10 * 100
    ).clip(0, 100)

    cold_risk = (
        (10 - df["temperature_min"]) / 10 * 100
    ).clip(0, 100)

    temperature_risk = pd.concat( 
        [hot_risk, cold_risk],
        axis=1
    ).max(axis=1)

    df["precipitation_risk"] = precip_risk
    df["wind_risk"] = wind_risk
    df["temperature_risk"] = temperature_risk

    df["risk_score"] = (
        df["temperature_risk"] * 0.3
        + df["precipitation_risk"] * 0.4 
        + df["wind_risk"] * 0.3
    ).round(2)

    return df 

def add_risk_level(df: pd.DataFrame):
    df = df.copy()

    df["risk_level"] = pd.cut(
        df["risk_score"],
        bins=[-float("inf"), 30, 60, 80, float("inf")],
        labels=["Low", "Medium", "High", "Critical"]
    )
    return df

def create_features(df):
    df = add_temperature_category(df)
    df = add_precipitation_category(df)
    df = add_wind_category(df)
    df = calculate_risk_score(df)
    df = add_risk_level(df)

    return df 

