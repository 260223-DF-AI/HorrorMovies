"""
Test functionality from validate.py
"""

import pandas as pd
import pytest

from src.validate import load_data

def test_load_data_csv():
    """Test loading our horror_movies dataset"""
    df = load_data("data/horror_movies.csv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    # ideal number of columns after validation
    assert df.shape[1] == 17
    assert df.shape[0] == 32540

def test_load_data_json():
    """Test loading a sample JSON file"""
    df = load_data("data/sample.json")

    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    assert df.shape[1] == 4
    assert df.shape[0] == 6



def test_nonexistent_file():
    """Test loading a file that does not exist"""

    with pytest.raises(ValueError):
        load_data("data/file_doesn't_exist.txt")
