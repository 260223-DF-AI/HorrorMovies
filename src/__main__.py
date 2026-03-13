""" Main Project File"""

import pandas as pd
from PIL import Image # type: ignore
from sqlalchemy import func, select
from rich import print
from rich.table import Table

from .validate import load_data
from .logger import log_execution
from .cli import clear_terminal, create_df_table, print_side_by_side
from .db import Movie, Metadata, Rating, Finance, get_session
from .analysis import highest_gross_histogram


@log_execution
def yearly_movie_release_count() -> None:
    """
    Output analysis for movies released per year
    """

    with get_session() as session:
        # extract year from release date
        year_extracted = func.extract("year", Movie.release_date).label("release_year")
        
        # query retrieves year & movie release counts
        query = (
            select(year_extracted, func.count(Movie.id))
            .join(Finance, Movie.id == Finance.movie_id)
            .where(Finance.revenue > 0)
            .group_by(year_extracted)
            .order_by(year_extracted)
        )

        # retrieve dataframe holding data from query result
        df = pd.read_sql_query(query, session.bind)
        df.rename(columns={"release_year": "Release Year", "count_1": "Movie Count"}, inplace=True)

        print_side_by_side(df[df["Release Year"] > 2010], ("src/__main__.py", (22, 36)), title="Horror Movie Release Year Totals")

@log_execution
def get_movie(title: str="Friday the 13th Part VIII: Jason Takes Manhattan") -> None:
    """
    Output basic information on a single movie
    """
    if not title:
        title = "Friday the 13th Part VIII: Jason Takes Manhattan"
    with get_session() as session:
        query = (
            select(Movie.title, Movie.release_date, Metadata.tagline, Rating.vote_average, (Finance.revenue - Finance.budget).label("profit"))
            .join(Metadata, Movie.id == Metadata.movie_id)
            .join(Rating, Movie.id == Rating.movie_id)
            .join(Finance, Movie.id == Finance.movie_id)
            .where(Movie.title == title)
        )

        df = pd.read_sql_query(query, session.bind)
        df.rename(columns={"title": "Title", "release_date": "Release Date", "collection_name": "Collection", "tagline": "Tagline", "vote_average": "Rating", "profit": "Profit"})

        table: Table = create_df_table(df, f"Movie Information: {title}")
        print(table)

@log_execution
def presentation() -> None:
    """
    A guided tour of multiple analyses that demonstrate 
    practical use of our project's database
    """
    clear_terminal()
    clear_terminal()

    title = ""
    while title != "pass":
        print("What's your favorite [bold red underline]scary[/] movie?\" -[bold dim]Ghostface[/], [i]SCREAM[/] (1996)")
        title = input()
        if title == "pass":
            break
        get_movie(title)

    # Show yearly movie release count analysis
    clear_terminal(line_endings=10)
    yearly_movie_release_count()
    input() # pause execution till hitting key

    clear_terminal()

    # open matplot of yearly movies released past 2010
    # plot_movies(year=2010)
    with Image.open("data/movies_by_year.png") as img:
        print(f"[bold #ad97e3 i]Opening graph displaying total horror movies released each year since 2010![/]")
        img.show()

    input()
    clear_terminal()

    # plot_vote_distribution()
    with Image.open("data/vote_distribution.png") as img:
        print(f"[bold green i]Opening bar graph displaying the vote distribution among the dataset's ratings![/]")
        img.show()

    input()

    clear_terminal()

    movies_df, _ = load_data("data/horror_movies.csv")
    print("[bold orange i]What year do we want to start seeing the highest grossing horror films from?[/]")
    input_year = input()
    highest_gross_histogram(movies_df, int(input_year))
    with Image.open("data/highest_grossing_by_year.png") as img:
        print(f"[bold orange i]Opening histogram displaying highest grossing movies by year![/]")
        img.show()

    input()


if __name__ == "__main__":
    presentation()