"""
Test functionality from validate.py
"""

import pandas as pd
import pytest

from src.validate import load_data

@pytest.mark.parametrize("filepath,row_expected,column_expected", [
    ("data/horror_movies.csv", 32540, 17),
    ("data/sample.json", 6, 4)
])
def test_load_data(filepath, row_expected, column_expected):
    """Test loading our horror_movies dataset"""
    df = load_data(filepath)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    # ideal number of columns after validation
    assert df.shape[1] == column_expected
    assert df.shape[0] == row_expected

    # checks specific values of the DataFrame
    assert df.iloc[1, 2] == 145
    assert df.iloc[2, 1] == 103

def test_nonexistent_file():
    """Test loading a file that does not exist"""

    with pytest.raises(ValueError):
        load_data("data/file_doesn't_exist.txt")
