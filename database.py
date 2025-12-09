"""Database connection and operations handler"""
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Connect to MySQL database with fallback"""
        try:
            self.connection = mysql.connector.connect(
                host='127.0.0.1',
                database='library_management',
                user='libadmin',
                password='7548'
            )
            if self.connection.is_connected():
                print("Successfully connected to database")
                return self.connection
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            return None

    def get_connection(self):
        """Ensure connection is alive, reconnect if needed"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection

    def execute_query(self, query, params=None, fetch=True):
        """Execute SELECT or INSERT/UPDATE/DELETE automatically"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            is_select = query.strip().lower().startswith("select")

            if is_select:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True

        except Error as e:
            messagebox.showerror("Database Error", f"Error executing query:\n{e}")
            return None

    def execute_query_one(self, query, params=None):
        """Fetch exactly one row"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            messagebox.showerror("Database Error", f"Error executing query:\n{e}")
            return None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

# Global database instance
db = Database()