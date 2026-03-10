import re

import pandas as pd
from pycountry import languages

"""
Functionality related to cleansing & validating our dataset
"""


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load data from file, parse through and clean for analysis and manipulation
    
    Args:
        filepath (str): Path to file to be opened, including file name
    
    Returns:
        df (pd.DataFrame): Parsed and cleaned dataframe.
    """

    # match string after final period to get file extension
    extension = re.match(r".*\.([^.]+)$", filepath).group(1).lower()
    if extension == "csv":
        df = pd.read_csv(filepath)
    elif extension == "json":
        df = pd.read_json(filepath)
    else:
        raise ValueError("Unsupported file format")

    # validate_data assumes horror data, maybe we make it more generic
    # and have separate validate_horror_data func
    if filepath == "data/horror_movies.csv": 
        df = validate_data(df)

    return df

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate provided DataFrame
    - Drop duplicates
    - Type checking
    - Fill/Drop missing values

    Returns:
    - df (pd.DataFrame): Cleaned and validated data
    - rejects_df (pd.DataFrame): Any entries dropped (duplicates and entries missing id original_title or title)
    """
    # df = df.drop_duplicates()
    # Drop unused columns
    df = df.drop(columns=["poster_path", "status", "backdrop_path"])

    # Try to fill missing title/original_title with original_title/title respectively
    df["title"] = df["title"].fillna(df["original_title"])
    df["original_title"] = df["original_title"].fillna(df["title"])

    # Fill/Drop Missing Values
    # If both original_title and title were missing, they will remain as NaN, drop
    drop_mask = df.duplicated() | df[["id", "original_title", "title"]].isna().any(axis=1)
    rejects_df = df[drop_mask]
    df = df[~drop_mask]

    # df = df.dropna(subset=["id", "original_title", "title"])

    # Type Checking
    # TODO: maybe drop type conversions (to_numeric, to_datetime, astype), only adding right now as confirmation read_csv properly converted everything
    df["id"] = pd.to_numeric(df["id"])
    df["release_date"] = pd.to_datetime(df["release_date"])
    df["popularity"] = pd.to_numeric(df["popularity"])
    df["vote_count"] = pd.to_numeric(df["vote_count"])
    df["vote_average"] = pd.to_numeric(df["vote_average"])
    df["budget"] = pd.to_numeric(df["budget"])
    df["revenue"] = pd.to_numeric(df["revenue"])
    df["runtime"] = pd.to_numeric(df["runtime"])
    df["adult"] = df["adult"].astype("bool")
    df["collection"] = pd.to_numeric(df["collection"])

    # String standardization
    df["original_title"] = df["original_title"].str.title().str.strip()
    df["title"] = df["title"].str.title().str.strip()
    df["original_language"] = df["original_language"].str.strip().map(code_to_language_name)
    df["genre_names"] = df["genre_names"].str.title().str.strip()
    df["collection_name"] = df["collection_name"].str.title().str.strip()

    return df, rejects_df

def code_to_language_name(code):
    if (code == "cn"):
        return "Chinese"
    try:
        lang = languages.get(alpha_2=code)
        return lang.name if lang else "Unknown"  # fallback to original code if not found
    except Exception:
        return code

# for testing
if __name__ == "__main__":
    print(load_data("data/horror_movies.csv").shape)
    # print(load_data("data/sample.json"))