import sqlite3
from pathlib import Path

def get_database_connection(db_name="khanoumi.db"):
    """Connect to SQLite database."""
    try:
        base_dir = Path(__file__).resolve().parent
        db_path = base_dir / db_name
        
        conn = sqlite3.connect(db_path)
        print(f"Connected to database at: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

if __name__ == "__main__":
    connection = get_database_connection()
    if connection:
        connection.close()