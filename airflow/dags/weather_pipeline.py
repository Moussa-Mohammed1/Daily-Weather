from datetime import datetime
from datetime import timedelta
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from src.extraction_pipeline import main as extract
from src.transformation_pipeline import clean_and_join, create_features_file


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLD_PATH = PROJECT_ROOT / "data" / "gold" / "weather_features.csv"


def load_to_postgres():
    from src.load.loader import load_data

    load_data()


def refresh_dashboard_data():
    if not GOLD_PATH.exists():
        raise FileNotFoundError(f"Dashboard data was not created: {GOLD_PATH}")

    dashboard_data = pd.read_csv(GOLD_PATH)
    if dashboard_data.empty:
        raise ValueError("Dashboard data is empty")

    print(f"Dashboard data refreshed: {len(dashboard_data)} rows")

with DAG(
    dag_id="etl-weather",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["weather", "morocco", "etl"],
) as dag:
    extraction = PythonOperator(
        task_id="extract_weather",
        python_callable=extract,
    )
    cleaning_and_joining = PythonOperator(
        task_id="clean_and_join",
        python_callable=clean_and_join,
    )
    feature_engineering = PythonOperator(
        task_id="feature_engineering",
        python_callable=create_features_file,
    )
    loading = PythonOperator(
        task_id="load_postgres",
        python_callable=load_to_postgres,
    )
    dashboard_refresh = PythonOperator(
        task_id="refresh_dashboard",
        python_callable=refresh_dashboard_data,
    )

    extraction >> cleaning_and_joining >> feature_engineering >> loading >> dashboard_refresh