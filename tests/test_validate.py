import pytest


from src.validate import load_data, validate_data
import pandas as pd



def test_load_data_csv():
    """Test loading our horror_movies dataset"""
    df = load_data("data/horror_movies.csv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    # ideal number of columns after validation
    assert df.shape[1] == 17
    assert df.shape[0] == 32540

