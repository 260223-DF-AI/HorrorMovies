"""Interacting with PostgreSQL"""
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.types import * #replace with only necessary types
from sqlalchemy.orm import DeclarativeBasem, Mapped, mapped_column, relationship
from dotenv import load_dotenv
from datetime import datetime
import os

# TODO: Split primary and foreign keys, finances table (1:1), collections table (1:M)

def setup():
    """
    Setup connection to PostgreSQL database using SQLAlchemy
    """
    load_dotenv()
    CS = os.getenv("CS")
    engine = create_engine(CS)

class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_title: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    original_language: Mapped[str] = mapped_column(String(2), nullable=False)
    release_date: Mapped[datetime] = mapped_column(Date)
    genres: Mapped[list["Genre"]] = relationship(back_populates="movie")
    collection_id: Mapped[int] = mapped_column(Integer)

class Metadatum(Base):
    __tablename__ = "metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    overview: Mapped[str] = mapped_column(Text)
    tagline: Mapped[str] = mapped_column(Text)
    adult: Mapped[str] = mapped_column(Boolean)

class Rating(Base):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    popularity: Mapped[float] = mapped_column(Float)
    vote_count: Mapped[int] = mapped_column(Integer)
    vote_average: Mapped[float] = mapped_column(Float)

class Finance(Base):
    __tablename__ = "finances"

    id: Mapped[int] = mapped_column()

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    genre_name: Mapped[str] = mapped_column(String(14), nullable=False)
    movies: Mapped[list["Movie"]] = relationship(back_populates="genres")

class Movie_Genre(Base):
    # Junction Table
    __tablename__ = "movies_genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))

    # ???

class collection 



if __name__ == "__main__":
    pass