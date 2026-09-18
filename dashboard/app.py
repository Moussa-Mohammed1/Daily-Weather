import sys
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


st.set_page_config(
    page_title="Morocco Weather Risk",
    layout="wide"
)


@st.cache_data
def load_data():
    return pd.read_csv(
        PROJECT_ROOT / "data" / "gold" / "weather_features.csv"
    )


# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.DataFrame()

try:
    df = load_data()

except pd.errors.EmptyDataError:
    st.warning(
        "The GOLD CSV file is empty or contains no columns."
    )

except FileNotFoundError:
    st.error(
        "The GOLD CSV file was not found."
    )


# --------------------------------------------------
# Dashboard header
# --------------------------------------------------

st.title("Morocco Weather Risk")

st.write(
    "Weather forecast analysis for delivery operations"
)


# --------------------------------------------------
# Filters
# --------------------------------------------------

st.subheader("Filters")

filtered_df = df.copy()


if not df.empty:

    fil1, fil2, fil3 = st.columns(3)

    with fil1:
        selected_city = st.selectbox(
            "City",
            ["All"]
            + sorted(
                df["city"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    with fil2:
        selected_date = st.selectbox(
            "Date",
            ["All"]
            + sorted(
                df["date"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    with fil3:
        selected_risk = st.selectbox(
            "Risk level",
            ["All"]
            + sorted(
                df["risk_level"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    # Apply filters

    if selected_city != "All":
        filtered_df = filtered_df[
            filtered_df["city"] == selected_city
        ]

    if selected_date != "All":
        filtered_df = filtered_df[
            filtered_df["date"] == selected_date
        ]

    if selected_risk != "All":
        filtered_df = filtered_df[
            filtered_df["risk_level"] == selected_risk
        ]


else:

    st.info(
        "No data available. The filters are disabled."
    )


# --------------------------------------------------
# KPIs
# --------------------------------------------------

if filtered_df.empty:

    number_of_cities = 0
    number_of_forecast_days = 0
    number_of_high_risk_periods = 0
    average_risk_score = None

else:

    number_of_cities = filtered_df["city"].nunique()

    number_of_forecast_days = filtered_df["date"].nunique()

    number_of_high_risk_periods = (
        filtered_df["risk_level"]
        .isin(["High", "Critical"])
        .sum()
    )

    average_risk_score = filtered_df["risk_score"].mean()


# --------------------------------------------------
# Overview
# --------------------------------------------------

st.subheader("Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Cities monitored",
        number_of_cities
    )

with col2:
    st.metric(
        "Forecast days",
        number_of_forecast_days
    )

with col3:
    st.metric(
        "High/Critical periods",
        number_of_high_risk_periods
    )

with col4:

    if average_risk_score is None:
        risk_score_display = "N/A"
    else:
        risk_score_display = f"{average_risk_score:.1f}"

    st.metric(
        "Average risk score",
        risk_score_display
    )


# --------------------------------------------------
# Weather data
# --------------------------------------------------

st.subheader("Weather Forecast Data")


if filtered_df.empty:

    st.info(
        "No weather data available for the current selection."
    )

else:

    st.dataframe(
        filtered_df,
        use_container_width=True
    )