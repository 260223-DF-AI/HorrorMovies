"""
For analysis-related functionality
"""

import pandas as pd

import matplotlib.pyplot as plt

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


@log_execution
def count_movies_by_year_after(df: pd.DataFrame, year: int) -> pd.Series:
    """
    Count movies released after a given year, grouped by release year.

    Args:
        df: DataFrame to be analyzed
        year: Only include movies released after this year

    Returns:
        Series indexed by release year with movie totals for each year
    """
    
    # if no dates are assigned to the movie, error will raise
    if "release_date" not in df.columns:
        raise ValueError("DataFrame must contain a 'release_date' column")

    # filter the movies that are released after the specified year
    release_dates = df["release_date"]
    release_years = release_dates.dropna().dt.year.astype(int)
    filtered_years = release_years[release_years > year]

    return filtered_years.value_counts().sort_index()

@log_execution
def plot_movies(df: pd.DataFrame, year: int, show_plot: bool = True) -> pd.Series:
    """
    Plot a histogram showing how many movies were released each year after a given year.

    Args:
        df: Verified DataFrame to be analyzed
        year: Only include movies released after this year
        show_plot: Display the plot when True

    Returns:
        Series indexed by release year with movie totals for each year
    """
    yearly_counts = count_movies_by_year_after(df, year)

    if yearly_counts.empty:
        raise ValueError(f"No movies found after {year}")

    plt.figure(figsize=(10, 6))
    plt.hist(
        yearly_counts.index,
        bins=range(year + 1, yearly_counts.index.max() + 2),
        weights=yearly_counts.values,
        edgecolor="black",
        align="left",
        rwidth=0.9,
    )
    plt.title(f"Movies Released After {year}")
    plt.xlabel("Release Year")
    plt.ylabel("Number of Movies")
    plt.xticks(yearly_counts.index, rotation=45)
    plt.grid(axis="y", alpha=0.75)
    plt.tight_layout()
    plt.savefig("movies_by_year.png")  # Save the plot as an image file

    if show_plot:
        plt.show()
    else:
        plt.close()

    return yearly_counts

if __name__ == "__main__":
    # for testing purposes
    movies_df, _ = load_data("data/horror_movies.csv")
    print(analyze_basic_data(movies_df))
    print(analyze_column(movies_df, "budget"))

    print(plot_movies(movies_df, 1989))