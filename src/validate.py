import pandas as pd

"""
Functionality related to cleansing & validating our dataset
"""


def validate_data(file_path: str) -> pd.DataFrame:
    """Return DataFrame storing validated dataset."""

    df: pd.DataFrame = pd.read_csv(file_path)

    # actually validate the data

    return df


# for testing
if __name__ == "__main__":
    print(validate_data("data/horror_movies.csv").head())