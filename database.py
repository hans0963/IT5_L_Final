"""
Database connection and operations handler
"""
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='library_management',
                user='root',  # Change this to your MySQL username
                password=''   # Change this to your MySQL password
            )
            if self.connection.is_connected():
                print("Successfully connected to database")
                return True
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            return False
    
    def execute_query(self, query, params=None, fetch=True):
        """Execute a query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
        except Error as e:
            messagebox.showerror("Database Error", f"Error executing query: {e}")
            return None if fetch else False
    
    def execute_query_one(self, query, params=None):
        """Execute a query and return one result"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            messagebox.showerror("Database Error", f"Error executing query: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

# Global database instance
db = Database()