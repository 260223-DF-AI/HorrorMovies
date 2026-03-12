"""
Test functionality from analysis.py 
"""
import pandas as pd
import pytest

from src.analysis import analyze_basic_data, count_movies_by_year_after, plot_movies
from src.validate import load_data

def test_analyze_basic_data():
    # discard rejects, unnecessary for test
    df_valid, df_rejects = load_data("data/horror_movies.csv")
    results: dict = analyze_basic_data(df_valid)

    assert isinstance(results, dict)

    assert len(results.keys()) == 4


def test_count_movies_by_year_after():
    df = pd.DataFrame({"release_date": pd.to_datetime(["1999-01-01", "2001-06-01", "2001-10-31", "2003-02-14", None])})

    results = count_movies_by_year_after(df, 2000)

    assert results.to_dict() == {2001: 2, 2003: 1}


def test_plot_movies_returns_yearly_counts_without_showing_plot():
    df = pd.DataFrame({"release_date": pd.to_datetime(["2008-01-01", "2011-03-04", "2011-08-09", "2012-10-31"])})

    results = plot_movies(df, 2010, show_plot=False)

    assert results.to_dict() == {2011: 2, 2012: 1}

   
