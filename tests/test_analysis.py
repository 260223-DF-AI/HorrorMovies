"""
Test functionality from analysis.py 
"""
import pandas as pd
import pytest

from src.analysis import analyze_basic_data, count_movies_by_year_after
from src.validate import load_data

def test_analyze_basic_data():
    """Test if the basic analysis of our data is correct"""

    # discard rejects, unnecessary for test
    df_valid, df_rejects = load_data("data/horror_movies.csv")
    results: dict = analyze_basic_data(df_valid)

    assert isinstance(results, dict)

    assert len(results.keys()) == 4


def test_count_movies_by_year_after():
    """Test if the count of movies by year after a specified year is correct"""

    # discard rejects, unnecessary for test
    df_valid, df_rejects = load_data("data/horror_movies.csv")

    # analyze the counts after 2020
    results = count_movies_by_year_after(df_valid, 2020)

    assert results.to_dict() == {2021: 1992, 2022: 1399}

   
