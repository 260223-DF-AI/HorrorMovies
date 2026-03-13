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

from rich import print
from rich.align import Align
# from rich.columns import Columns
# from rich.console import Console, Group
# from rich.layout import Layout
# from rich.live import Live
# from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax

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