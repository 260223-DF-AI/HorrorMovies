"""
For analysis-related functionality
"""

import pandas as pd

def read_data(file_path) -> pd.DataFrame:
    """
    Read data from a CSV file and return a DataFrame
    """
    return pd.read_csv(file_path)