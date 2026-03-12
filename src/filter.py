import pandas as pd
from .logger import log_execution

@log_execution
def filter(df: pd.DataFrame, column: str, lower_bound=None, upper_bound=None) -> pd.DataFrame:
    """
    Filters dataframe down to a range for a given column
    
    Args:
    - df (pd.DataFrame): The dataframe to be filtered down
    - column (str): The column name to use during filtering
    - lower_bound: The lowest value (inclusive)
    - upper_bound: The highest value (inclusive)
    
    Returns:
    - df (pd.DataFrame): The filtered dataframe

    NOTE: Leaving both lower_bound and upper_bound empty will return the same, unchanged dataframe (no sorting occurs in this function)
    """

    if lower_bound and upper_bound:
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    elif lower_bound:
        df = df[df[column] >= lower_bound]
    elif upper_bound:
        df = df[df[column] <= upper_bound]

    return df


if __name__ == "__main__":
    from .validate import load_data

    df, rejects = load_data("data/horror_movies.csv")
    # print(df["status"].unique())
    # print(df.shape)
    # print(rejects.shape)
    # print(rejects)

    df_release = filter(df, "release_date", pd.to_datetime("1980-01-01"), pd.to_datetime("1989-12-31"))
    print(df_release.shape)
    print(f"{df_release["release_date"].min()}, {df_release["release_date"].max()}")
    print(df_release.loc[df_release["release_date"] == pd.to_datetime("1980-01-01")]["title"])
    print(df_release.loc[df_release["release_date"] == pd.to_datetime("1989-12-31")]["title"])

    df_vote = filter(df, "vote_average", 9.0)
    print(df_vote.shape)
    print(f"{df_vote["vote_average"].min()}, {df_vote["vote_average"].max()}")
    print(df_vote.loc[df_vote["vote_average"] == 9.0]["title"])
    print(df_vote.loc[df_vote["vote_average"] == 10.0]["title"])

    df_budget = filter(df, "budget", None, 1000000)
    print(df_budget.shape)
    print(f"{df_budget["budget"].min()}, {df_budget["budget"].max()}")
    print(df_budget.loc[df_budget["budget"] == 0]["title"])
    print(df_budget.loc[df_budget["budget"] == 1000000]["title"])

    df_pop = filter(df, "popularity")
    print(df_pop.shape)
    min = df_pop["popularity"].min()
    max = df_pop["popularity"].max()
    print(f"{min}, {max}")
    print(df_pop.loc[df_pop["popularity"] == min]["title"])
    print(df_pop.loc[df_pop["popularity"] == max]["title"])
