"""
For analysis-related functionality
"""

import pandas as pd

def read_data(file_path: str) -> pd.DataFrame:
    """
    Read data from a CSV file and return a DataFrame
    """
    return pd.read_csv(file_path)

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate the DataFrame and return a cleaned version.
    Currently, this will drop any rows with missing values.
    This can be changed later
    """
    return df.dropna()