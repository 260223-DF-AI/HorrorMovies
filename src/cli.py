"""
Functionality relating to the application's command line usage

Rich reference material to use:


- Landing page:
    https://github.com/Textualize/rich

- Live displays (animate elements):
    https://github.com/Textualize/rich/blob/master/examples/table_movie.py
"""

import pandas as pd
from rich import print
from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.text import Text

from time import sleep

from .db import get_session
from .db import Movie, Metadata, Rating, Finance, Genre, Movie_Genre, Collection
from .validate import load_data, validate_data
from sqlalchemy import func
from sqlalchemy import select


def menu() -> None:
    """
    Enters the initial command line menu 
    """

    console = Console(width=80, style="#B8FCC8")
    # console.rule("[bold u]Horror Movies Data Analysis[/]", style="#FCB8EC")

    options: list[str] = [
        "Display sample dataframe",
        "First test option",
        "Second test option"
    ]

    
    columns: Columns = Columns(width=40, align="center", column_first=True)
    columns.add_renderable("[bold u]Options[/]")

    for index, option in enumerate(options, 1):
        columns.add_renderable(f"[b]{index}.[/] {option}")

    layout: Layout = get_menu_layout()
    console.print(layout)
    layout["options"].update(Align(columns, vertical="middle"))
    # console.print(layout)
    # print(layout)

    # with Live(layout, screen=True) as live:
    #     try:
    #         while True:
    #             sleep(1)
    #     except KeyboardInterrupt:
    #         exit()




def get_menu_layout() -> Layout:
    """
    Construct main layout for initial menu.
    Layout top: "header"
    Layouts middle: "options" for option list and "extra" for extra unassigned space
    Layouts bottom: "footer"
    """

    layout: Layout = Layout()

    # layout of three rows in a column
    layout.split(
        Layout(name="header", size=2),
        Layout(ratio=1, name="main"),
        # Layout(size=10, name="footer")
    )

    layout["header"].update(Align.center(Text("Horror Movies Data Analysis", style="#FCB8EC bold underline")))

    # middle row itself is made of two columns
    layout["main"].split_row(Layout(name="options"), Layout(name="extra", ratio=2))

    # add text to the right side space
    layout["extra"].update(
        Align.center(
            Text(
                f"This is some extra unused space. For demonstration",
                justify="center",
                style="u"
            ),
            vertical="middle"
        )
    )

    return layout


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


def presentation() -> None:
    """
    A guided tour of multiple analyses that demonstrate 
    practical use of our project's database
    """

    with get_session() as session:
        # count movies by release year; group_by must include selected columns or an aggregate
        year_extracted = func.extract("year", Movie.release_date).label("release_year")
        
        # form query to pass to pandas
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

        print(create_df_table(df[df["Release Year"] > 2010], title="Movies Released After 2010 with Revenue > 0"))




if __name__ == "__main__":

    presentation()
    # df, df_rejects = load_data("data/horror_movies.csv")

    # small 4 column dataframe preview for testing
    # df_to_show: pd.DataFrame = df.head().iloc[:, :5]
    # df_to_show = df_to_show.drop(columns=["overview"])

    # print(create_df_table(df_to_show, title="Horror Movies Dataset Sample"))

    # menu()

