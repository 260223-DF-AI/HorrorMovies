import pandas as pd

def filter(df: pd.DataFrame, column: str, range_start=None, range_end=None) -> pd.DataFrame:
    """
    Filters dataframe down to a range for a given column
    
    Args:
    - df (pd.DataFrame): The dataframe to be filtered down
    - column (str): The column name to use during filtering
    - range_start: The starting point (inclusive)
    - range_end: The ending point (inclusive)
    
    Returns:
    - df (pd.DataFrame): The filtered dataframe

    NOTE: Leaving both range_start and range_end empty will return the same, unchanged dataframe (no sorting occurs in this function)
    """

    if range_start and range_end:
        df = df[(df[column] >= range_start) & (df[column] <= range_end)]
    elif range_start:
        df = df[df[column] >= range_start]
    elif range_end:
        df = df[df[column] <= range_end]

    return df


if __name__ == "__main__":
    from validate import load_data

    df = load_data("../data/horror_movies.csv")