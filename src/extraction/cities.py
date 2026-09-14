import pandas as pd

def extract_raw_cities(input_path: str) -> pd.DataFrame:
    return pd.read_csv(input_path)

def save_bronze_cities(df: pd.DataFrame, output_path: str) -> None:
    df.to_csv(output_path, index=False)
    