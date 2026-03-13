"""
Functionality relating to the application's command line usage

Rich reference material to use:


- Landing page:
    https://github.com/Textualize/rich

- Live displays (animate elements):
    https://github.com/Textualize/rich/blob/master/examples/table_movie.py
"""

import os
import pandas as pd
import platform
from time import sleep

from rich import print
from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax
from PIL import Image

from .db import get_session
from .db import Movie, Metadata, Rating, Finance, Genre, Movie_Genre, Collection
from .validate import load_data, validate_data
from sqlalchemy import func
from sqlalchemy import select

from .analysis import plot_vote_distribution, plot_movies
from .logger import log_execution

@log_execution
def clear_terminal(line_endings:int=0) -> None:
    """
    Clear terminal, printing `line_endings` number of newlines
    after clearing terminal.
    """
    # Check the operating system name
    if platform.system() == "Windows":
        # Command for Windows
        os.system('cls')
    else:
        # Command for Linux and macOS
        os.system('clear')

    # start terminal output a bit down
    if line_endings > 0:
        print("\n"*line_endings)

@log_execution
def create_df_table(df: pd.DataFrame, title:str="Data") -> Table:
    """
    Print `df` in a rich table.
    """

    # convert dataframe data to string for printing
    df = df.astype(str)

    table: Table = Table(title=title)

    # style each row, alternating dim and not dim
    # table.row_styles = ["green not dim", "green dim"]
    table.row_styles = ["not dim", "dim"]
    

    # add df column headers to the table
    for index, col in enumerate(df.columns):
        if index % 2 == 0:
            table.add_column(f"[bold purple]{col.title()}[/]", style="#ad97e3")
        else:
            table.add_column(f"[bold green]{col.title()}[/]", style="green")

    # add df row values to the table
    for row in df.values:
        row = row.astype(str)
        table.add_row(*row)

    return table

@log_execution
def print_side_by_side(df: pd.DataFrame, right_side_content: str|tuple, title: str = "") -> None:
    """
    Given dataframe to print on leftside and string to print on right side,
    print data side by side. Optionally display a title above the layout.
    """

    def get_right_side_content() -> Text|Syntax:
        if isinstance(right_side_content, str):
            # create text for right side
            text: Text = Text(right_side_content, justify="center")
            text_aligned = Align.center(text, vertical="middle")
            return text_aligned

        # if not string, it's a tuple of filename & range of code lines to showcase
        else:
            filename, line_range = right_side_content
            syntax = Syntax.from_path(
                filename,
                line_numbers=True,
                line_range=(line_range[0], line_range[1]),
                # highlight_lines={190} # Highlight specific line within the range
            )
            return syntax
        
    right_side_content = get_right_side_content()

    # create table for left side
    table: Table = create_df_table(df)

    # use a table for side-by-side layout with vertical alignment
    # display title if provided
    if title:
        layout_table: Table = Table(show_header=False, show_footer=False, box=None, padding=(0, 2), title=title, title_style="bold #FCB8EC")
    else:
        layout_table: Table = Table(show_header=False, show_footer=False, box=None, padding=(0, 2))
    
    layout_table.add_column(no_wrap=False, vertical="Center")
    layout_table.add_column(no_wrap=False, vertical="Center")
    layout_table.add_row(table, right_side_content)

    print(layout_table)

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

        print_side_by_side(df[df["Release Year"] > 2010], ("src/cli.py", (137, 148)), title="Horror Movie Release Year Totals")

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

    input("What year do we want to start seeing the highest grossing horror films from? ")

    plot_vote_distribution()
    with Image.open("data/vote_distribution.png") as img:
        print(f"[bold green i]Opening bar graph displaying the vote distribution among the dataset's ratings![/]")
        img.show()


if __name__ == "__main__":
    presentation()