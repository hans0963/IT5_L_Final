#!/usr/bin/env python3
"""Debug script to check database status"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")

print(f"Database path: {DB_PATH}")
print(f"Database exists: {os.path.exists(DB_PATH)}")

if os.path.exists(DB_PATH):
    print(f"Database size: {os.path.getsize(DB_PATH)} bytes")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\nTables in database: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check librarians
    cursor.execute("SELECT COUNT(*) FROM librarians")
    count = cursor.fetchone()[0]
    print(f"\nLibrarians count: {count}")
    
    if count > 0:
        cursor.execute("SELECT username, email FROM librarians")
        for row in cursor.fetchall():
            print(f"  - {row[0]} ({row[1]})")
    
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    print(f"Students count: {count}")
    
    conn.close()
else:
    print("Database does not exist!")
