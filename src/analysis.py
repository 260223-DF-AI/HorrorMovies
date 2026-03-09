"""
For analysis-related functionality
"""

import pandas as pd
from src.validate import load_data

def analyze_basic_data(df: pd.DataFrame) -> dict:
    """
    Analyze the provided DataFrame and return a dict. with very basic results.

    Args:
        df: DataFrame to be analyzed

    Returns:
        basic_data: Dict. containing basic analysis results
    """
    basic_data = {}

    # retrieve basic data and append the key-value pairs to the basic_data dict.
    basic_data["total_movies"] = len(df)
    basic_data["average_runtime"] = round(float(df["runtime"].mean()), 2)
    basic_data["average_budget"] = round(float(df["budget"].mean()), 2)
    basic_data["average_revenue"] = round(float(df["revenue"].mean()), 2)

    return basic_data

# for testing purposes
print(analyze_basic_data(load_data("data/horror_movies.csv")))