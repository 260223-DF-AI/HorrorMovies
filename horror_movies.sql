-- SETUP HORROR MOVIE DATABASE AND TABLES

CREATE DATABASE IF NOT EXISTS horror_movies;

CREATE TABLE IF NOT EXISTS movies (
    id INT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    original_title VARCHAR(50) NOT NULL,
    original_language VARCHAR(2),
    release_date DATE,
    collection    
)

id rev budget
    runtime TINYINT,

id description tagline

JUNCTION GENRES





"id","original_title","title","original_language",
"overview","tagline","release_date","poster_path",
"popularity","vote_count","vote_average","budget",
"revenue","runtime","status","adult","backdrop_path",
"genre_names","collection","collection_name"
