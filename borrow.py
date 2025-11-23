"""
Borrow GUI module
"""
import tkinter as tk
from tkinter import ttk, messagebox
from database import db

class BorrowManagementWindow:
    def __init__(self, root, user_data, dashboard_root):
        self.root = root
        self.user_data = user_data
        self.dashboard_root = dashboard_root
        
        self.root.title("Borrow Books")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.show_student_management()
    
    def clear_frame(self):
        """Clear all widgets from the frame"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def on_closing(self):
        """Handle window closing"""
        self.go_back()
    
    def go_back(self):
        """Return to dashboard"""
        self.root.destroy()
        self.dashboard_root.deiconify()
    
    def show_borrow_management(self):
        """Display borrow management page"""
        self.clear_frame()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top navigation bar
        nav_frame = tk.Frame(main_frame, bg='#2c3e50', height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)
        
        # Back button
        back_btn = tk.Button(
            nav_frame,
            text="← Back to Dashboard",
            font=('Arial', 11),
            bg='#34495e',
            fg='white',
            cursor='hand2',
            command=self.go_back
        )
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Title
        title_label = tk.Label(
            nav_frame,
            text="Borrow Management",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side=tk.LEFT, padx=20)
        
        # User info
        user_label = tk.Label(
            nav_frame,
            text=f"Logged in: {self.user_data['first_name']} {self.user_data['last_name']}",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        user_label.pack(side=tk.RIGHT, padx=20)