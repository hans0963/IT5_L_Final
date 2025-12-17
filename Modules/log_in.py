"""
Login and Registration module for Library Management System (SQLite version)
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

        self.show_login_page()

    def clear_frame(self):
        """Clear all widgets from the frame"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_page(self):
        """Display login page"""
        self.clear_frame()

        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Librarian Login",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=20)

        # Login form frame
        form_frame = tk.Frame(main_frame, bg='#34495e', padx=40, pady=30)
        form_frame.pack(pady=10, padx=50)

        # Username
        tk.Label(form_frame, text="Username:", font=('Arial', 10), bg='#34495e', fg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = ttk.Entry(form_frame, font=('Arial', 10), width=25)
        self.username_entry.grid(row=1, column=0, pady=(0, 10))

        # Password
        tk.Label(form_frame, text="Password:", font=('Arial', 10), bg='#34495e', fg='white').grid(row=2, column=0, sticky='w', pady=5)
        self.password_entry = ttk.Entry(form_frame, font=('Arial', 10), width=25, show='*')
        self.password_entry.grid(row=3, column=0, pady=(0, 10))

        # Buttons frame
        btn_frame = tk.Frame(form_frame, bg='#34495e')
        btn_frame.grid(row=4, column=0, pady=10)

        login_btn = tk.Button(
            btn_frame,
            text="Login",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            cursor='hand2',
            width=12,
            command=self.login
        )
        login_btn.pack(side=tk.LEFT, padx=5)

        register_btn = tk.Button(
            btn_frame,
            text="Register",
            font=('Arial', 11),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            width=12,
            command=self.show_register_page
        )
        register_btn.pack(side=tk.LEFT, padx=5)

    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        """Handle login authentication"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password")
            self.clear_login_fields()
            return

        hashed_password = self.hash_password(password)

        query = "SELECT * FROM librarians WHERE username = ? AND password = ?"
        result = db.execute_query_one(query, (username, hashed_password))

        if result:
            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {result['first_name']} {result['last_name']}!"
            )
            self.clear_login_fields()
            self.open_dashboard(result)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.clear_login_fields()

    def clear_login_fields(self):
        """Reset login input fields"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus()

    def open_dashboard(self, user_data):
        """Open the dashboard window"""
        from Modules.dashboard import DashboardWindow
        self.root.withdraw()  # Hide login window
        dashboard_root = tk.Toplevel(self.root)
        DashboardWindow(dashboard_root, user_data, self.root)

    def show_register_page(self):
        """Display registration page"""
        self.clear_frame()

        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Librarian Registration",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=20)

        # Registration form frame
        form_frame = tk.Frame(main_frame, bg='#34495e', padx=40, pady=30)
        form_frame.pack(pady=10, padx=50)

        # First Name
        tk.Label(form_frame, text="First Name:", font=('Arial', 10), bg='#34495e', fg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.reg_firstname = ttk.Entry(form_frame, font=('Arial', 10), width=25)
        self.reg_firstname.grid(row=1, column=0, pady=(0, 10))

        # Last Name
        tk.Label(form_frame, text="Last Name:", font=('Arial', 10), bg='#34495e', fg='white').grid(row=2, column=0, sticky='w', pady=5)
        self.reg_lastname = ttk.Entry(form_frame, font=('Arial', 10), width=25)
        self.reg_lastname.grid(row=3, column=0, pady=(0, 10))

        # Email
        tk.Label(form_frame, text="Email:", font=('Arial', 10), bg='#34495e', fg='white').grid(row=4, column=0, sticky='w', pady=5)
        self.reg_email = ttk.Entry(form_frame, font=('Arial', 10), width=25)
        self.reg_email.grid(row=5, column=0, pady=(0, 10))

        # Username
        tk.Label(form_frame, text="Username:", font=('Arial', 10), bg='#34495e', fg='white').grid(row=6, column=0, sticky='w', pady=5)
        self.reg_username = ttk.Entry(form_frame, font=('Arial', 10), width=25)
        self.reg_username.grid(row=7, column=0, pady=(0, 10))

        # Password
        tk.Label(form_frame, text="Password:", font=('Arial', 10), bg='#34495e', fg='white').grid(row=8, column=0, sticky='w', pady=5)
        self.reg_password = ttk.Entry(form_frame, font=('Arial', 10), width=25, show='*')
        self.reg_password.grid(row=9, column=0, pady=(0, 10))

        # Confirm Password
        tk.Label(form_frame, text="Confirm Password:", font=('Arial', 10), bg='#34495e', fg='white').grid(row=10, column=0, sticky='w', pady=5)
        self.reg_confirm_password = ttk.Entry(form_frame, font=('Arial', 10), width=25, show='*')
        self.reg_confirm_password.grid(row=11, column=0, pady=(0, 15))

        # Buttons frame
        btn_frame = tk.Frame(form_frame, bg='#34495e')
        btn_frame.grid(row=12, column=0, pady=10)

        register_btn = tk.Button(
            btn_frame,
            text="Register",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            cursor='hand2',
            width=12,
            command=self.register
        )
        register_btn.pack(side=tk.LEFT, padx=5)

        back_btn = tk.Button(
            btn_frame,
            text="Back to Login",
            font=('Arial', 11),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            width=12,
            command=self.show_login_page
        )
        back_btn.pack(side=tk.LEFT, padx=5)

    def register(self):
        """Handle librarian registration"""
        first_name = self.reg_firstname.get().strip()
        last_name = self.reg_lastname.get().strip()
        email = self.reg_email.get().strip()
        username = self.reg_username.get().strip()
        password = self.reg_password.get().strip()
        confirm_password = self.reg_confirm_password.get().strip()

        # Validation
        if not all([first_name, last_name, email, username, password, confirm_password]):
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return

        if not validate_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        if not validate_username(username):
            messagebox.showerror(
                "Invalid Username",
                "Username must be 4-30 characters and contain only letters, numbers, and underscores."
            )
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
            print(f"🔐 Registering librarian: {username}")

            query = """
                INSERT INTO librarians (first_name, last_name, email, username, password, hire_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            values = (first_name, last_name, email, username, hashed_password, date.today().isoformat())

            result = db.execute_query(query, values, fetch=False)
            print(f"✓ Registration result: {result}")
            
            if result:
                # Verify the data was saved by querying it back
                verify_query = "SELECT * FROM librarians WHERE username = ?"
                saved_data = db.execute_query_one(verify_query, (username,))
                print(f"✓ Verification - Data saved: {saved_data is not None}")
                
                messagebox.showinfo("Success", "Registration successful! You can now login.")
                self.show_login_page()
            else:
                messagebox.showerror("Error", "Failed to register. Check console for details.")
        except Exception as e:
            print(f"❌ Registration exception: {e}")
            if "UNIQUE constraint failed" in str(e):
                messagebox.showerror("Registration Error", "Username or email already exists")
            else:
                messagebox.showerror("Database Error", f"Error during registration: {e}")

