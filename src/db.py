"""Interacting with PostgreSQL"""
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.types import * #replace with only necessary types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from dotenv import load_dotenv
from datetime import datetime
import os

from .validate import load_data


class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_title: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    original_language: Mapped[str] = mapped_column(String(2), nullable=False)
    # metadata: Mapped["Metadata"] = mapped_column(ForeignKey("metadatas.id"))
    release_date: Mapped[datetime] = mapped_column(Date)
    # rating: Mapped["Rating"] = mapped_column(ForeignKey("ratings.id"))
    # finance: Mapped["Finance"] = mapped_column(ForeignKey("finances.id"))
    genres: Mapped[list["Genre"]] = relationship("genres", back_populates="movies")
    # collection_id: Mapped[int] = mapped_column(ForeignKey("collections.id"))
    collection: Mapped["Collection"] = relationship("collections", back_populates="movies")

class Metadata(Base):
    __tablename__ = "metadatas"

    # id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    overview: Mapped[str] = mapped_column(Text)
    tagline: Mapped[str] = mapped_column(Text)
    adult: Mapped[str] = mapped_column(Boolean)

class Rating(Base):
    __tablename__ = "ratings"

    # id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    popularity: Mapped[float] = mapped_column(Float)
    vote_count: Mapped[int] = mapped_column(Integer)
    vote_average: Mapped[float] = mapped_column(Float)

class Finance(Base):
    __tablename__ = "finances"

    # id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    budget: Mapped[int] = mapped_column(Integer)
    revenue: Mapped[int] = mapped_column(Integer)

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    genre_name: Mapped[str] = mapped_column(String(14), nullable=False)

    movies: Mapped[list["Movie"]] = relationship("movies", back_populates="genres")

class Movie_Genre(Base):
    # Junction Table
    __tablename__ = "movies_genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))

    # ??? do we need relationshps defined here? do we even need this class?

class Collection(Base):
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    collection_name: Mapped[str] = mapped_column(String(30), nullable=False)
    movies: Mapped[list["Movie"]] = relationship("movies", back_populates="collections")


def setup():
    """
    Setup connection to PostgreSQL database using SQLAlchemy
    """
    load_dotenv()
    CS = os.getenv("CS")
    engine = create_engine(CS)

    valid_df, rejects_df = load_data("data/horror_movies.csv")

    rejects_df.to_sql(name="horror_movies_rejects", con=engine, index=False, if_exists="replace")
    
    # Create dataframes for individual tables
    movie_df = valid_df[["id", "original_title", "title", "original_language", "release_date"]]
    metadata_df = valid_df[["id", "overview", "tagline"]]
    rating_df = valid_df[["id", "popularity", "vote_count", "vote_average"]]
    finance_df = valid_df[["id", "budget", "revenue"]]
    genre_names: list = valid_df["genre_names"].tolist() #.apply(lambda x : x.split(", "))
    genre_list: list = [name.split(", ") for name in genre_names]
    genres_flat = [name for sublist in genre_list for name in sublist]
    genres_unique: set = set(genres_flat)
    genre_df = pd.DataFrame(genres_unique, columns=["genre_name"])

    collections_df = valid_df[["collection", "collection_name"]]
    collections_df = collections_df.rename(columns={"collection": "collection_id"})
    collections_df = collections_df.dropna().drop_duplicates()

    movie_df.to_sql(name="movies", con=engine, index=False, if_exists="replace")
    metadata_df.to_sql(name="metadatas", con=engine, index=False, if_exists="replace")
    rating_df.to_sql(name="ratings", con=engine, index=False, if_exists="replace")
    finance_df.to_sql(name="finances", con=engine, index=False, if_exists="replace")
    genre_df.to_sql(name="genres", con=engine, index=True, if_exists="replace")
    collections_df.to_sql(name="collections", con=engine, index=False, if_exists="replace")


    for index, genres_str in enumerate(genre_names):
        for genre in genres_str.split(", "):
            # get movie id for movie attached to the genre we are operating on
            movie_id = valid_df.loc[index].id

            # get the genre id for the genre string we are operating on
            genre_id = genre_df.loc[genre_df["genre_name"] == genre].iloc[0]
            print(f"{movie_id}, {genre_id.iloc[0]}")

            # use movie_id and genre_id to make new dataframe to .to_sql
            # or movie_genre objects to add to table with sqlalchemy


if __name__ == "__main__":
    setup()