"""
Test functionality from analysis.py 
"""
import pandas as pd
import pytest

from src.analysis import analyze_basic_data
from src.validate import load_data

def test_analyze_basic_data():
    df: pd.DataFrame = load_data("data/horror_movies.csv")
    results: dict = analyze_basic_data(df)

    assert isinstance(results, dict)

    assert len(results.keys()) == 4
    

   