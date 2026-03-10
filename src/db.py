"""Interacting with PostgreSQL"""

import psycopg2
import pandas as pd

def get_connection():
    try:
        return psycopg2.connect(
            database="horror_movies",
            user="postgres",
            password="password",
            host="localhost",
            port=5432
        )
    except Exception as e:
        print(e)
        return False

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
    conn = get_connection()
    if conn:
        print("Connection established")
        conn.autocommit = True
        cursor = conn.cursor()
        sql = ''' CREATE database horror_movies '''
        cursor.execute(sql)
        print("Database created successfully")
        conn.close()
    else:
        print("Connection failed")