"""Main Dashboard GUI module"""
import tkinter as tk
from tkinter import messagebox

class DashboardWindow:
    def __init__(self, root, user_data, login_root):
        self.root = root
        self.user_data = user_data
        self.login_root = login_root
        
        self.root.title("Library Management System - Dashboard")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.show_dashboard()
    
    def clear_frame(self):
        """Clear all widgets from the frame"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def on_closing(self):
        """Handle window closing"""
        self.root.destroy()
        self.login_root.destroy()
    
    def show_dashboard(self):
        """Display main dashboard"""
        self.clear_frame()
        
        # Main container
        main_container = tk.Frame(self.root, bg='#ecf0f1')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Top bar
        top_bar = tk.Frame(main_container, bg='#2c3e50', height=80)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Welcome message
        welcome_label = tk.Label(
            top_bar,
            text=f"Welcome, {self.user_data['first_name']} {self.user_data['last_name']}!",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        welcome_label.pack(side=tk.LEFT, padx=30, pady=20)
        
        # Logout button
        logout_btn = tk.Button(
            top_bar,
            text="Logout",
            font=('Arial', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            cursor='hand2',
            width=10,
            command=self.logout
        )
        logout_btn.pack(side=tk.RIGHT, padx=30, pady=20)
        
        # Dashboard content
        content_frame = tk.Frame(main_container, bg='#ecf0f1')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        # Title
        title_label = tk.Label(
            content_frame,
            text="Library Management Dashboard",
            font=('Arial', 20, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Button grid frame
        button_grid = tk.Frame(content_frame, bg='#ecf0f1')
        button_grid.pack(expand=True)
        
        # Define dashboard buttons
        buttons = [
            ("Students", self.show_student_management, '#3498db'),
            ("Books", self.show_book_management, '#9b59b6'),
            ("Borrow", self.show_borrow_management, '#e67e22'),
            ("Return", self.show_return_management, '#1abc9c'),
            ("Reservations", self.show_reservations, '#34495e'),
            ("Fines", self.show_fines_management, '#c0392b'),
            ("Summary Report", self.show_summary_report, '#BAB86C')
        ]
        
        # Create buttons in grid
        row, col = 0, 0
        for text, command, color in buttons:
            btn = tk.Button(
                button_grid,
                text=text,
                font=('Arial', 14, 'bold'),
                bg=color,
                fg='white',
                cursor='hand2',
                width=15,
                height=3,
                command=command
            )
            btn.grid(row=row, column=col, padx=15, pady=15)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def logout(self):
        """Handle logout"""
        self.root.destroy()
        self.login_root.deiconify()
    
    def show_student_management(self):
        """Open student management window"""
        from Modules.students import StudentManagementWindow
        self.root.withdraw()
        student_root = tk.Toplevel(self.root)
        StudentManagementWindow(student_root, self.user_data, self.root)
        student_root.protocol("WM_DELETE_WINDOW", lambda: [student_root.destroy(), self.root.deiconify()])
    
    def show_book_management(self):
        """Open books management window"""
        from Modules.books import BookmanagementWindow  # fixed class name
        self.root.withdraw()
        books_root = tk.Toplevel(self.root)
        BookmanagementWindow(books_root, self.user_data, self.root)
        books_root.protocol("WM_DELETE_WINDOW", lambda: [books_root.destroy(), self.root.deiconify()])
    
    def show_borrow_management(self):
        from Modules.borrow import BorrowManagementWindow
        self.root.withdraw()
        borrow_root = tk.Toplevel(self.root)
        BorrowManagementWindow(borrow_root, user_data=self.user_data, dashboard_root=self.root)
        borrow_root.protocol("WM_DELETE_WINDOW", lambda: [borrow_root.destroy(), self.root.deiconify()])
    
    def show_return_management(self):
        from Modules.return_book import ReturnWindow
        self.root.withdraw()
        return_root = tk.Toplevel(self.root)
        ReturnWindow(return_root, self.user_data, dashboard_root=self.root)
        return_root.protocol("WM_DELETE_WINDOW", lambda: [return_root.destroy(), self.root.deiconify()])
    
    def show_reservations(self):
        from Modules.reservations import ReservationWindow
        self.root.withdraw()
        reservation_root = tk.Toplevel(self.root)
        ReservationWindow(reservation_root, self.user_data, self.root)
        reservation_root.protocol("WM_DELETE_WINDOW", lambda: [reservation_root.destroy(), self.root.deiconify()])
    
    def show_fines_management(self):
        from Modules.fine import FineManagementWindow
        self.root.withdraw()
        fines_root = tk.Toplevel(self.root)
        FineManagementWindow(fines_root, self.user_data, self.root)
        fines_root.protocol("WM_DELETE_WINDOW", lambda: [fines_root.destroy(), self.root.deiconify()])
    
    def show_summary_report(self):
        from Modules.summary_report import SummaryReportWindow
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)
        SummaryReportWindow(new_window, self.user_data, self.root)
        new_window.protocol("WM_DELETE_WINDOW", lambda: [new_window.destroy(), self.root.deiconify()])