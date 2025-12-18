import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "library.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.sql")

def init_db(load_data=True):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if librarians table exists (indicator that schema was loaded)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='LIBRARIANS'")
    tables_exist = cursor.fetchone() is not None
    
    # Load schema if tables don't exist
    if not tables_exist:
        print("Creating database schema...")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        print("✓ Database schema created.")
    
    # Check if librarians table is empty
    cursor.execute("SELECT COUNT(*) FROM LIBRARIANS")
    librarians_count = cursor.fetchone()[0]
    
    # Load sample data if librarians table is empty
    if load_data and librarians_count == 0 and os.path.exists(DATA_PATH):
        print("Loading sample data...")
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        print("✓ Sample data loaded successfully.")
    
    conn.commit()
    conn.close()
    print("✓ Database ready.")

if __name__ == "__main__":
    init_db()