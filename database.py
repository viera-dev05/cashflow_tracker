import sqlite3
import os

# Set up database path to folder named 'data' in the project directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "database.db")

def init_db():
    """Initialize the database with the required tables."""
    # Create the 'data' directory if it doesn't exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with sqlite3.connect(DB_PATH) as db:
        # Create users table if it doesn't exist
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                hash TEXT NOT NULL
            )
        """)


    with sqlite3.connect(DB_PATH) as db:
        # Create categories table if it doesn't exist
        db.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            type TEXT NOT NULL CHECK (type IN ('Income', 'Outcome')),
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(category, type, user_id)
        )
        """)


    # TODO: Add more tables as needed    