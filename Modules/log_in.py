"""
Login and Registration module for Library Management System (SQLite version)
GUI DESIGN APPLIED ONLY
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import hashlib

from Modules.dashboard import DashboardWindow
from Core.database import db
from Core.validators import validate_email, validate_username, validate_password


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System - Login")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use("clam")

        self.show_login_page()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ================= LOGIN PAGE =================
    def show_login_page(self):
        self.clear_frame()

        main = tk.Frame(self.root, bg="#2c3e50")
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            main,
            text="School Library Borrowing and Cataloging System",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=30)

        tk.Label(
            main,
            text="Librarian Login",
            font=("Arial", 14),
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(pady=10)

        form = tk.Frame(main, bg="#34495e", padx=40, pady=30)
        form.pack(pady=20)

        # Username
        tk.Label(form, text="Username:", bg="#34495e",
                 fg="white", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=10)
        self.username_entry = ttk.Entry(form, width=25)
        self.username_entry.grid(row=1, column=0, pady=(0, 15))

        # Password
        tk.Label(form, text="Password:", bg="#34495e",
                 fg="white", font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=10)
        self.password_entry = ttk.Entry(form, width=25, show="*")
        self.password_entry.grid(row=3, column=0, pady=(0, 20))

        tk.Button(
            form, text="Login",
            width=20,
            bg="#27ae60", fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            command=self.login
        ).grid(row=4, column=0, pady=10)

        # Register link
        link_frame = tk.Frame(main, bg="#2c3e50")
        link_frame.pack(pady=20)

        tk.Label(
            link_frame,
            text="Don't have an account?",
            bg="#2c3e50",
            fg="#ecf0f1",
            font=("Arial", 10)
        ).pack(side=tk.LEFT)

        tk.Button(
            link_frame,
            text="Register Here",
            bg="#2c3e50",
            fg="#3498db",
            font=("Arial", 10, "bold"),
            border=0,
            cursor="hand2",
            command=self.show_register_page
        ).pack(side=tk.LEFT, padx=5)

        self.password_entry.bind("<Return>", lambda e: self.login())

    # ================= REGISTER PAGE =================
    def show_register_page(self):
        self.clear_frame()

        main = tk.Frame(self.root, bg="#2c3e50")
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            main,
            text="Librarian Registration",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=20)

        form = tk.Frame(main, bg="#34495e", padx=40, pady=30)
        form.pack(pady=10)

        def field(label, row, attr, show=None):
            tk.Label(form, text=label, bg="#34495e",
                     fg="white", font=("Arial", 10)).grid(row=row, column=0, sticky="w", pady=5)
            entry = ttk.Entry(form, width=25, show=show)
            entry.grid(row=row + 1, column=0, pady=(0, 10))
            setattr(self, attr, entry)

        field("First Name:", 0, "reg_firstname")
        field("Last Name:", 2, "reg_lastname")
        field("Email:", 4, "reg_email")
        field("Username:", 6, "reg_username")
        field("Password:", 8, "reg_password", "*")
        field("Confirm Password:", 10, "reg_confirm_password", "*")

        btns = tk.Frame(form, bg="#34495e")
        btns.grid(row=12, column=0, pady=10)

        tk.Button(
            btns, text="Register",
            width=12,
            bg="#27ae60", fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            command=self.register
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btns, text="Back to Login",
            width=12,
            bg="#95a5a6", fg="white",
            font=("Arial", 11),
            cursor="hand2",
            command=self.show_login_page
        ).pack(side=tk.LEFT, padx=5)

    # ================= LOGIC (UNCHANGED) =================
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password")
            return

        hashed_password = self.hash_password(password)
        query = "SELECT * FROM librarians WHERE username = ? AND password = ?"
        result = db.execute_query_one(query, (username, hashed_password))

        if result:
            messagebox.showinfo("Login Successful",
                                f"Welcome, {result['first_name']} {result['last_name']}!")
            self.open_dashboard(result)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_dashboard(self, user_data):
        self.root.withdraw()
        dashboard_root = tk.Toplevel(self.root)
        DashboardWindow(dashboard_root, user_data, self.root)

    def register(self):
        first_name = self.reg_firstname.get().strip()
        last_name = self.reg_lastname.get().strip()
        email = self.reg_email.get().strip()
        username = self.reg_username.get().strip()
        password = self.reg_password.get().strip()
        confirm_password = self.reg_confirm_password.get().strip()

        if not all([first_name, last_name, email, username, password, confirm_password]):
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return

        if not validate_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return

        if not validate_username(username):
            messagebox.showerror("Invalid Username", "Username must be 4-30 characters")
            return

        if password != confirm_password:
            messagebox.showerror("Password Error", "Passwords do not match")
            return

        is_valid, msg = validate_password(password)
        if not is_valid:
            messagebox.showerror("Weak Password", msg)
            return

        try:
            hashed_password = self.hash_password(password)
            query = """
                INSERT INTO librarians (first_name, last_name, email, username, password, hire_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            values = (first_name, last_name, email, username,
                      hashed_password, date.today().isoformat())
            db.execute_query(query, values, fetch=False)

            messagebox.showinfo("Success", "Registration successful! You can now login.")
            self.show_login_page()

        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Registration Error", "Username or email already exists")
            else:
                messagebox.showerror("Database Error", str(e))
