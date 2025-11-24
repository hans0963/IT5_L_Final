"""
Login and Registration GUI module
"""
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from datetime import date
from database import db
from validators import validate_email, validate_username, validate_password
from tkinter import END

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System - Login")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Show login page
        self.show_login_page()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
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
            text="Library Management System", 
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=30)
        
        subtitle_label = tk.Label(
            main_frame, 
            text="Librarian Login", 
            font=('Arial', 14),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        subtitle_label.pack(pady=10)
        
        # Login form frame
        form_frame = tk.Frame(main_frame, bg='#34495e', padx=40, pady=30)
        form_frame.pack(pady=20, padx=50)
        
        # Username
        username_label = tk.Label(
            form_frame, 
            text="Username:", 
            font=('Arial', 11),
            bg='#34495e',
            fg='white'
        )
        username_label.grid(row=0, column=0, sticky='w', pady=10)
        
        self.username_entry = ttk.Entry(form_frame, font=('Arial', 11), width=25)
        self.username_entry.grid(row=1, column=0, pady=(0, 15))
        
        # Password
        password_label = tk.Label(
            form_frame, 
            text="Password:", 
            font=('Arial', 11),
            bg='#34495e',
            fg='white'
        )
        password_label.grid(row=2, column=0, sticky='w', pady=10)
        
        self.password_entry = ttk.Entry(form_frame, font=('Arial', 11), width=25, show='*')
        self.password_entry.grid(row=3, column=0, pady=(0, 20))
        
        # Login button
        login_btn = tk.Button(
            form_frame,
            text="Login",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            cursor='hand2',
            width=20,
            command=self.login
        )
        login_btn.grid(row=4, column=0, pady=10)
        
        # Register link
        register_frame = tk.Frame(main_frame, bg='#2c3e50')
        register_frame.pack(pady=20)
        
        register_label = tk.Label(
            register_frame,
            text="Don't have an account?",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        register_label.pack(side=tk.LEFT)
        
        register_btn = tk.Button(
            register_frame,
            text="Register Here",
            font=('Arial', 10, 'bold'),
            bg='#2c3e50',
            fg='#3498db',
            border=0,
            cursor='hand2',
            command=self.show_register_page
        )
        register_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.login())

    def login(self):
        """Handle login authentication"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password")
            self.clear_login_fields()
            return

        hashed_password = self.hash_password(password)

        query = "SELECT * FROM librarian WHERE username = %s AND password = %s"
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
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.username_entry.focus()

    def open_dashboard(self, user_data):
        """Open the dashboard window"""
        from dashboard import DashboardWindow
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
        
        # Register button
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
        
        # Back button
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
        
        # Email validation
        if not validate_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return
        
        # Username rule
        if not validate_username(username):
            messagebox.showerror(
                "Invalid Username",
                "Username must be 4-30 characters and contain only letters, numbers, and underscores."
            )
            return
            
        # Password match
        if password != confirm_password:
            messagebox.showerror("Password Error", "Passwords do not match")
            return

        # Strong password validation
        is_valid, msg = validate_password(password)
        if not is_valid:
            messagebox.showerror("Weak Password", msg)
            return
        
        try:
            hashed_password = self.hash_password(password)
            
            query = """
                INSERT INTO librarian (first_name, last_name, email, username, password, hire_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, email, username, hashed_password, date.today())
            
            if db.execute_query(query, values, fetch=False):
                messagebox.showinfo("Success", "Registration successful! You can now login.")
                self.show_login_page()
        except Exception as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Registration Error", "Username or email already exists")
            else:
                messagebox.showerror("Database Error", f"Error during registration: {e}")