"""Interacting with PostgreSQL"""

import pandas as pd

def load_postgresql(filepath: str) -> pd.DataFrame:
    """Load data from PostgreSQL database file, return dataframe"""
    
    df = None

    with open(filepath, "r", encoding="utf-8") as f:
        df = None        
    
    return df if df else None

def save_postgresql(filepath: str, df: pd.DataFrame):
    """Save dataframe to PostgreSQL database file"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("")



if __name__ == "__main__":
    pass