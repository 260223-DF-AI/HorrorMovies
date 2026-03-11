"""
For analysis-related functionality
"""

import pandas as pd
from .validate import load_data
from .logger import log_execution

@log_execution
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


@log_execution
def analyze_column(df: pd.DataFrame, column: str) -> dict:
    """
    Analyze a specific column in the provided DataFrame and return a dict. with basic results.

    Args:
        df: DataFrame to be analyzed
        column: Column name to be analyzed

    Returns:
        column_data: Dict. containing basic analysis results for the specified column
    """
    column_data = {}

    # retrieve basic data and append the key-value pairs to the column_data dict.

    # finds the most common value within a column. could be useful for "genre" and "collection_name"
    column_data["most_common_value"] = int(df[column].mode()[0])

    # finds the highest value in a column. good for finding highest grossing or highest budget
    column_data["highest_value"] = df.loc[df[column].idxmax()]["title"]

    # finds the lowest value in a column. good for finding lowest grossing or lowest budget
    column_data["lowest_value"] = df.loc[df[column].idxmin()]["title"]

    return column_data


if __name__ == "__main__":
    # for testing purposes
    print(analyze_basic_data(load_data("data/horror_movies.csv")))
    print(analyze_column(load_data("data/horror_movies.csv"), "budget"))