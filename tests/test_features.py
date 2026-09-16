import pandas as pd

from src.transformation.features import (
    add_temperature_category,
    add_precipitation_category,
    add_wind_category,
    calculate_risk_score,
    add_risk_level,
    create_features,
)


def test_temperature_categories():
    weather = pd.DataFrame({
        "temperature_max": [-10, 5, 5.1, 15, 15.1, 30, 30.1, 35, 35.1],
    })

    result = add_temperature_category(weather)

    assert result["temperature_category"].astype(str).tolist() == [
        "Very cold",
        "Very cold",
        "Cold",
        "Cold",
        "Normal",
        "Normal",
        "Hot",
        "Hot",
        "Very Hot",
    ]


def test_precipitation_categories():
    weather = pd.DataFrame({
        "precipitation_sum": [0, 0.1, 2.5, 2.6, 10, 10.1],
    })

    result = add_precipitation_category(weather)

    assert result["precipitation_category"].astype(str).tolist() == [
        "None",
        "Light",
        "Light",
        "Moderate",
        "Moderate",
        "Heavy",
    ]


def test_wind_categories():
    weather = pd.DataFrame({
        "wind_speed_max": [20, 20.1, 40, 40.1, 60, 60.1],
    })

    result = add_wind_category(weather)

    assert result["wind_category"].astype(str).tolist() == [
        "Normal",
        "Moderate",
        "Moderate",
        "Strong",
        "Strong",
        "Extreme",
    ]


def test_calculate_risk_score():
    weather = pd.DataFrame({
        "temperature_max": [35, 20],
        "temperature_min": [0, 10],
        "precipitation_sum": [15, 0],
        "precipitation_probability": [50, 0],
        "wind_speed_max": [30, 0],
    })

    result = calculate_risk_score(weather)

    assert result["temperature_risk"].tolist() == [100.0, 0.0]
    assert result["precipitation_risk"].tolist() == [50.0, 0.0]
    assert result["wind_risk"].tolist() == [50.0, 0.0]
    assert result["risk_score"].tolist() == [65.0, 0.0]


def test_risk_levels():
    weather = pd.DataFrame({
        "risk_score": [0, 30, 30.1, 60, 60.1, 80, 80.1],
    })

    result = add_risk_level(weather)

    assert result["risk_level"].astype(str).tolist() == [
        "Low",
        "Low",
        "Medium",
        "Medium",
        "High",
        "High",
        "Critical",
    ]


def test_create_features_adds_all_features_without_mutating_input():
    weather = pd.DataFrame({
        "temperature_max": [35],
        "temperature_min": [0],
        "precipitation_sum": [15],
        "precipitation_probability": [50],
        "wind_speed_max": [30],
    })

    original = weather.copy()
    result = create_features(weather)

    expected_columns = {
        "temperature_category",
        "precipitation_category",
        "wind_category",
        "temperature_risk",
        "precipitation_risk",
        "wind_risk",
        "risk_score",
        "risk_level",
    }

    assert expected_columns.issubset(result.columns)
    pd.testing.assert_frame_equal(weather, original)