"""Interacting with PostgreSQL"""
import pandas as pd
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.types import * #replace with only necessary types
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker
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
    release_date: Mapped[datetime] = mapped_column(Date)
    # many-to-many through junction table movies_genres; use class names not table names
    genres: Mapped[list["Genre"]] = relationship(
        "Genre",
        secondary="movies_genres",
        back_populates="movies",
    )
    # foreign key pointing to the collections table; may be null when movie has no collection
    collection_id: Mapped[int | None] = mapped_column(ForeignKey("collections.collection_id"), nullable=True)
    collection: Mapped["Collection"] = relationship("Collection", back_populates="movies")

class Metadata(Base):
    __tablename__ = "metadatas"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    overview: Mapped[str] = mapped_column(Text)
    tagline: Mapped[str] = mapped_column(Text)
    adult: Mapped[str] = mapped_column(Boolean)

class Rating(Base):
    __tablename__ = "ratings"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    popularity: Mapped[float] = mapped_column(Float)
    vote_count: Mapped[int] = mapped_column(Integer)
    vote_average: Mapped[float] = mapped_column(Float)

class Finance(Base):
    __tablename__ = "finances"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    budget: Mapped[int] = mapped_column(Integer)
    revenue: Mapped[int] = mapped_column(Integer)

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    genre_name: Mapped[str] = mapped_column(String(14), nullable=False)

    movies: Mapped[list["Movie"]] = relationship(
        "Movie",
        secondary="movies_genres",
        back_populates="genres",
    )

class Movie_Genre(Base):
    # Junction Table
    __tablename__ = "movies_genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))

class Collection(Base):
    __tablename__ = "collections"

    collection_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    collection_name: Mapped[str] = mapped_column(String(30), nullable=False)
    movies: Mapped[list["Movie"]] = relationship("Movie", back_populates="collection")


def setup():
    """
    Setup connection to PostgreSQL database using SQLAlchemy
    """
    # initialize connection to postgres db
    load_dotenv()
    CS = os.getenv("CS")
    engine = create_engine(CS)

    valid_df, rejects_df = load_data("data/horror_movies.csv")

    rejects_df.to_sql(name="horror_movies_rejects", con=engine, index=False, if_exists="replace")
    
    # Create dataframes for individual tables
    # include collection column so we can establish FK
    movie_df = valid_df[["id", "original_title", "title", "original_language", "release_date", "collection"]]
    metadata_df = valid_df[["id", "overview", "tagline"]]
    rating_df = valid_df[["id", "popularity", "vote_count", "vote_average"]]
    finance_df = valid_df[["id", "budget", "revenue"]]
    genre_names: list = valid_df["genre_names"].tolist() #.apply(lambda x : x.split(", "))
    # build unique genres list and a numeric id for each one
    genre_list: list = [name.split(", ") for name in genre_names]
    genres_flat = [name for sublist in genre_list for name in sublist]
    # sort so the resulting ids are deterministic
    genres_unique = sorted(set(genres_flat))
    genre_df = pd.DataFrame(genres_unique, columns=["genre_name"])
    genre_df["id"] = range(len(genre_df))

    # build collection dataframe and keep ids to store on movies
    collections_df = valid_df[["collection", "collection_name"]]
    collections_df = collections_df.rename(columns={"collection": "collection_id"})
    collections_df = collections_df.dropna().drop_duplicates()

    # rename dataframe fields to match ORM classes
    movie_df = movie_df.rename(columns={"collection": "collection_id"})
    metadata_df = metadata_df.rename(columns={"id": "movie_id"})
    rating_df = rating_df.rename(columns={"id": "movie_id"})
    finance_df = finance_df.rename(columns={"id": "movie_id"})

    # write dataframes to respective databases!
    movie_df.to_sql(name="movies", con=engine, index=False, if_exists="replace")
    metadata_df.to_sql(name="metadatas", con=engine, index=False, if_exists="replace")
    rating_df.to_sql(name="ratings", con=engine, index=False, if_exists="replace")
    finance_df.to_sql(name="finances", con=engine, index=False, if_exists="replace")
    genre_df.to_sql(name="genres", con=engine, index=False, if_exists="replace")
    collections_df.to_sql(name="collections", con=engine, index=False, if_exists="replace")

    # explode the genre_names field into one row per (movie, genre)
    exploded = valid_df[["id", "genre_names"]].copy()
    exploded = exploded.assign(
        genre_name=exploded["genre_names"].str.split(", ")
    ).explode("genre_name")
    exploded = exploded.drop(columns=["genre_names"])

    # merge with genre_df to get the numeric genre id
    movie_genre_df = exploded.merge(genre_df, on="genre_name", how="left")
    movie_genre_df = movie_genre_df.rename(columns={"id_x": "movie_id", "id_y": "genre_id"})

    # assign a sequential id for the linking table
    movie_genre_df = movie_genre_df.reset_index(drop=True)
    movie_genre_df["id"] = movie_genre_df.index

    # select only the columns we care about in the correct order
    movie_genre_df = movie_genre_df[["id", "movie_id", "genre_id"]]
    movie_genre_df.to_sql(name="movies_genres", con=engine, index=False, if_exists="replace")


def get_session() -> Session:
    """
    Get a SQLAlchemy session for interacting with the database

    Usage:
    with get_session() as session:
        # interact with database via session
    """
    load_dotenv()
    CS = os.getenv("CS")
    engine = create_engine(CS)

    # use sessionmaker to create session factory based on engine
    Session: Session = sessionmaker(bind=engine)
    return Session()

if __name__ == "__main__":
    setup()