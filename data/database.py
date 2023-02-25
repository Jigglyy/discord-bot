import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_table():
    """Creates the users table if it doesn't exist."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            discriminator TEXT
        )
    """)
    
    conn.commit()
    conn.close()
