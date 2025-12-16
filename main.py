""" Main entry point for Library Management System """
import tkinter as tk
from log_in import LoginWindow

def main():
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# run the code here 

# pyinstaller --onefile --windowed --hidden-import mysql.connector.plugins.mysql_native_password --hidden-import reportlab main.py