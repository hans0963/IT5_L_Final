"""Database connection and operations handler (SQLite)"""
import sqlite3
from tkinter import messagebox
import os, sys, shutil


# Always use absolute path so the database file is consistent
def get_db_path():
    if getattr(sys, 'frozen', False):  # running from exe
        # writable folder next to the exe
        base_dir = os.path.dirname(sys.executable)
        db_path = os.path.join(base_dir, "library.db")

        # if no persistent copy exists, copy from bundled Core/library.db
        bundled_db = os.path.join(sys._MEIPASS, "Core", "library.db")
        if not os.path.exists(db_path):
            shutil.copyfile(bundled_db, db_path)

        return db_path
    else:  # running from source
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "library.db")

DB_NAME = get_db_path()

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Connect to SQLite database (creates file if missing)"""
        try:
            self.connection = sqlite3.connect(DB_NAME)
            # Ensure rows behave like dictionaries
            self.connection.row_factory = sqlite3.Row
            # Print absolute path for debugging
            print(f"✓ Connected to SQLite database at: {os.path.abspath(DB_NAME)}")
            return self.connection
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            return None

    def get_connection(self):
        """Always return a valid connection"""
        if not self.connection:
            self.connect()
        return self.connection

    def execute_query(self, query, params=None, fetch=True):
        """Execute SELECT or INSERT/UPDATE/DELETE automatically"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            is_select = query.strip().lower().startswith("select")

            if is_select and fetch:
                result = [dict(row) for row in cursor.fetchall()]
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                print(f"✓ Query committed: {query[:60]}...")
                return True

        except sqlite3.Error as e:
            print(f"❌ Database Error: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Error executing query:\n{e}")
            return False

    def execute_query_one(self, query, params=None):
        """Fetch exactly one row"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            row = cursor.fetchone()
            cursor.close()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"❌ Database Error: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Error executing query:\n{e}")
            return None

    def close(self):
        if self.connection:
            try:
                self.connection.close()
                print("✓ Database connection closed")
            except Exception as e:
                print(f"❌ Error closing database: {e}")

# Global database instance
db = Database()

def setup_database():
    """Create required tables if they don't exist"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Librarians table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS librarians (
            librarian_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            hire_date TEXT NOT NULL
        )
    """)

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            registration_date TEXT NOT NULL
        )
    """)

    # Books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT NOT NULL UNIQUE,
            year TEXT NOT NULL,
            available INTEGER NOT NULL DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()
    print("✓ Database setup complete")