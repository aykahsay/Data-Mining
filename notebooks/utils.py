import pandas as pd
import numpy as np


# This function is to be used in testing as we wait for data to be cleaned
def load_and_drop_na_data(filepath):
    """Load data with automatic cleaning (drops nulls in all columns)"""
    df = pd.read_csv(filepath)

    # 1. Basic cleaning
    print(f"Raw data: {len(df)} rows")
    df = df.dropna()  # Drop rows with any null values

    # Optional: Remove whitespace and empty strings for all string/object columns
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
        df = df[df[col] != '']  # Drop rows where any string column is empty

    # 2. Deduplication
    initial_count = len(df)
    df = df.drop_duplicates(keep='first')
    print(f"Removed {initial_count - len(df)} duplicates")

    # 3. Index reset (critical for alignment)
    df = df.reset_index(drop=True)

    # 4. Final validation
    assert df.isnull().sum().sum() == 0, "Nulls still exist!"
    assert not df.duplicated().any(), "Duplicates remain!"
    print(f"Clean data: {len(df)} rows")

    return df
