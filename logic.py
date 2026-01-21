# logic.py
import sqlite3
import random

DB_NAME = "movies.db"

# ================== DATA AWAL (BANYAK) ==================
SEED_DATA = [
    # ================= FILM ACTION =================
    ("The Dark Knight", "film", "action"),
    ("Inception", "film", "action"),
    ("The Matrix", "film", "action"),
    ("John Wick", "film", "action"),
    ("John Wick: Chapter 2", "film", "action"),
    ("John Wick: Chapter 3", "film", "action"),
    ("Mad Max: Fury Road", "film", "action"),
    ("Gladiator", "film", "action"),
    ("Die Hard", "film", "action"),
    ("Casino Royale", "film", "action"),
    ("Logan", "film", "action"),
    ("Top Gun: Maverick", "film", "action"),

    # ================= FILM SCI-FI =================
    ("Interstellar", "film", "sci-fi"),
    ("Blade Runner 2049", "film", "sci-fi"),
    ("Arrival", "film", "sci-fi"),
    ("Dune", "film", "sci-fi"),
    ("Dune: Part Two", "film", "sci-fi"),
    ("Ex Machina", "film", "sci-fi"),
    ("Minority Report", "film", "sci-fi"),
    ("Edge of Tomorrow", "film", "sci-fi"),

    # ================= FILM DRAMA =================
    ("The Shawshank Redemption", "film", "drama"),
    ("Forrest Gump", "film", "drama"),
    ("Fight Club", "film", "drama"),
    ("The Godfather", "film", "drama"),
    ("The Godfather Part II", "film", "drama"),
    ("Joker", "film", "drama"),
    ("Parasite", "film", "drama"),
    ("Whiplash", "film", "drama"),

    # ================= FILM COMEDY =================
    ("The Hangover", "film", "comedy"),
    ("Superbad", "film", "comedy"),
    ("Deadpool", "film", "comedy"),
    ("Step Brothers", "film", "comedy"),
    ("The Grand Budapest Hotel", "film", "comedy"),

    # ================= FILM HORROR =================
    ("The Conjuring", "film", "horror"),
    ("Hereditary", "film", "horror"),
    ("It", "film", "horror"),
    ("Get Out", "film", "horror"),
    ("A Quiet Place", "film", "horror"),

    # ================= SERIAL ACTION =================
    ("The Boys", "serial", "action"),
    ("Reacher", "serial", "action"),
    ("24", "serial", "action"),
    ("Jack Ryan", "serial", "action"),
    ("Vikings", "serial", "action"),

    # ================= SERIAL SCI-FI =================
    ("Stranger Things", "serial", "sci-fi"),
    ("Black Mirror", "serial", "sci-fi"),
    ("Dark", "serial", "sci-fi"),
    ("Westworld", "serial", "sci-fi"),
    ("The Expanse", "serial", "sci-fi"),

    # ================= SERIAL DRAMA =================
    ("Breaking Bad", "serial", "drama"),
    ("Better Call Saul", "serial", "drama"),
    ("Peaky Blinders", "serial", "drama"),
    ("The Sopranos", "serial", "drama"),
    ("Chernobyl", "serial", "drama"),

    # ================= SERIAL COMEDY =================
    ("Friends", "serial", "comedy"),
    ("The Office", "serial", "comedy"),
    ("Brooklyn Nine-Nine", "serial", "comedy"),
    ("How I Met Your Mother", "serial", "comedy"),
    ("Ted Lasso", "serial", "comedy"),

    # ================= SERIAL HORROR =================
    ("The Walking Dead", "serial", "horror"),
    ("The Haunting of Hill House", "serial", "horror"),
    ("Midnight Mass", "serial", "horror"),
    ("From", "serial", "horror"),
]

# ================== DATABASE ==================
def connect():
    return sqlite3.connect(DB_NAME)

def setup_database():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            type TEXT,
            genre TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER,
            user_id INTEGER,
            rating INTEGER,
            FOREIGN KEY(movie_id) REFERENCES movies(id)
        )
    """)

    for title, tipe, genre in SEED_DATA:
        cur.execute(
            "INSERT OR IGNORE INTO movies (title, type, genre) VALUES (?, ?, ?)",
            (title, tipe, genre)
        )

    conn.commit()
    conn.close()

# ================== LOGIC ==================
def get_genres():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT genre FROM movies")
    genres = [g[0] for g in cur.fetchall()]
    conn.close()
    return genres

def get_recommendation(tipe, genre):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title FROM movies WHERE type=? AND genre=? ORDER BY RANDOM() LIMIT 1",
        (tipe.lower(), genre.lower())
    )
    data = cur.fetchone()
    conn.close()
    return data

def add_rating(movie_id, user_id, rating):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ratings (movie_id, user_id, rating) VALUES (?, ?, ?)",
        (movie_id, user_id, rating)
    )
    conn.commit()
    conn.close()

def get_average_rating(movie_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT AVG(rating) FROM ratings WHERE movie_id=?", (movie_id,))
    avg = cur.fetchone()[0]
    conn.close()
    return round(avg, 2) if avg else None
