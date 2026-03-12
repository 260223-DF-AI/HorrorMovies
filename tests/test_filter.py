""" Test filtering function to return ranges of data by columns """

import pandas as pd
import pytest

from src.filter import filter
from src.validate import *

@pytest.fixture
def dataframe():
    df, rejects = load_data("data/horror_movies.csv")
    return df, rejects

@pytest.mark.parametrize("column,lower,upper,count,min_id,max_id", [
    ("release_date", pd.to_datetime("1980-01-01"), pd.to_datetime("1989-12-31"), 2563, 5817, 29592), # 80's Horror Movies
    ("vote_average", 9.0, None, 853, 4230, 28), # Vote averages >= 9.0
    ("budget", None, 1000000, 30985, 0, 210), # Budgets less that $1,000,000
    ("popularity", None, None, 32405, 32539, 0), # should return full DataFrame
])
def test_filter_bounding(dataframe, column, lower, upper, count, min_id, max_id):
    """ Test lower bound, upper bound, both and neither on range of data """

    df, _ = dataframe
    df = filter(df, column, lower, upper)

    assert df.shape[0] == count
    assert df[column].idxmin() == min_id
    assert df[column].idxmax() == max_id

def test_filter_rejects(dataframe):
    """ Test if rejects contains the correct number of entries """

    df, rejects = dataframe

    assert df.shape[0] == 32405
    assert rejects.shape[0] == 135