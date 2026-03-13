"""
For analysis-related functionality
"""

import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import pandas as pd
from sqlalchemy import func
from sqlalchemy import select

from .db import get_session, Movie, Rating, Finance
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
def count_movies_by_year_after(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    Count movies released after a given year, grouped by release year.

    Args:
        df: DataFrame to be analyzed
        year: Only include movies released after this year

    Returns:
        DataFrame indexed by release year with movie count for each year
    """
    
    with get_session() as session:
        # extract year from release date
        year_extracted = func.extract("year", Movie.release_date).label("release_year")

        # query retrieves year & movie release counts
        query = (
            select(year_extracted, func.count(Movie.id))
            .where(year_extracted > year)  # only include movies released after specified year
            .group_by(year_extracted)
            .order_by(year_extracted)
        )
        df = pd.read_sql_query(query, session.bind)
        df.rename(columns={"release_year": "Release Year", "count_1": "Movie Count"}, inplace=True)
        return df.set_index("Release Year")["Movie Count"]


@log_execution
def plot_movies(df: pd.DataFrame, year: int) -> None:
    """
    Plot a histogram showing how many movies were released each year after a given year.

    Args:
        df: Verified DataFrame to be analyzed
        year: Only include movies released after this year
    """
    
    # query the data from the database
    yearly_counts = count_movies_by_year_after(df, year)

    if yearly_counts.empty:
        raise ValueError(f"No movies found after {year}")

    # begin plotting histogram
    plt.figure(figsize=(10, 6))
    plt.hist(
        yearly_counts.index,
        bins=range(year + 1, int(yearly_counts.index.max()) + 2),
        weights=yearly_counts.values,
        color="black",
        edgecolor="black",
        align="left",
        rwidth=0.9,
    )
    plt.title(f"Movies Released After {year}")
    plt.xlabel("Release Year")
    plt.ylabel("Number of Movies")
    plt.xticks(yearly_counts.index, rotation=45)
    plt.grid(axis="y", alpha=0.75)
    plt.gcf().set_facecolor("orange")
    plt.tight_layout()
    plt.savefig("data/movies_by_year.png")  # Save the plot as an image file


@log_execution
def highest_gross_histogram(df: pd.DataFrame, year: int) -> None:
    """
    Output histogram of highest grossing movies by year, starting from a specified year.
    """

    with get_session() as session:
        release_year = func.extract("year", Movie.release_date).label("release_year")

        query = (
            select(Movie.title, release_year, Finance.revenue)
            .join(Finance, Movie.id == Finance.movie_id)
            .where(release_year > year)
            .where(Finance.revenue > 0)
        )

        df = pd.read_sql_query(query, session.bind)

    if df.empty:
        raise ValueError(f"No revenue data found after {year}")

    # keep exactly one movie per year: the highest-grossing entry in that year
    top_movies = df.loc[df.groupby("release_year")["revenue"].idxmax()].copy()
    top_movies["release_year"] = top_movies["release_year"].astype(int)
    top_movies = top_movies.sort_values("release_year")

    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        top_movies["release_year"],
        top_movies["revenue"],
        color="black",
        edgecolor="black",
    )

    for bar, title in zip(bars, top_movies["title"]):
        plt.text(
            bar.get_x() + (bar.get_width() / 2),
            bar.get_y(),
            title,
            color="#ad97e3",
            fontweight="bold",
            ha="center",
            va="bottom",
            rotation=90,
            fontsize=8,
        ).set_path_effects([PathEffects.withStroke(linewidth=3, foreground="black")])

    plt.title(f"Highest Grossing Film Per Year After {year}")
    plt.xlabel("Release Year")
    plt.ylabel("Revenue (per hundred millions)")
    plt.xticks(top_movies["release_year"], rotation=45)
    plt.grid(axis="y", alpha=0.75)
    plt.gcf().set_facecolor("orange")
    plt.tight_layout()
    plt.savefig("data/highest_grossing_by_year.png")


def plot_vote_distribution():
    """
    Plot histogram showing vote average distribution
    """

    with get_session() as session:
        # get df with all movies and their ratings
        query = session.query(Movie, Rating).join(Rating, Movie.id == Rating.movie_id).where(Rating.vote_average > 0)
        df = pd.read_sql_query(query.statement, session.bind)

    all_values = pd.Series([round(x * 0.1, 1) for x in range(0, 101)])
    counts = df["vote_average"].value_counts()
    full_counts = all_values.map(counts).fillna(0)
    plt.figure(figsize=(17,7))
    plt.gcf().set_facecolor("orange")
    ax = plt.bar(all_values, full_counts, width=0.08, color="black", edgecolor="black")
    ax = plt.gca()
    ticks = [x for x in all_values if x % 0.5 == 0]
    ax.set_xticks(ticks)
    ax.set_xticklabels(ticks)
    ax.set(title = "Average Vote Distribution", xlabel="Vote Average", ylabel = "Total Count")
    plt.savefig("data/vote_distribution.png")


if __name__ == "__main__":
    # for testing purposes
    # movies_df, _ = load_data("data/horror_movies.csv")
    # print(analyze_basic_data(movies_df))
    # print(analyze_column(movies_df, "budget"))

    # plot_movies(movies_df, 2000)
    # highest_gross_histogram(movies_df, 2010)
    # plot_vote_distribution()
    pass