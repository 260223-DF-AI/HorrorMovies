"""
Test functionality from validate.py
"""

import pandas as pd
import pytest

from src.validate import load_data

@pytest.mark.parametrize("filepath,column,row", [
    ("data/horror_movies.csv", 32540, 17),
    ("data/sample.json", 6, 4)
])
def test_load_data(filepath, column, row):
    """Test loading our files and validating the data"""
    
    df = load_data(filepath)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    # ideal number of columns and rows after validation
    assert df.shape[0] == column
    assert df.shape[1] == row

    # checks specific values of the JSON DataFrame
    if filepath == 'data/sample.json':
        assert df.iloc[1, 2] == 145
        assert df.iloc[2, 1] == 103

def test_nonexistent_file():
    """Test loading a file that does not exist"""

    with pytest.raises(ValueError):
        load_data("data/file_doesn't_exist.txt")
