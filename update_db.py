from website import create_app, db
from website.models import User, Note
import sqlite3
import os

def update_database_schema():
    """Add title column to note table if it doesn't exist"""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "database.db")
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("Database doesn't exist yet. It will be created with the latest schema.")
        return
        
    # Connect to existing database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if title column exists
    cursor.execute("PRAGMA table_info(note)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Add title column if it doesn't exist
    if "title" not in columns:
        print("Adding 'title' column to note table...")
        cursor.execute("ALTER TABLE note ADD COLUMN title TEXT")
        conn.commit()
        print("Database schema updated successfully.")
    else:
        print("Title column already exists.")
        
    conn.close()

if __name__ == "__main__":
    update_database_schema()
