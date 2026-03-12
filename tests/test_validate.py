"""
Test functionality from validate.py
"""
import pandas as pd
import pytest
from pycountry import languages

from src.validate import load_data, code_to_language_name

@pytest.mark.parametrize("filepath,column,row", [
    ("data/horror_movies.csv", 32405, 16),
    ("data/horror_movies.json", 32405, 16)
])
def test_load_data(filepath, column, row):
    """Test loading our files and validating the data"""
    
    df, df_rejects = load_data(filepath)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    # ideal number of columns and rows after validation
    assert df.shape[0] == column
    assert df.shape[1] == row

    # check that the original title in a specified cell is correct
    assert df.at[10, "original_title"] == "The Exorcism of God"

@pytest.mark.parametrize("code,name", [
    ("en", "English"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("de", "German"),
    ("it", "Italian"),
    ("uh", "Unknown"), # not a real code, should return "Unknown"
    ("cn", "Chinese"),
])
def test_code_language_name(code, name):
    """Test if the language codes translate to their correct names"""

    assert code_to_language_name(code) == name

def test_nonexistent_file():
    """Test loading a file that does not exist"""

    with pytest.raises(ValueError):
        load_data("data/file_doesn't_exist.txt")
