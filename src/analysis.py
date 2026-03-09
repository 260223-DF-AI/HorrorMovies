"""
For analysis-related functionality
"""

import pandas as pd
from validate import load_data

def analyze_basic_data(df: pd.DataFrame) -> dict:
    """
    Analyze the provided DataFrame and return a dict. with very basic results.

    Taking DF and giving a set of info.
    """
    basic_data = {}

    basic_data["total_movies"] = len(df)
    basic_data["average_runtime"] = df["runtime"].mean()
    basic_data["average_budget"] = df["budget"].mean()
    basic_data["average_revenue"] = df["revenue"].mean()

    return basic_data